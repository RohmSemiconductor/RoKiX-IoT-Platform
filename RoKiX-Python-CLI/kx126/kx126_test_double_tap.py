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
Example app for basic taptap detection

Double tap uses interrupt int1
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY
from kx_lib.kx_util import get_other_pin_index, convert_to_enumkey
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx126.kx126_driver import KX126Driver, r, b, m, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


#############################################
class Parameter_set_1: # pylint: disable=bad-whitespace
    # Tap sensitivity for 400Hz, no averaging (Normal power)
    LOW_POWER_MODE      = False
    odr_OSA             = 25
    odr_OTDT            = 400
    lp_average          = '16_SAMPLE_AVG'
    TAP_TTL             = [0x7E, 0x46, 0x2A]                #
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ### tap values              # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTRC_VALUE   = 0x02
    KX126_TDTC_VALUE    = 0x78  # 0x78  #       #       #       #           # timer value 1/400Hz, 2,5ms tick => 0,3s
    KX126_TTH_VALUE     = 0xCB  # 0xCB  #       #       #       #           # threshold high (0,0078) 3.08g in 4g range
    KX126_TTL_VALUE     = TAP_TTL[SENSITIVITY]       
                                # 0x2A  #       #       #       #           # threshold low (0.81g in 4g range)
    KX126_FTD_VALUE     = 0xA2  # 0xA2  #       #       #       #           # timer (default A2h) (0.025s, 2.5ms tick)
    KX126_STD_VALUE     = 0x24  # 0x24  #       #       #       #           # time (default 24h) (0.09s, 2.5ms tick) - TTL
    KX126_TLT_VALUE     = 0x28  # 0x28  #       #       #       #           # timer(default 28h) (0.1s, 2.5ms)
    KX126_TWS_VALUE     = 0xA0  # 0xA0  #       #       #       #           # time (default A0h) (0.4s, 2.5ms)

#############################################
class Parameter_set_2: # pylint: disable=bad-whitespace
    # Tap sensitivity for 2g, 100Hz, 2sample average (light hand, low power)
    LOW_POWER_MODE      = True
    odr_OSA             = 25
    odr_OTDT            = 100
    lp_average          = '2_SAMPLE_AVG'
    TAP_TTL             = [0xA4, 0x92, 0x82]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity

    ## light tap values        # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTRC_VALUE = 0x02
    KX126_TDTC_VALUE    = 0x0B  #       #       # 0x0E  #       #
    KX126_TTH_VALUE     = 0xEB  #       #       # 0xEB  #       #
    KX126_TTL_VALUE     = TAP_TTL[SENSITIVITY]
                                      #       # 0x82  #       #
    KX126_FTD_VALUE     = 0x15  #       #       # 0x15  #       #
    KX126_STD_VALUE     = 0x12  #       #       # 0x12  #       #
    KX126_TLT_VALUE     = 0x09  #       #       # 0x09  #       #
    KX126_TWS_VALUE     = 0x22  #       #       # 0x22  #       #
class Parameter_set_3: # pylint: disable=bad-whitespace
    # alternate settings for heavy hand #######
    # Tap sensitivity for 4g, 100Hz, 1 sample average (heavy hand, low power)
    LOW_POWER_MODE      = True
    odr_OSA             = 25
    odr_OTDT            = 100
    lp_average          = 'NO_AVG'
    TAP_TTL             = [0xB4, 0xA2, 0x92]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    # tap values                                            400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX126_TDTRC_VALUE = 0x02
    KX126_TDTC_VALUE = 0x1E                # timer value    0x78  # 0x3C  # 0x1E  # 0x11  # 0x0D
    KX126_TTH_VALUE  = 0xDB                # threshold high 0xCB  # 0xDB  # 0xDB  # 0xDB  # 0xDB
    KX126_TTL_VALUE  = TAP_TTL[SENSITIVITY]
                                           # threshold low  0xA2  # 0xA2  # 0x92  # 0x52  # 0x42
    KX126_FTD_VALUE  = 0x17                # timer          0x2A  # 0x19  # 0x17  # 0x15  # 0x02
    KX126_STD_VALUE  = 0x12                # timer          0x24  # 0x1A  # 0x12  # 0x05  # 0x03
    KX126_TLT_VALUE  = 0x0b                # timer          0x28  # 0x1F  # 0x0B  # 0x06  # 0x04
    KX126_TWS_VALUE  = 0x28                # timer          0xA0  # 0x50  # 0x28  # 0x13  # 0x0C

# native / rotated directions
resultResolverToString = {
    b.KX126_INS1_TLE:  "x-",
    b.KX126_INS1_TRI:  "x+",
    b.KX126_INS1_TDO:  "y-",
    b.KX126_INS1_TUP:  "y+",
    b.KX126_INS1_TFD:  "z-",
    b.KX126_INS1_TFU:  "z+"}

##########################################
# Enabler methods for asic features


class KX126DoubleTapStream(StreamConfig):
    fmt = "BBBBBB"
    hdr = "ch!ins1!ins2!na!stat!int_rel"
    reg = r.KX126_INS1

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


