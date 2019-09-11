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
Double tap detection.
For KX022 double tap detection works always with +-4g range
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx_lib.kx_util import evkit_config, convert_to_enumkey, get_other_pin_index, get_other_timer
from kx_lib.kx_configuration_enum import ACTIVE_HIGH, ACTIVE_LOW

from kx022.kx022_driver import KX022Driver
from kx022.kx022_driver import r, b, e, m

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)


class ParameterSet1:
    """Tap sensitivity for 400Hz, no averaging (Normal power)"""
    # pylint: disable=bad-whitespace
    TAP_TTL             = [0x7E, 0x46, 0x2A]                #
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ### tap values              # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX022_TDTRC_VALUE = 0x02
    KX022_TDTC_VALUE    = 0x78  # 0x78  #       #       #       #           # timer value 1/400Hz, 2,5ms tick => 0,3s
    KX022_TTH_VALUE     = 0xCB  # 0xCB  #       #       #       #           # threshold high (0,0078) 3.08g in 4g range
    KX022_TTL_VALUE     = TAP_TTL[SENSITIVITY]
                                # 0x2A  #       #       #       #           # threshold low (0.81g in 4g range)
    KX022_FTD_VALUE     = 0xA2  # 0xA2  #       #       #       #           # timer (default A2h) (0.025s, 2.5ms tick)
    KX022_STD_VALUE     = 0x24  # 0x24  #       #       #       #           # time (default 24h) (0.09s, 2.5ms tick) - TTL
    KX022_TLT_VALUE     = 0x28  # 0x28  #       #       #       #           # timer(default 28h) (0.1s, 2.5ms)
    KX022_TWS_VALUE     = 0xA0  # 0xA0  #       #       #       #           # time (default A0h) (0.4s, 2.5ms)
    odr_OTDT            = 400
    odr_OSA             = 400
    LOW_POWER_MODE      = False                                             # low power or full resolution mode
    lp_average          = '16_SAMPLE_AVG'                                 # how many samples averaged in low power mode

class ParameterSet2:
    """Tap sensitivity for 2g, 100Hz, 2sample average (light hand, low power)"""
    # pylint: disable=bad-whitespace
    TAP_TTL             = [0xA4, 0x92, 0x82]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    # light tap values        # 400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX022_TDTRC_VALUE = 0x02
    KX022_TDTC_VALUE    = 0x0B  #       #       # 0x0E  #       #
    KX022_TTH_VALUE     = 0xEB  #       #       # 0xEB  #       #
    KX022_TTL_VALUE     = TAP_TTL[SENSITIVITY]
                                #       #       # 0x82  #       #
    KX022_FTD_VALUE     = 0x15  #       #       # 0x15  #       #
    KX022_STD_VALUE     = 0x12  #       #       # 0x12  #       #
    KX022_TLT_VALUE     = 0x09  #       #       # 0x09  #       #
    KX022_TWS_VALUE     = 0x22  #       #       # 0x22  #       #
    odr_OTDT            = 100
    odr_OSA             = 100
    LOW_POWER_MODE      = True                                  # low power or full resolution mode
    lp_average          = '2_SAMPLE_AVG'                        # how many samples averaged in low power mode

class ParameterSet3:
    """Tap sensitivity for 4g, 100Hz, 1 sample average (heavy hand, low power)"""
    # pylint: disable=bad-whitespace
    TAP_TTL             = [0xB4, 0xA2, 0x92]                # low, middle or high sensitivity
    SENSITIVITY         = 2 # 0 for low, 1 = middle and 2 = high sensitivity
    ## low power
    ## tap values                                            400Hz # 200Hz # 100Hz # 50Hz  # 25Hz
    KX022_TDTRC_VALUE   = 0x02
    KX022_TDTC_VALUE = 0x1E                # timer value    0x78  # 0x3C  # 0x1E  # 0x11  # 0x0D
    KX022_TTH_VALUE  = 0xDB                # threshold high 0xCB  # 0xDB  # 0xDB  # 0xDB  # 0xDB
    KX022_TTL_VALUE  = TAP_TTL[SENSITIVITY]
                                            # threshold low  0xA2  # 0xA2  # 0x92  # 0x52  # 0x42
    KX022_FTD_VALUE  = 0x17                # timer          0x2A  # 0x19  # 0x17  # 0x15  # 0x02
    KX022_STD_VALUE  = 0x12                # timer          0x24  # 0x1A  # 0x12  # 0x05  # 0x03
    KX022_TLT_VALUE  = 0x0b                # timer          0x28  # 0x1F  # 0x0B  # 0x06  # 0x04
    KX022_TWS_VALUE  = 0x28                # timer          0xA0  # 0x50  # 0x28  # 0x13  # 0x0C
    odr_OTDT            = 100
    odr_OSA             = 100
    LOW_POWER_MODE      = True                                          # low power or full resolution mode
    lp_average          = 'NO_AVG'                                   # how many samples averaged in low power mode

# native / rotated directions
RESULT_TO_STRING_MAP = {
    b.KX022_INS1_TLE: "x-",
    b.KX022_INS1_TRI: "x+",
    b.KX022_INS1_TDO: "y-",
    b.KX022_INS1_TUP: "y+",
    b.KX022_INS1_TFD: "z-",
    b.KX022_INS1_TFU: "z+",
}


