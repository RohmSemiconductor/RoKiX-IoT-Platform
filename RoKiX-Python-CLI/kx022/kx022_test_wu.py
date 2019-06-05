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
Wakeup demonstration
For KX022 wakeup detection works always with +-8g range
"""
import struct

import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_exception import ProtocolTimeoutException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx_lib.kx_util import evkit_config, convert_to_enumkey, CH_ACC, get_other_pin_index, get_other_timer
from kx_lib.kx_configuration_enum import ACTIVE_HIGH, POLARITY_DICT, CFG_POLARITY, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT

from kx022.kx022_driver import KX022Driver
from kx022.kx022_driver import r, b, e, m, r122, b122, e122, m122

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.INFO) # Use this debug level to get "human readable" information of wake-up directions
# LOGGER.setLevel(kx_logger.INFO)


class Parameter_set_1(object):
    # low power, low odr
    LOW_POWER_MODE = True           # low power or full resolution mode
    WUFC_VALUE = 0x00               # wakeup control timer
    ATH_VALUE = 0x0a                # threshold for wakeup
    odr = 3.125                     # ODR for sensor
    lp_average = '16_SAMPLE_AVG'   # how many samples averaged in low power mode


class Parameter_set_2(object):
    # low power, max odr
    LOW_POWER_MODE = True           # low power or full resolution mode
    WUFC_VALUE = 0                  # wakeup control timer
    ATH_VALUE = 10                  # threshold for wakeup
    odr = 12.5                       # ODR for sensor
    lp_average = 'NO_AVG'           # how many samples averaged in low power mode


# native / rotated directions
resultResolverToString = {
    b.KX022_INS3_XNWU: "x-",
    b.KX022_INS3_XPWU: "x+",
    b.KX022_INS3_YNWU: "y-",
    b.KX022_INS3_YPWU: "y+",
    b.KX022_INS3_ZNWU: "z-",
    b.KX022_INS3_ZPWU: "z+"}


def wu_bits_to_str(ins3):
    "Convert content of ins3 register to movement directions"
    direction_list = []
    for i in range(0, 6):
        j = 0x01 << i
        if ins3 & j > 0:
            direction_list.append(resultResolverToString[j])

    return ' '.join(direction_list)


def determine_wu_direction(data):
    _, _, _, ins3, _, _, _ = data
    LOGGER.info('Wakeup Direction: %s' % wu_bits_to_str(ins3))
    return True  # Continue reading


class KX022WuStream(StreamConfig):
    fmt = "<BBBBBBB"
    hdr = "ch!INS1!INS2!INS3!STATUS!NA!INT_REL"
    reg = r.KX022_INS1

    def __init__(self, sensors, pin_index=None, timer=None):
        assert sensors[0].name in KX022Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        if pin_index is None:
            pin_index = get_other_pin_index()

        if timer is None:
            timer = get_other_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer)


def enable_wakeup(sensor,
                  direction_mask=b.KX022_INC2_XNWUE |      # x- direction mask
                  b.KX022_INC2_XPWUE |      # x+ direction mask
                  b.KX022_INC2_YNWUE |      # y- direction mask
                  b.KX022_INC2_YPWUE |      # y+ direction mask
                  b.KX022_INC2_ZNWUE |      # z- direction mask
                  b.KX022_INC2_ZPWUE,      # z+ direction mask
                  cfg=Parameter_set_1,
                  power_off_on=True):       # set to False if this function is part of other configuration

    LOGGER.info('Wakeup event init start')

    #
    # parameter validation
    #
    assert sensor.name in KX022Driver.supported_parts

    assert convert_to_enumkey(cfg.odr) in e.KX022_ODCNTL_OSA.keys(),\
        'Invalid odr value "{}". Valid values are {}'.format(cfg.odr, e.KX022_ODCNTL_OSA.keys())

    assert convert_to_enumkey(cfg.odr) in e.KX022_CNTL3_OWUF.keys(),\
        'Invalid odr value "{}". Valid values are {}'.format(cfg.odr, e.KX022_CNTL3_OWUF.keys())

    assert cfg.lp_average in e.KX022_LP_CNTL_AVC.keys(),\
        'Invalid lp_average value "{}". Valid values are {}'.format(cfg.lp_average, e.KX022_LP_CNTL_AVC.keys())

    assert cfg.LOW_POWER_MODE in [True, False],\
        'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(cfg.LOW_POWER_MODE, [True, False])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
    #
    # Configure sensor
    #

    # NOTE for wake up detection the g-range is fixed to +-8g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # low current
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)
        # set averaging (only for low power)
        sensor.set_average(e.KX022_LP_CNTL_AVC[cfg.lp_average])
    else:
        # full resolution
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)

    # enable wakeup detection engine
    sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_WUFE)
    # stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KX022_ODCNTL_OSA[convert_to_enumkey(cfg.odr)])
    # Set wuf detection odr
    sensor.set_bit_pattern(r.KX022_CNTL3,
                           e.KX022_CNTL3_OWUF[convert_to_enumkey(cfg.odr)],
                           m.KX022_CNTL3_OWUF_MASK)

    #
    # Init wuf detection engine
    #

    # WUF direction definition
    sensor.write_register(r.KX022_INC2, direction_mask)
    # WUF timer
    sensor.write_register(r.KX022_WUFC, cfg.WUFC_VALUE)
    # WUF threshold
    sensor.write_register(r.KX022_ATH, cfg.ATH_VALUE)

    if sensor.name == 'KX122':
        # additional setting for KX122, select one of below options
        sensor.set_bit_pattern(r122.KX122_INC2, e122.KX122_INC2_AOI[
            'OR'], m122.KX122_INC2_AOI_MASK)  # (POR default value)
        #sensor.set_bit_pattern(r122.KX122_INC2, e122.KX122_INC2_AOI['AND'], m122.KX122_INC2_AOI_MASK)

    #
    # interrupt pin routings and settings
    #
    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    if evkit_config.other_function_mode == ADAPTER_GPIO1_INT:
        sensor.set_interrupt_polarity(intpin=1, polarity=polarity)
        # enable wakeup detection to int1
        sensor.set_bit(r.KX022_INC4, b.KX022_INC4_WUFI1)
        # latched interrupt for int1
        sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)
        # enable int1 pin
        sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEN1)

    elif evkit_config.other_function_mode == ADAPTER_GPIO2_INT:
        sensor.set_interrupt_polarity(intpin=2, polarity=polarity)
        # enable wakeup detection to int2
        sensor.set_bit(r.KX022_INC6, b.KX022_INC6_WUFI2)
        # latched interrupt for int2
        sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)
        # enable int2 pin
        sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEN2)
    else:
        pass  # TIMER_POLL or REG_POLL
    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on(CH_ACC)

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('Wakeup event initialized.')


class KX022WUDataLogger(SingleChannelEventReader):

    def enable_data_logging(self, **kwargs):
        enable_wakeup(self.sensors[0], **kwargs)


class KX022Driver_wu(KX022Driver):

    def read_drdy(self, intpin=None, channel=None):
        # if using "stream_mode = False" then the read_drdy() must be overriden
        # and monitor INS2/WUFS instead of INS2/DRDY
        return self.read_register(r.KX022_INS2)[0] & b.KX022_INS2_WUFS != 0


def main():
    l = KX022WUDataLogger([KX022Driver_wu])
    l.enable_data_logging()
    l.run(KX022WuStream, reader_arguments={'callback': determine_wu_direction, 'console': True})


if __name__ == '__main__':
    main()