def enable_double_tap(sensor,
                      cfg=Parameter_set_1,
                      int_number=2,
                      power_off_on=True):

    LOGGER.info('Double tap event init start')

    #
    # parameter validation
    #

    assert cfg.LOW_POWER_MODE in [True, False],\
        'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
            cfg.LOW_POWER_MODE, [True, False])

    assert cfg.lp_average in e.KX126_LP_CNTL_AVC.keys(), \
        'Invalid lp_average value "{}". Valid values are {}'.format(
            cfg.lp_average, e.KX126_LP_CNTL_AVC.keys())

    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
        'Invalid odr_OSA value "{}". Valid values are {}'.format(
            cfg.odr_OSA, e.KX126_ODCNTL_OSA.keys())

    assert convert_to_enumkey(cfg.odr_OTDT) in e.KX126_CNTL3_OTDT.keys()
    'Invalid odr_OTDT value "{}". Valid values are {}'.format(
        cfg.odr_OTDT, e.KX126_CNTL3_OTDT.keys())

    assert int_number in [1, 2]
    # Sensor set to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()                          # this sensor request PC=0 to PC=1 before valid settingsSet sensor to stand-by to enable setup change

    #
    # Configure sensor
    #
    # g-range is fixed +-4g

    # resolution / power mode selection
    # Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)
    if cfg.LOW_POWER_MODE:
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                          # low current
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])                     # lowest current mode average
    else:
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                            # high resolution

    # Set double tap bit on
    sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_TDTE)

    # Set tap odr
    sensor.write_register(r.KX126_CNTL3, 0)         # all odrs to minimum first
    sensor.set_bit_pattern(r.KX126_CNTL3, e.KX126_CNTL3_OTDT[convert_to_enumkey(cfg.odr_OTDT)], m.KX126_CNTL3_OTDT_MASK)

    # stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])

    #
    # Init tap detection engine
    #

    # Init tap directions
    sensor.write_register(r.KX126_INC3, 0)          # all off, default is all on
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TLEM)  # x- left set
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TRIM)  # x+ right set
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TDOM)  # y- back set
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TUPM)  # y+ front set
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TFDM)  # z- down set
    sensor.set_bit(r.KX126_INC3, b.KX126_INC3_TFUM)  # z+ up set

    # Disable/enable single tap and double tap interrupt
    sensor.write_register(r.KX126_TDTRC, cfg.KX126_TDTRC_VALUE)


    # TDTC: Counter information for the detection of a double tap event. 1/400Hz (0.3s, 2.5ms)
    sensor.write_register(r.KX126_TDTC, cfg.KX126_TDTC_VALUE)

    # TTH: High threshold jerk value for tap functions
    sensor.write_register(r.KX126_TTH, cfg.KX126_TTH_VALUE)

    # TTL: Low threshold jerk value for tap functions
    sensor.write_register(r.KX126_TTL, cfg.KX126_TTL_VALUE)

    # FTD: Timer settings for tap signal.
    sensor.write_register(r.KX126_FTD, cfg.KX126_FTD_VALUE)

    # STD: Timer for two taps signal above threshold
    sensor.write_register(r.KX126_STD, cfg.KX126_STD_VALUE)

    # TLT: Timer calculates samples above threshold
    sensor.write_register(r.KX126_TLT, cfg.KX126_TLT_VALUE)

    # TWS: TImer for tap function event
    sensor.write_register(r.KX126_TWS, cfg.KX126_TWS_VALUE)

    # interrupt pin routings and settings
    # interrupt signal parameters
    sensor.reset_bit(r.KX126_INC1, b.KX126_INC1_IEL1)  # latched interrupt

    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity {}'.format(
        sensor.resource[CFG_POLARITY]))

    sensor.set_interrupt_polarity(intpin=int_number, polarity=polarity)

    if int_number == 1:
        sensor.set_bit(r.KX126_INC4, b.KX126_INC4_TDTI1)     # double tap to int1
        sensor.set_bit(r.KX126_INC1, b.KX126_INC1_IEN1)       # enable int1 pin
    else:
        sensor.set_bit(r.KX126_INC6, b.KX126_INC6_TDTI2)     # double tap to int2
        sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)       # enable int2 pin

    #
    # Turn on operating mode (disables setup)
    #
    if power_off_on:
        sensor.set_power_on()                               # settings coming to valid and start measurements

    # sensor.register_dump()

    LOGGER.info('\nDouble tap event initialized.')

    sensor.release_interrupts()                         # clear all internal function interrupts




def determine_double_tap_direction(data):
    # channel, ins1, ins2, NA, status, rel = data
    _, ins1, _, _, _, _ = data
    print('Double tap direction: ' + resultResolverToString[ins1])
    return True  # Continue reading


class KX126DoubleTapLogger(SingleChannelEventReader):

    def enable_data_logging(self, **kwargs):
        enable_double_tap(self.sensors[0], **kwargs)


def main():
    app = KX126DoubleTapLogger([KX126Driver])
    app.enable_data_logging()
    app.run(KX126DoubleTapStream, reader_arguments={'callback': determine_double_tap_direction, 'console': True})


if __name__ == '__main__':
    main()
