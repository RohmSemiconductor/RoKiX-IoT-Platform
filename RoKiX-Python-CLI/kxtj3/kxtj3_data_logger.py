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
KXTJ3 data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, POLARITY_DICT, CFG_POLARITY, CFG_SAD, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT, REG_POLL
from kx_lib.kx_data_logger import SingleChannelReader
from kxtj3.kxtj3_driver import KXTJ3Driver, r, b, m, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KXTJ3DataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = "ch!ax!ay!az"
    reg = r.KXTJ3_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in KXTJ3Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        if timer is None:
            timer = get_drdy_timer()

        'Sensor can only be connected to adapter logical int pin 1'
        assert pin_index in[None, 1]

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer)


def enable_data_logging(sensor,
                        odr=25,
                        max_range='2G',
                        lp_mode=False,
                        power_off_on=True,
                        int_number=None):

    LOGGER.info('enable_data_logging start')

    assert int_number in [None, 1]

    #
    # parameter validation
    #
    assert sensor.name in KXTJ3Driver.supported_parts
    assert max_range in e.KXTJ3_CTRL_REG1_GSEL.keys(), \
        'Invalid max_range value "{}". Valid values are {}'.format(
            max_range, e.KXTJ3_CTRL_REG1_GSEL.keys())

    assert lp_mode in [True, False],\
        'Invalid lp_mode value "{}". Valid values are {}'.format(
            lp_mode, [True, False])

    assert convert_to_enumkey(odr) in e.KXTJ3_DATA_CTRL_REG_OSA.keys(),\
        'Invalid odr value "{}". Valid values are {}'.format(
            odr, e.KXTJ3_DATA_CTRL_REG_OSA.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # select g-range
    sensor.set_range(e.KXTJ3_CTRL_REG1_GSEL[max_range])

    # resolution / power mode selection
    if lp_mode is True:
        # enable low current mode
        sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)
    else:
        # full resolution
        sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)

    # odr setting for data logging
    sensor.set_odr(e.KXTJ3_DATA_CTRL_REG_OSA[convert_to_enumkey(odr)])

    _intpin = 0
    if int_number is None:
        if evkit_config.drdy_function_mode == ADAPTER_GPIO1_INT:
            _intpin = 1

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
            sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEL)  # latched interrupt
            sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)   # enable interrrupt pin

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


class KXTJ3DataLogger(SingleChannelReader):
    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    l = KXTJ3DataLogger([KXTJ3Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KXTJ3DataStream)


if __name__ == '__main__':
    main()
