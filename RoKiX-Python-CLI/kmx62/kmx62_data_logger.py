# The MIT License (MIT)
#
# Copyright (c) 2018 Kionix Inc.
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
KMX62 accelerometer/magnetomter sensor data logger application
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_datalogger_args, get_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, CH_MAG, CH_TEMP, POLARITY_DICT, CFG_POLARITY, ACTIVE_HIGH, ACTIVE_LOW
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from kmx62.kmx62_driver import KMX62Driver
from kmx62.kmx62_driver import r, b, m, e  # pylint: disable=unused-import
LOGGER = kx_logger.get_logger(__name__)
_CODE_FORMAT_VERSION = 2.0


class KMX62DataStream(StreamConfig):

    def __init__(self, sensor, pin_index=None):
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        self.define_request_message(
            fmt="<Bhhhhhhh",
            hdr="ch!ax!ay!az!mx!my!mz!temp",
            reg=r.KMX62_ACCEL_XOUT_L,
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=25,
                        max_range_acc='2G',
                        lp_mode=False,
                        power_off_on=True,
                        int_number=None):

    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert convert_to_enumkey(odr) in e.KMX62_ODCNTL_OSA.keys(
    ), 'Invalid odr_OSA value "{}". Support values are {}'.format(odr, e.KMX62_ODCNTL_OSA.keys())

    assert max_range_acc in e.KMX62_CNTL2_GSEL, 'Invalid range value "{}". Support values are {}'.format(
        max_range_acc, e.KMX62_CNTL2_GSEL.keys())

    assert (lp_mode in list(e.KMX62_CNTL2_RES.keys()) +
            [False]), 'Invalid lp_mode value "{}". Support values are {} and False'.format(lp_mode, e.KMX62_CNTL2_RES.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #
    # Select acc ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSA[convert_to_enumkey(odr)], CH_ACC)
    # Select mag ODRs
    sensor.set_odr(e.KMX62_ODCNTL_OSM[convert_to_enumkey(odr)], CH_MAG)

    # select g-range (for acc)
    sensor.set_range(e.KMX62_CNTL2_GSEL[max_range_acc])

    # resolution / power mode selection

    if lp_mode not in ['MAX1', 'MAX2', False]:
        # Low power mode
        sensor.set_average(e.KMX62_CNTL2_RES[lp_mode], None, CH_ACC)
    else:
        # Full power mode
        sensor.set_average(b.KMX62_CNTL2_RES_MAX2, None, CH_ACC)

    #
    # interrupt pin routings and settings
    #

    if int_number is None:
        # KMX62: interrupt source selection activates also physical interrupt pin
        if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
            sensor.enable_drdy(1, CH_ACC)  # acc data ready to int1
            # sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
        elif evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO2_INT':
            sensor.enable_drdy(2, CH_ACC)  # acc data ready to int2
            # sensor.enable_drdy(2, CH_MAG)                       # mag data ready to int2
        elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
            sensor.enable_drdy(1, CH_ACC)  # acc data ready to int1
            # sensor.enable_drdy(1, CH_MAG)                       # mag data ready to int1
    else:
        sensor.enable_drdy(int_number, CH_ACC)

    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrput polarity %s' % format(sensor.resource[CFG_POLARITY]))
    if polarity == ACTIVE_HIGH:
        IEA1 = b.KMX62_INC3_IEA1_HIGH
        IEA2 = b.KMX62_INC3_IEA2_HIGH
    elif polarity == ACTIVE_LOW:
        IEA1 = b.KMX62_INC3_IEA1_LOW
        IEA2 = b.KMX62_INC3_IEA2_LOW
    else:
        raise EvaluationKitException('Unsupported interrupt polarity %s' % sensor.resource[CFG_POLARITY])

    # interrupt signal parameters
    sensor.write_register(
        r.KMX62_INC3, 
        b.KMX62_INC3_IED1_PUSHPULL |
        IEA1 |
        b.KMX62_INC3_IEL1_LATCHED |
        b.KMX62_INC3_IED2_PUSHPULL | 
        IEA2 |
        b.KMX62_INC3_IEL2_LATCHED)
    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        # sensor.set_power_on(CH_MAG )                       # mag ON
        # sensor.set_power_on(CH_ACC | CH_MAG )              # acc + mag ON
        sensor.set_power_on(CH_ACC | CH_MAG | CH_TEMP)

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    dl = SensorDataLogger()
    dl.add_channel('ch!ax!ay!az!mx!my!mz!temp')
    dl.start()

    try:
        while (loop is None) or (count < loop):
            count += 1
            sensor.drdy_function()
            ax, ay, az, mx, my, mz, temp = sensor.read_data(CH_ACC | CH_MAG | CH_TEMP)
            dl.feed_values((10, ax, ay, az, mx, my, mz, temp))

    except (KeyboardInterrupt):
        dl.stop()


def read_with_stream(sensor, loop):
    stream = KMX62DataStream(sensor)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=25):

    args = get_datalogger_args()
    if args.odr:
        odr = args.odr
    sensor = KMX62Driver()
    connection_manager = ConnectionManager()
    connection_manager.add_sensor(sensor)
    enable_data_logging(sensor, odr=odr)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)

    elif args.timer_stream_mode:
        raise EvaluationKitException('Timer polling not yet implemented')

    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    connection_manager.disconnect()


if __name__ == '__main__':
    app_main()
