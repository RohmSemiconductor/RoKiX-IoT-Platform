# The MIT License (MIT)
#
# Copyright (c) 2018 Rohm Semiconductor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
"""
KX132  data logger application
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_datalogger_args, get_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, POLARITY_DICT, CFG_POLARITY
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from kx132.kx132_driver import KX132Driver, r, b, m, e

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)


class KX132DataStream(StreamConfig):
    def __init__(self, sensor, pin_index=None):
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        self.define_request_message(
            fmt="<Bhhh",
            hdr="ch!ax!ay!az",
            reg=r.KX132_XOUT_L,
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=25,
                        max_range='2G',
                        lp_mode=False,
                        low_pass_filter='ODR_9',
                        power_off_on=True,          # set to False if this function is part of other configuration
                        int_number=None):
    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert convert_to_enumkey(odr) in e.KX132_ODCNTL_OSA.keys(), 'Invalid for odr value "{}". Valid values are {}'.format(
        convert_to_enumkey(odr), e.KX132_ODCNTL_OSA.keys())

    assert max_range in e.KX132_CNTL1_GSEL.keys(), 'Invalid  for range value "{}". Valid values are {}'.format(
        max_range, e.KX132_CNTL1_GSEL.keys())

    assert (lp_mode in list(e.KX132_LP_CNTL1_AVC.keys()) +
            [False]), 'Invalid for lp_mode value "{}". Valid values are: False or {}'.format(
                lp_mode, e.KX132_LP_CNTL1_AVC.keys())

    assert low_pass_filter in ['BYPASS', 'ODR_9', 'ODR_2'], 'Invalid filter value "{}". Valid values are: BYPASS or {}'.format(
        low_pass_filter, ['BYPASS', 'ODR_9', 'ODR_2'])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # select g-range
    sensor.set_range(e.KX132_CNTL1_GSEL[max_range])

    # resolution / power mode selection

    if lp_mode is not False:
        # enable low current mode
        sensor.reset_bit(r.KX132_CNTL1, b.KX132_CNTL1_RES)
        # define averaging value
        sensor.set_average(e.KX132_LP_CNTL1_AVC[lp_mode])
    else:
        # full resolution
        sensor.set_bit(r.KX132_CNTL1, b.KX132_CNTL1_RES)

    # odr setting for data logging
    sensor.set_odr(e.KX132_ODCNTL_OSA[convert_to_enumkey(odr)])

    # set bandwitdh
    if low_pass_filter != 'BYPASS':
        # FIXME use this pattern sensor.set_BW(e.KX022_ODCNTL_LPRO[low_pass_filter], 0, CH_ACC)
        if low_pass_filter == 'ODR_9':
            sensor.set_BW(0, 0, CH_ACC)
        else:
            sensor.set_BW(b.KX132_ODCNTL_LPRO, 0, CH_ACC)
        sensor.enable_iir()
    else:
        sensor.disable_iir()
    #
    # interrupt pin routings and settings
    #

    _intpin = 0
    if int_number is None:
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            _intpin = 1

        elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
            _intpin = 2

        elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
            # interrupt must be enabled to get register updates
            sensor.enable_drdy(intpin=1)

        else:
            pass  # INTERVAL_READ no need to do anything

    else:
        _intpin = int_number

    if _intpin > 0:
        LOGGER.debug('Configuring interrupt pin {}'.format(_intpin))
        if _intpin == 1:
            # latched interrupt
            sensor.set_bit_pattern(r.KX132_INC1, b.KX132_INC1_IEN1, b.KX132_INC1_IEN1 | b.KX132_INC1_IEL1)
            # sensor.reset_bit(r.KX132_INC1, b.KX132_INC1_IEL1)
            # sensor.set_bit(r.KX132_INC1, b.KX132_INC1_IEN1)  # enable interrupt
        else:
            # latched interrupt
            sensor.set_bit_pattern(r.KX132_INC5, b.KX132_INC5_IEN2, b.KX132_INC5_IEN2 | b.KX132_INC5_IEL2)
            # sensor.reset_bit(r.KX132_INC5, b.KX132_INC5_IEL2)
            # sensor.set_bit(r.KX132_INC5, b.KX132_INC5_IEN2)  # enable interrupt

        polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
        LOGGER.debug('Configuring interrupt polarity {}'.format(
            sensor.resource[CFG_POLARITY]))
        sensor.set_interrupt_polarity(intpin=_intpin, polarity=polarity)

        # use acc data ready
        sensor.enable_drdy(intpin=_intpin)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        # NOTE: temperature not available on low power mode, enabling only accel channel
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    dl = SensorDataLogger()
    dl.add_channel('ch!ax!ay!az')
    dl.start()

    try:
        while (loop is None) or (count < loop):
            count += 1
            sensor.drdy_function()
            ax, ay, az = sensor.read_data()
            dl.feed_values((10, ax, ay, az))

    except KeyboardInterrupt:
        dl.stop()


def read_with_stream(sensor, loop, timer=None, pin_index=None):
    assert not timer or not pin_index, 'Both timer and pin_index cannot be set at same time.'
    if timer:
        raise NotImplementedError
        #stream = KX132DataTimerStream(sensor=sensor, timer=timer)
    else:
        stream = KX132DataStream(sensor=sensor, pin_index=pin_index)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=25):
    args = get_datalogger_args()
    if args.odr:
        odr = args.odr
    sensor = KX132Driver()
    connection_manager = ConnectionManager(odr=odr)
    connection_manager.add_sensor(sensor)
    enable_data_logging(sensor, odr=odr)
    if args.stream_mode:
        read_with_stream(sensor, args.loop)

    elif args.timer_stream_mode:
        read_with_stream(sensor, loop=args.loop, timer=1. / odr)

    else:
        read_with_polling(sensor, args.loop)
    sensor.set_power_off()
    connection_manager.disconnect()


if __name__ == '__main__':
    app_main()
