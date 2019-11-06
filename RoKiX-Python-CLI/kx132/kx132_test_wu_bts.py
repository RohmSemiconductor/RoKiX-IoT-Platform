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
KX132  Example app for WakeUp/Back To Sleep  (WU and BTS) detection
8G ADP datapath data used for WUFBTS detection. Filters and RMS are bypassed.

NOTE if ADP datapath used then this application will overwrite  raw data and ADP date settings!

"""

import imports  # pylint: disable=unused-import
import time
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_exception import ProtocolTimeoutException
from kx_lib.kx_util import get_drdy_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, CH_TEMP, CH_ADP, POLARITY_DICT, CFG_POLARITY, CFG_SAD, CFG_AXIS_MAP
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx132.kx132_driver import KX132Driver, r, b, m, e, SLEEP, WAKE, directions
from kx132 import kx132_raw_adp_logger

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
LOGGER.setLevel(kx_logger.INFO)  # uncomment this to get text printout of wuf/bts directions

WUF_AXES = b.KX132_1211_INC2_XNWUE | \
           b.KX132_1211_INC2_XPWUE | \
           b.KX132_1211_INC2_YNWUE | \
           b.KX132_1211_INC2_YPWUE | \
           b.KX132_1211_INC2_ZNWUE | \
           b.KX132_1211_INC2_ZPWUE


class KX132WuBtsStream(StreamConfig):
    fmt = "<BBBB"
    hdr = "ch!INS3!STATUS!INT_REL"
    reg = r.KX132_1211_INS3

    def __init__(self, sensors, pin_index=2, timer=None):
        StreamConfig.__init__(self, sensors[0])
        assert pin_index in [1, 2], 'got %s' % pin_index
        assert not timer, 'Timer not supported in this data stream'

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index)


class Parameter_set_1(object):
    WUF_THRESHOLD_VALUE = 20       # 3.9mg*value
    WUF_COUNTER_VALUE = 2         # 1/OWUF*value
    BTS_THRESHOLD_VALUE = 20       # 3.9mg*value
    BTS_COUNTER_VALUE = 2         # 1/OBTS*value
    AOI = b.KX132_1211_INC2_AOI_OR       # AND-OR configuration on motion detection : b.KX132_1211_INC2_AOI_OR / b.KX132_1211_INC2_AOI_AND
    PR_MODE = 0                     # Pulse rejection mode : 0 standard / 1 reject
    TH_MODE = 1                     # wake / back-to-sleep threshold mode : 0/1. 0=absolute, 1=relative
    C_MODE = 0                      # defines debounce counter clear mode : 0/1. 0=reset 1=decrement
    WUF_AXES = b.KX132_1211_INC2_XNWUE | \
               b.KX132_1211_INC2_XPWUE | \
               b.KX132_1211_INC2_YNWUE | \
               b.KX132_1211_INC2_YPWUE | \
               b.KX132_1211_INC2_ZNWUE | \
               b.KX132_1211_INC2_ZPWUE


def enable_wu_bts(sensor,
                  odr_owuf=12.5,
                  odr_bts=12.5,
                  cfg=Parameter_set_1,
                  ADP_WB_ISEL=0,  # 0=raw data to WUFBTS, 1=ADP data to WUFBTS
                  power_off_on=True):

    LOGGER.info('enable_wu_bts start')

    assert ADP_WB_ISEL in [0, 1]

    assert convert_to_enumkey(odr_owuf) in e.KX132_1211_CNTL3_OWUF.keys(), 'Invalid for odr_owuf value "{}". Valid values are {}'.format(
        convert_to_enumkey(odr_owuf), e.KX132_1211_CNTL3_OWUF.keys())

    assert convert_to_enumkey(odr_bts) in e.KX132_1211_CNTL4_OBTS.keys(), 'Invalid for odr_owuf value "{}". Valid values are {}'.format(
        convert_to_enumkey(odr_bts), e.KX132_1211_CNTL4_OBTS.keys())

    assert cfg.C_MODE in [0, 1], 'Invalid for C_MODE value "{}".'.format(cfg.C_MODE)

    if power_off_on:
        sensor.set_power_off()
        time.sleep(0.1)

    # Wakeup dircetion mask and occurence
    sensor.set_bit_pattern(
        r.KX132_1211_INC2,
        cfg.WUF_AXES | cfg.AOI,
        WUF_AXES | m.KX132_1211_INC2_AOI_MASK)

    # Interrupt pin routings and settings for wu and bts
    sensor.set_bit(r.KX132_1211_INC6, b.KX132_1211_INC6_WUFI2)    # wu to int2
    sensor.set_bit(r.KX132_1211_INC6, b.KX132_1211_INC6_BTSI2)    # bts to int2
    sensor.set_bit(r.KX132_1211_INC5, b.KX132_1211_INC5_IEN2)     # enable in2 pin
    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity {}'.format(
        sensor.resource[CFG_POLARITY]))
    sensor.set_interrupt_polarity(intpin=2, polarity=polarity)

    # Wakeup and back to sleep settings
    # Wakeup threshold and Back to sleep threshold are 10 bit values
    sensor.write_register(r.KX132_1211_WUFTH, cfg.WUF_THRESHOLD_VALUE & 0xff)
    sensor.write_register(r.KX132_1211_BTSTH, cfg.BTS_THRESHOLD_VALUE & 0xff)
    # Wakeup and back to sleep msb's
    bts_msb = ((cfg.BTS_THRESHOLD_VALUE >> 8) & 0x07) << 4
    wuf_msb = ((cfg.WUF_THRESHOLD_VALUE >> 8) & 0x07)
    sensor.write_register(r.KX132_1211_BTSWUFTH, bts_msb | wuf_msb)
    # Wakeup and back to sleep counters
    sensor.write_register(r.KX132_1211_WUFC, cfg.WUF_COUNTER_VALUE)
    sensor.write_register(r.KX132_1211_BTSC, cfg.BTS_COUNTER_VALUE)

    # Enable
    # NOTE () is mandatory on if else clause otherwise value evaluated incorectly
    sensor.write_register(
        r.KX132_1211_CNTL4,
        b.KX132_1211_CNTL4_WUFE |  # WUF enabled
        b.KX132_1211_CNTL4_BTSE |  # BTS enabled
        (b.KX132_1211_CNTL4_PR_MODE if cfg.PR_MODE else 0) |
        (b.KX132_1211_CNTL4_TH_MODE if cfg.TH_MODE else 0) |
        (b.KX132_1211_CNTL4_C_MODE_DECREMENTED if cfg.C_MODE else b.KX132_1211_CNTL4_C_MODE_RESET)
    )

    # print('a 0b{:08b}'.format((sensor.read_register(r.KX132_1211_CNTL4)[0])))

    # Wakeup odr
    sensor.set_bit_pattern(r.KX132_1211_CNTL3, e.KX132_1211_CNTL3_OWUF[convert_to_enumkey(odr_owuf)], m.KX132_1211_CNTL3_OWUF_MASK)
    # Back to sleep odr
    sensor.set_bit_pattern(r.KX132_1211_CNTL4, e.KX132_1211_CNTL4_OBTS[convert_to_enumkey(odr_bts)], m.KX132_1211_CNTL4_OBTS_MASK)

    # set Motion engine to wake mode
    sensor.set_bit(r.KX132_1211_CNTL5, b.KX132_1211_CNTL5_MAN_SLEEP)

    # route raw data or ADP data to WUFBTS
    if ADP_WB_ISEL:  # ADP data to Motion Engine
        # NOTE ADP must be enabled and configured separately kx132_raw_adp_logger.configure_adp()

        # route adp data to Motion engine (instead of raw data)
        sensor.set_bit(r.KX132_1211_ADP_CNTL2, b.KX132_1211_ADP_CNTL2_ADP_WB_ISEL)

        # ADP to WUF works only with RMS data
        sensor.set_bit(r.KX132_1211_ADP_CNTL2, b.KX132_1211_ADP_CNTL2_RMS_WB_OSEL)  # ADP RMS output data

    else:  # raw data to Motion Engine
        # route raw data to Motion engine (instead of ADP data)
        sensor.reset_bit(r.KX132_1211_ADP_CNTL2, b.KX132_1211_ADP_CNTL2_ADP_WB_ISEL)

    # Turn on operating mode (disables setup)
    if power_off_on:
        sensor.set_power_on(CH_ACC)
    sensor.register_dump_listed([r.KX132_1211_ADP_CNTL1])
    LOGGER.debug('enable_wu_bts done')
    # sensor.register_dump()
    # sys.exit()


def callback(data):
    ch, ins3, status, rel = data
    del ch, status, rel

    # convert bitvalue direction to text
    if ins3 & b.KX132_1211_INS3_BTS:
        LOGGER.info('Back to sleep')
    else:
        pos = directions(ins3 & WUF_AXES)
        LOGGER.info('Wake up {}'.format(pos))

    return True


def main():
    evkit_config.add_argument(
        '--use_adp',
        action='store_true',
        help='Routes adp data to wake up/back to sleep engine'
    )
    app = SingleChannelEventReader([KX132Driver])
    sensor = app.sensors[0]
    sensor.por()

    if evkit_config.use_adp:
        sensor.set_power_off()
        kx132_raw_adp_logger.enable_data_logging(
            sensor,
            odr=evkit_config.odr,
            max_range='2G',
            lp_mode='128_SAMPLE_AVG',
            low_pass_filter='BYPASS',
            filter1_setting=None,
            filter2_setting=None,
            adp_odr=evkit_config.odr,
            rms_average='2_SAMPLE_AVG',
            power_off_on=False)

        enable_wu_bts(
            sensor,
            ADP_WB_ISEL=1,
            odr_owuf=12.5,
            odr_bts=12.5,
            cfg=Parameter_set_1,
            power_off_on=False)  # ADP data to WUFBTS

        sensor.set_power_on(CH_ACC | CH_ADP)

    else:
        enable_wu_bts(
            sensor,
            ADP_WB_ISEL=0,
            odr_owuf=12.5,
            odr_bts=12.5,
            cfg=Parameter_set_1)  # raw data to WUFBTS

    app.run(KX132WuBtsStream, pin_index=2, reader_arguments={'callback': callback})


if __name__ == '__main__':
    main()