def enable_double_tap(sensor,
                      direction_mask=None,
                      cfg=ParameterSet1,
                      int_pin=2,
                      power_off_on=True):  # set to False if this function is part of other configuration
    if direction_mask is None:
        direction_mask = (b.KX022_INC3_TLEM  # x- left set
                          | b.KX022_INC3_TRIM  # x+ right set
                          | b.KX022_INC3_TDOM  # y- back set
                          | b.KX022_INC3_TUPM  # y+ front set
                          | b.KX022_INC3_TFDM  # z- down set
                          | b.KX022_INC3_TFUM)  # z+ up set


    LOGGER.info('Double tap event init start')

    #
    # parameter validation
    #

    assert int_pin in [1, 2]

    assert convert_to_enumkey(cfg.odr_OSA) in e.KX022_ODCNTL_OSA.keys(), \
        'Invalid odr_OSA value "{}". Valid values are {}'.format(
            cfg.odr_OSA, e.KX022_ODCNTL_OSA.keys())

    assert convert_to_enumkey(cfg.odr_OTDT) in e.KX022_CNTL3_OTDT.keys(), \
        'Invalid odr_OTDT value "{}". Valid values are {}'.format(
            cfg.odr_OTDT, e.KX022_CNTL3_OTDT.keys())

    assert cfg.lp_average in e.KX022_LP_CNTL_AVC.keys(), \
        'Invalid lp_average value "{}". Valid values are {}'.format(
            cfg.lp_average, e.KX022_LP_CNTL_AVC.keys())

    assert cfg.LOW_POWER_MODE in [True, False], \
        'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
            cfg.LOW_POWER_MODE, [True, False])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # g-range is fixed +-4g

    # resolution / power mode selection
    if cfg.LOW_POWER_MODE is True:
        # Low power mode
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)
        # set averaging (only for low power)
        sensor.set_average(e.KX022_LP_CNTL_AVC[cfg.lp_average])
    else:
        # Full power mode
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)

    ## Set double tap bit on
    sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_TDTE)

    # Set tap detection odr
    new_otdt = e.KX022_CNTL3_OTDT[convert_to_enumkey(cfg.odr_OTDT)]
    sensor.set_bit_pattern(r.KX022_CNTL3, new_otdt, m.KX022_CNTL3_OTDT_MASK)

    # stream odr (if stream odr is biggest odr, it makes effect to current
    # consumption)
    sensor.set_odr(e.KX022_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])

    #
    # Init tap detection engine
    #

    # tap direction definition
    sensor.write_register(r.KX022_INC3, direction_mask)

    # Disable single tap and enable double tap interrupt
    sensor.write_register(r.KX022_TDTRC, cfg.KX022_TDTRC_VALUE)

    # TDTC: Counter information for the detection of a double tap event.
    # 1/400Hz (0.3s, 2.5ms)
    sensor.write_register(r.KX022_TDTC, cfg.KX022_TDTC_VALUE)

    # TTH: High threshold jerk value for tap functions
    sensor.write_register(r.KX022_TTH, cfg.KX022_TTH_VALUE)

    # TTL: Low threshold jerk value for tap functions
    sensor.write_register(r.KX022_TTL, cfg.KX022_TTL_VALUE)

    # FTD: Timer settings for tap signal.
    sensor.write_register(r.KX022_FTD, cfg.KX022_FTD_VALUE)

    # STD: Timer for two taps signal above threshold
    sensor.write_register(r.KX022_STD, cfg.KX022_STD_VALUE)

    # TLT: Timer calculates samples above threshold
    sensor.write_register(r.KX022_TLT, cfg.KX022_TLT_VALUE)

    # TWS: TImer for tap function event
    sensor.write_register(r.KX022_TWS, cfg.KX022_TWS_VALUE)

    #
    # interrupt pin routings and settings
    #

    if evkit_config.get('generic', 'int2_active_high') == 'TRUE':
        sensor.set_interrupt_polarity(intpin=int_pin, polarity=ACTIVE_HIGH)
    else:
        sensor.set_interrupt_polarity(intpin=int_pin, polarity=ACTIVE_LOW)

    if int_pin == 1:
        # enable double tap detection to int1
        sensor.set_bit(r.KX022_INC4, b.KX022_INC4_TDTI1)
        # latched interrupt 1
        sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)
        # enable int1 pin
        sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEN1)

    else:  # int_pin==2
        # enable double tap detection to int2
        sensor.set_bit(r.KX022_INC6, b.KX022_INC6_TDTI2)
        # latched interrupt 2
        sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)
        # enable int2 pin
        sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEN2)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('Double tap event initialized.')


class KX022DTDataLogger(SingleChannelEventReader):
    def enable_data_logging(self, **kwargs):
        enable_double_tap(self.sensors[0], **kwargs)


class KX022DTStream(StreamConfig):
    fmt = 'BBBBBBB'
    hdr = 'ch!INS1!INS2!INS3!STATUS!NA!INT_REL'
    reg = r.KX022_INS1

    def __init__(self, sensors, pin_index=None, timer=None):
        sensor = sensors[0]
        assert sensor.name in KX022Driver.supported_parts
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


def main():
    logger = KX022DTDataLogger([KX022Driver])
    logger.enable_data_logging()
    logger.run(KX022DTStream)


if __name__ == '__main__':
    main()
