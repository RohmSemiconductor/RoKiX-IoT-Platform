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
KX224 data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, POLARITY_DICT, CFG_POLARITY, CFG_SAD, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT, REG_POLL
from kx_lib.kx_data_logger import SingleChannelReader
from kx224.kx224_driver import KX224Driver, r, b, m, e


LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX224DataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = "ch!ax!ay!az"
    reg = r.KX224_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in KX224Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        if timer is None:
            timer = get_drdy_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer
        )


def enable_data_logging(sensor,
                        odr=25,
                        max_range='8G',
                        lp_mode=False,
                        low_pass_filter='ODR_9',
                        power_off_on=True,          # set to False if this function is part of other configuration
                        int_number=None):
    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert sensor.name in KX224Driver.supported_parts

    assert convert_to_enumkey(odr) in e.KX224_ODCNTL_OSA.keys(),\
        'Invalid odr value "{}". Valid values are {}'.format(
            odr, e.KX224_ODCNTL_OSA.keys())

    assert max_range in e.KX224_CNTL1_GSEL, \
        'Invalid max_range value "{}". Valid values are {}'.format(
            max_range, e.KX224_CNTL1_GSEL.keys())

    assert (lp_mode in list(e.KX224_LP_CNTL_AVC.keys()) +
            [False]), 'Invalid lp_mode value "{}". Valid values are: False or {}'.format(
                lp_mode, e.KX224_LP_CNTL_AVC.keys())

    assert low_pass_filter in list(e.KX224_ODCNTL_LPRO.keys()) + \
        ['BYPASS'], 'Invalid filter value "{}". Valid values are: BYPASS or {}'.format(
            filter, e.KX224_ODCNTL_LPRO.keys())

    # CNTL1 registers are configured first

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # select g-range
    sensor.set_range(e.KX224_CNTL1_GSEL[max_range])

    # resolution / power mode selection

    if lp_mode is not False:
        # enable low current mode
        sensor.reset_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)
        # define averaging value
        sensor.set_average(e.KX224_LP_CNTL_AVC[lp_mode])
    else:
        # full resolution
        sensor.set_bit(r.KX224_CNTL1, b.KX224_CNTL1_RES)

    # odr setting for data logging
    sensor.set_odr(e.KX224_ODCNTL_OSA[convert_to_enumkey(odr)])

    # set bandwitdh
    if low_pass_filter != 'BYPASS':
        sensor.set_BW(low_pass_filter, 0, CH_ACC)
        sensor.enable_iir()
    else:
        sensor.disable_iir()

    #
    # interrupt pin routings and settings
    #

    _intpin = 0
    if int_number is None:
        if evkit_config.drdy_function_mode == ADAPTER_GPIO1_INT:
            _intpin = 1

        elif evkit_config.drdy_function_mode == ADAPTER_GPIO2_INT:
            _intpin = 2

        elif evkit_config.drdy_function_mode == REG_POLL:
            # interrupt must be enabled to get register updates
            sensor.enable_drdy(intpin=1)

        else:
            pass  # TIMER_POLL no need to do anything

    else:
        _intpin = int_number

    if _intpin > 0:
        LOGGER.debug('Configuring interrupt pin {}'.format(_intpin))
        if _intpin == 1:
            # latched interrupt
            sensor.reset_bit(r.KX224_INC1, b.KX224_INC1_IEL1)
            # enable interrupt
            sensor.set_bit(r.KX224_INC1, b.KX224_INC1_IEN1)
        else:
            # latched interrupt
            sensor.reset_bit(r.KX224_INC5, b.KX224_INC5_IEL2)
            # enable interrupt
            sensor.set_bit(r.KX224_INC5, b.KX224_INC5_IEN2)

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
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('enable_data_logging done')


class KX224DataLogger(SingleChannelReader):
    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    l = KX224DataLogger([KX224Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX224DataStream)


if __name__ == '__main__':
    main()
