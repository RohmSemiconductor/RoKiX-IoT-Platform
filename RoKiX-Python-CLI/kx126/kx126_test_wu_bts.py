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
Example app for WakeUp/Back To Sleep  (WU and BTS) detection

WakeUp and Back sleep uses INT2 interrupt.
KX126 wakeup detection works always with +-8g range
"""

import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx_lib.kx_util import get_other_pin_index, get_datalogger_config, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, ACTIVE_HIGH, POLARITY_DICT, CFG_POLARITY

from kx126.kx126_driver import KX126Driver, r, b, m, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


# wake and sleep status
wakesleep_status = {
    0: 'Sleep',
    1: 'Wake'}

####
# threshold and counter values for wuf and bts
# example wakeup/back to sleep values (fast transitions)
# values for 2g and 12.5Hz odr for both OWUF and OBTS
# OSA (stream odr) = 25Hz (> OWUF & OBTS)


class Parameter_set_1: # pylint: disable=bad-whitespace

    WUF_THRESHOLD_VALUE = 260           # 3.9mg*value
    WUF_COUNTER_VALUE   = 2             # 1/OWUF*value
    BTS_THRESHOLD_VALUE = 200           # 3.9mg*value
    BTS_COUNTER_VALUE   = 4             # 1/OBTS*value
    LOW_POWER_MODE      = False
    lp_average          = '16_SAMPLE_AVG'
    odr_OSA             = 25
    odr_OWUF            = 12.5
    odr_OBTS            = 12.5


# wuf/bts direction axes masks
WUF_AXES = b.KX126_INC2_XNWUE | \
    b.KX126_INC2_XPWUE | \
    b.KX126_INC2_YNWUE | \
    b.KX126_INC2_YPWUE | \
    b.KX126_INC2_ZNWUE | \
    b.KX126_INC2_ZPWUE

# wuf directions source
wufbts_direction = {
    b.KX126_INS3_ZNWU: "FACE_UP",
    b.KX126_INS3_ZPWU: "FACE_DOWN",
    b.KX126_INS3_XNWU: "UP",
    b.KX126_INS3_XPWU: "DOWN",
    b.KX126_INS3_YPWU: "RIGHT",
    b.KX126_INS3_YNWU: "LEFT"}

SLEEP, WAKE = range(2)


class KX126WuBtsStream(StreamConfig):
    fmt = "<BBBB"
    hdr = "ch!ins3!status!int_rel"
    reg = r.KX126_INS3

    def __init__(self, sensors, pin_index=2, timer=None):
        assert sensors[0].name in KX126Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])
        assert not timer, 'Timer not supported in this data stream'

        # get pin_index if it is not given and timer is not used
        if pin_index is None and timer is None:
            pin_index = get_other_pin_index()

        assert pin_index in [1, 2], 'got %s' % pin_index

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index)


def wake_sleep(sensor, mode):                                   # select wake or sleep mode manually
    assert mode in [SLEEP, WAKE]
    if mode == WAKE:
        sensor.set_bit(r.KX126_CNTL5, b.KX126_CNTL5_MAN_WAKE)           # wait until wake setup bit released
        while sensor.read_register(r.KX126_CNTL5, 1)[0] & \
                b.KX126_CNTL5_MAN_WAKE != 0:
            pass    # wait until wake mode valid
        while sensor.read_register(r.KX126_STAT, 1)[0] & b.KX126_STAT_WAKE == 0:
            pass
        return
    elif mode == SLEEP:
        sensor.set_bit(r.KX126_CNTL5, b.KX126_CNTL5_MAN_SLEEP)          # wait until sleep setup bit released
        while sensor.read_register(r.KX126_CNTL5, 1)[0] & \
                b.KX126_CNTL5_MAN_SLEEP != 0:
            pass   # wait until sleep mode valid
        while sensor.read_register(r.KX126_STAT, 1)[0] & b.KX126_STAT_WAKE > 0:
            pass
        return


"""
def directions(dir):            # print wuf+bts source directions
    fst = True
    pos = None
    for i in range(0, 6):
        mask = 0x01 << i
        if dir & mask > 0:
            if not fst:
                pos = pos + "+" + wufbts_direction[dir & mask]
            else:
                pos = wufbts_direction[dir & mask]
                fst = False
    return pos
