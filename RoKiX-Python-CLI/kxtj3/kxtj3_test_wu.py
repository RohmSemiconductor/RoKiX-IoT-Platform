# The MIT License (MIT)
#
# Copyright (c) 2020 Rohm Semiconductor
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
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx_lib.kx_util import evkit_config, convert_to_enumkey, CH_ACC, get_other_pin_index, get_other_timer
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT

from kxtj3.kxtj3_driver import KXTJ3Driver
from kxtj3.kxtj3_driver import r, b, e, m

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.INFO) # Use this debug level to get "human readable" information of wake-up directions
# LOGGER.setLevel(kx_logger.INFO)


class Parameter_set_1(object):
    # low power, low odr
    LOW_POWER_MODE = True           # low power or full resolution mode
    WUFC_VALUE = 0x00               # wakeup control timer
    ATH_VALUE = 0xa0                # threshold for wakeup
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
    b.KXTJ3_INT_SOURCE2_XNWU: "x-",
    b.KXTJ3_INT_SOURCE2_XPWU: "x+",
    b.KXTJ3_INT_SOURCE2_YNWU: "y-",
    b.KXTJ3_INT_SOURCE2_YPWU: "y+",
    b.KXTJ3_INT_SOURCE2_ZNWU: "z-",
    b.KXTJ3_INT_SOURCE2_ZPWU: "z+"}


def wu_bits_to_str(int_source2):
    "Convert content of int_source2 register to movement directions"
    direction_list = []
    for i in range(0, 6):
        j = 0x01 << i
        if int_source2 & j > 0:
            direction_list.append(resultResolverToString[j])

    return ' '.join(direction_list)


def determine_wu_direction(data):
    channel, int_source1, int_source2, status_reg, NA, rel = data
    print ('WAKEUP DETECTION streming mode:'+wu_bits_to_str(int_source2))
    return True  # Continue reading
    
class KXTJ3WuStream(StreamConfig):
    fmt = "<BBBBBB"
    hdr = "ch!INS1!INS2!STATUS!NA!INT_REL"
    reg = r.KXTJ3_INT_SOURCE1

    def __init__(self, sensors, pin_index=1, timer=None):
        assert sensors[0].name in KXTJ3Driver.supported_parts
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
                  direction_mask=b.KXTJ3_INT_CTRL_REG2_XNWU |      # x- direction mask
                  b.KXTJ3_INT_CTRL_REG2_XPWU |      # x+ direction mask
                  b.KXTJ3_INT_CTRL_REG2_YNWU |      # y- direction mask
                  b.KXTJ3_INT_CTRL_REG2_YPWU |      # y+ direction mask
                  b.KXTJ3_INT_CTRL_REG2_ZNWU |      # z- direction mask
                  b.KXTJ3_INT_CTRL_REG2_ZPWU,       # z+ direction mask
                  cfg=Parameter_set_1,
                  power_off_on=True       # set to False if this function is part of other configuration
                  ):

    LOGGER.info('Wakeup event init start')

    #
    # parameter validation
    #

    assert convert_to_enumkey(cfg.odr) in e.KXTJ3_DATA_CTRL_REG_OSA.keys(),\
    'Invalid odr value "{}". Valid values are {}'.format(
    cfg.odr,e.KXTJ3_DATA_CTRL_REG_OSA.keys())
    
    assert cfg.LOW_POWER_MODE in [True, False],\
    'Invalid cfg.LOW_POWER_MODE value "{}". Valid values are True and False'.format(
    cfg.LOW_POWER_MODE)

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
        sensor.reset_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)
    else:
        # full resolution
        sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_RES)

    # enable wakeup detection engine
    sensor.set_bit(r.KXTJ3_CTRL_REG1, b.KXTJ3_CTRL_REG1_WUFE)
    # stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KXTJ3_DATA_CTRL_REG_OSA[convert_to_enumkey(cfg.odr)])
    # Set wuf detection odr
    sensor.set_bit_pattern(r.KXTJ3_CTRL_REG2,
                           e.KXTJ3_CTRL_REG2_OWUF[convert_to_enumkey(cfg.odr)],
                           m.KXTJ3_CTRL_REG2_OWUF_MASK)

    #
    # Init wuf detection engine
    #

    # WUF direction definition
    sensor.write_register(r.KXTJ3_INT_CTRL_REG2, direction_mask)
    # WUF timer
    sensor.write_register(r.KXTJ3_WAKEUP_THRESHOLD_H, cfg.ATH_VALUE >> 4)
    sensor.write_register(r.KXTJ3_WAKEUP_THRESHOLD_L, cfg.ATH_VALUE & 0xf << 4)
    # WUF threshold
    sensor.write_register(r.KXTJ3_WAKEUP_COUNTER, cfg.WUFC_VALUE)

    #
    # interrupt pin routings and settings
    #

    # enable interrrupt pin
    sensor.set_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEN)

    # latched interrupt
    sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1, b.KXTJ3_INT_CTRL_REG1_IEL)
    if evkit_config.get('generic', 'int1_active_high') == 'TRUE':
        sensor.set_bit(r.KXTJ3_INT_CTRL_REG1,
                       b.KXTJ3_INT_CTRL_REG1_IEA)  # active high
    else:
        sensor.reset_bit(r.KXTJ3_INT_CTRL_REG1,
                         b.KXTJ3_INT_CTRL_REG1_IEA)  # active low

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('Wakeup event initialized.')



class KXTJ3WUDataLogger(SingleChannelEventReader):

    def enable_data_logging(self, **kwargs):
        enable_wakeup(self.sensors[0], **kwargs)


class KXTJ3Driver_wu(KXTJ3Driver):

    def read_drdy(self, intpin=None, channel=None):
        # if using "stream_mode = False" then the read_drdy() must be overriden
        # and monitor WUFS instead of DRDY
        return self.read_register(r.KXTJ3_INT_SOURCE1)[0] & b.KXTJ3_INT_SOURCE1_WUFS != 0


def main():
    # overwrite rokix_settings since sensor has only int1
    evkit_config.set('other_function_mode', 'ADAPTER_GPIO1_INT')

    l = KXTJ3WUDataLogger([KXTJ3Driver_wu])
    l.enable_data_logging()
    l.run(
        KXTJ3WuStream, 
        reader_arguments={
            'callback': determine_wu_direction, 
            'console': True})


if __name__ == '__main__':
    main()