"""


def enable_wu_bts(sensor,
                  cfg=Parameter_set_1,
                  power_off_on=True):       # set to False if this function is part of other configuration

    LOGGER.info('Wakeup event init start')

    #
    # parameter validation
    #
    assert sensor.name in KX126Driver.supported_parts
    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
        'Invalid odr_OSA value "{}". Valid values are {}'.format(
            cfg.odr_OSA, e.KX126_ODCNTL_OSA.keys())

    assert convert_to_enumkey(cfg.odr_OWUF) in e.KX126_CNTL3_OWUF.keys(), \
        'Invalid odr_OWUF value "{}". Valid values are {}'.format(
            cfg.odr_OWUF, e.KX126_CNTL3_OWUF.keys())

    assert convert_to_enumkey(cfg.odr_OBTS) in e.KX126_CNTL4_OBTS.keys(), \
        'Invalid odr_OBTS value "{}". Valid values are {}'.format(
            cfg.odr_OBTS, e.KX126_CNTL4_OBTS.keys())

    assert cfg.LOW_POWER_MODE in [True, False],\
        'Invalid cfg.LOW_POWER_MODE value "{}". Valid values are {}'.format(
            cfg.LOW_POWER_MODE, [True, False])

    assert cfg.lp_average in e.KX126_LP_CNTL_AVC.keys(), \
        'Invalid lp_average value "{}". Valid values are {}'.format(
            cfg.lp_average, e.KX126_LP_CNTL_AVC.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()
    #
    # Configure sensor
    #
    # g-range is fixed +-8g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE:
        # low current
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)  # low current
        # set averaging (only for low power)
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])
    else:
        # full resolution
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)

    # enable wakeup detection engine
    sensor.set_bit(r.KX126_CNTL4, b.KX126_CNTL4_WUFE)                     # enable wuf
    sensor.set_bit(r.KX126_CNTL4, b.KX126_CNTL4_BTSE)                     # enable bts

    # stream odr (if stream odr is biggest odr, it makes effect to current consumption)

    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])

    #
    # Init wuf detection engine
    #

    sensor.write_register(r.KX126_WUFTH, cfg.WUF_THRESHOLD_VALUE & 0x0ff)
    sensor.write_register(r.KX126_BTSTH, cfg.BTS_THRESHOLD_VALUE & 0x0ff)
    msbs = ((cfg.BTS_THRESHOLD_VALUE & 0x700) >> 4) | ((cfg.WUF_THRESHOLD_VALUE & 0x700) >> 8)
    sensor.write_register(r.KX126_BTSWUFTH, msbs)
    sensor.write_register(r.KX126_WUFC, cfg.WUF_COUNTER_VALUE & 0x0ff)
    sensor.write_register(r.KX126_BTSC, cfg.BTS_COUNTER_VALUE & 0x0ff)

    # sensor.set_bit(r.KX126_CTL4, b.KX126_CTL4_TH_MODE) # relative threshold (jerk)
    # sensor.set_bit(r.KX126_CTL4, b.KX126_CTL4_C_MODE)   # debounce counter method (decreased)

    sensor.set_bit_pattern(r.KX126_CNTL3, e.KX126_CNTL3_OWUF[convert_to_enumkey(cfg.odr_OWUF)], m.KX126_CNTL3_OWUF_MASK)
    sensor.set_bit_pattern(r.KX126_CNTL4, e.KX126_CNTL4_OBTS[convert_to_enumkey(cfg.odr_OBTS)], m.KX126_CNTL4_OBTS_MASK)
    # change mode (manual)
    wake_sleep(sensor, WAKE)
    #wake_sleep(sensor, SLEEP)
    #
    # interrupt pin routings and settings
    #
    # interrupt signal parameters
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2)  # latched interrupt

    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity {}'.format(
        sensor.resource[CFG_POLARITY]))
    sensor.set_interrupt_polarity(intpin=2, polarity=polarity)

    # wakeup direction mask and occurence
    sensor.write_register(r.KX126_INC2, WUF_AXES)
    #sensor.set_bit(r.KX126_INC2, b.KX126_INC2_AOI_AND)
    sensor.reset_bit(r.KX126_INC2, b.KX126_INC2_AOI_OR)

    # interrupt pin routings and settings for wu and bts
    sensor.set_bit(r.KX126_INC6, b.KX126_INC6_WUFI2)            # wu to int 2
    sensor.set_bit(r.KX126_INC6, b.KX126_INC6_BTSI2)            # bts to int 2
    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)             # enable int2 pin

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on(CH_ACC)                                 # acc ON

    # sensor.register_dump()#sys.exit()

    LOGGER.info('enable_bts_wu done')


class KX126WuBtsDataLogger(SingleChannelEventReader):

    def enable_data_logging(self, **kwargs):
        enable_wu_bts(self.sensors[0], **kwargs)


def main():
    l = KX126WuBtsDataLogger([KX126Driver])
    l.enable_data_logging()
    l.run(KX126WuBtsStream)


if __name__ == '__main__':
    main()
