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
 Orientation Detection (ORI) is integrated feature for display rotation application

 MAIN REGISTER PARAMETERS
 Angle parameters are scaled to 2g measurement range
      TILT_ANGLE_LL is (according component's coordinate) threshold angle from currently detected position to another position
      TILT_ANGLE_HL is "transient angle" prevention threshold during rotating motion. Helpful parameter if timer value is short
      HYST_SET is +/-addenum to TILT_ANGLE_LL to prevent detection vibration
 TILT_TIMER is time * (1/OTP); how many sample must be valid until accepted
 OTP is selection of function dedicated ODR(Hz)
 CNTL2, bits LEM, RIM, DOM, UPM, FDM and FUM are masks of x-, x+, y+, y-, z+ and z-

 practically, with example values:
 from horizontal direction (z+ or z- side top); threshold level (to horizontal level) is 30degrees
 from vertical direction (x+,  x-,  y+ or y- side top); threshold level (compared to horizontal level) is 30degrees (or 60 degrees from start)

 other parameters
      CNTL1, bit RES and LP_CNTL average value make effects to current consumption
      ODCNTL, bit OSAx and CNTL3, bits OWUFx, OTDTx make effect current consumption if selected ORD is higher than OTPx

"""
# Example app for tilt position detection
##
# tilt position detection uses interrupt int2
##
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY
from kx_lib.kx_util import get_other_pin_index, convert_to_enumkey
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx126.kx126_driver import KX126Driver, r, b, m, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class Parameter_set_1: # pylint: disable=bad-whitespace
    # default values
    LOW_POWER_MODE        = False
    odr_OSA               = 25
    lp_average            = '16_SAMPLE_AVG'
    odr_OTP               = 12.5
    TILT_TIMER_VALUE      = 0x04    # Register's default value 0x00; timer = 0.0s
                                    # 0x04 is 0.32s with 12.5Hz OTP, this value prevents detection vibration
    TILT_ANGLE_LL_VALUE   = 0x10    # Register's default value 0x0C; angles about 22 and 90-22=58 degrees
                                    # 0x10 = 30degrees maybe better value than default
    TILT_ANGLE_HL_VALUE   = 0x2A    # Register's default value 0x2A; angle over 90 degrees
                                    # 0x2D maybe better
    HYST_SET_VALUE        = 0x14    # Register's default value; angle threshold addenum +15/-15 degrees

class Parameter_set_2: # pylint: disable=bad-whitespace
    # values for detecting tilt angle angles 25 degrees / 20 degrees
    LOW_POWER_MODE        = False
    odr_OSA               = 25
    lp_average            = '16_SAMPLE_AVG'
    odr_OTP               = 12.5
    TILT_TIMER_VALUE      = 0x02    # Register's default value 0x00; timer = 0.0s
    TILT_ANGLE_LL_VALUE   = 0x0C    # 20deg is target angle
    TILT_ANGLE_HL_VALUE   = 0x2D    # transient angle blocking
    HYST_SET_VALUE        = 0x09    # hysteresis ~5 degrees


# native / rotated directions
resultResolverToString = {
    b.KX126_TSCP_LE: "x-",
    b.KX126_TSCP_RI: "x+",
    b.KX126_TSCP_DO: "y-",
    b.KX126_TSCP_UP: "y+",
    b.KX126_TSCP_FD: "z-",
    b.KX126_TSCP_FU: "z+"}


class KX126TiltStream(StreamConfig):
    fmt = "BBBBBBBB"
    hdr = "ch!tscp!tspp!ins1!ins2!ins3!status!rel"
    reg = r.KX126_TSCP

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


def enable_tilt_position(sensor,
                         direction_mask=b.KX126_CNTL2_LEM |  # x- tilt direction mask
                         b.KX126_CNTL2_RIM |  # x+ tilt direction mask
                         b.KX126_CNTL2_DOM |  # y- tilt direction mask
                         b.KX126_CNTL2_UPM |  # y+ tilt direction mask
                         b.KX126_CNTL2_FDM |  # z- tilt direction mask
                         b.KX126_CNTL2_FUM,  # z+ tilt direction mask
                         cfg=Parameter_set_1,
                         power_off_on=True
                         ):

    LOGGER.info('Tilt position detection init start')

    assert convert_to_enumkey(cfg.odr_OSA) in e.KX126_ODCNTL_OSA.keys(), \
        'Invalid odr_OSA value "{}". Valid values are {}'.format(
        cfg.odr_OSA, e.KX126_ODCNTL_OSA.keys())

    assert convert_to_enumkey(cfg.odr_OTP) in e.KX126_CNTL3_OTP.keys(), \
        'Invalid odr_OTP value "{}". Valid values are {}'.format(
            cfg.odr_OTP, e.KX126_CNTL3_OTP.keys())

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

    # stream odr (if stream odr is biggest odr, it makes effect to current consumption)
    sensor.set_odr(e.KX126_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])

    # g-range is fixed +-4g

    # resolution / power mode selection
    # Set performance mode (To change value, the PC1 must be first cleared to set stand-by mode)
    if cfg.LOW_POWER_MODE is True:
        sensor.reset_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                          # low current

        # set averaging for low power mode
        sensor.set_average(e.KX126_LP_CNTL_AVC[cfg.lp_average])  # average of 16 samples
    else:
        sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_RES)                    # high resolution

    sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_TPE)                        # enable tilt position engine

    # tilt position feature settings
    sensor.write_register(r.KX126_CNTL3, e.KX126_CNTL3_OTP[convert_to_enumkey(cfg.odr_OTP)])          # tilt detection ODR is 12.5Hz

    sensor.write_register(r.KX126_CNTL2, direction_mask)

    sensor.write_register(r.KX126_TILT_TIMER, cfg.TILT_TIMER_VALUE)             # Tilt timer
    sensor.write_register(r.KX126_TILT_ANGLE_LL, cfg.TILT_ANGLE_LL_VALUE)       # lower tilt angle threshold
    sensor.write_register(r.KX126_TILT_ANGLE_HL, cfg.TILT_ANGLE_HL_VALUE)       # higher tilt angle threshold
    sensor.write_register(r.KX126_HYST_SET, cfg.HYST_SET_VALUE)                 # angle hysteresis

    #
    # interrupt pin routings and settings
    #
    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity {}'.format(
        sensor.resource[CFG_POLARITY]))
    sensor.set_interrupt_polarity(intpin=2, polarity=polarity)

    # interrupt pin routings and settings
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2)   # latched interrupt for int2
    sensor.set_bit(r.KX126_INC6, b.KX126_INC6_TPI2)     # enable tilt detection to int 2
    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)     # enable int2 pin

    # Turn on operating mode (disables setup)
    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('Tilt position event initialized.')

    sensor.release_interrupts()                         # clear all internal function interrupts


def determine_tilt_position(data):
    channel, tscp, tspp, ins1, ins2, ins3, status, rel = data
    #print (channel, tscp, tspp, ins1, ins2, ins3, status, rel)
    print('TILT_POSITION:' + resultResolverToString[tscp])
    del channel, tscp, tspp, ins1, ins2, ins3, status, rel
    return True  # Continue reading


class KX126TiltLogger(SingleChannelEventReader):

    def enable_data_logging(self, **kwargs):
        enable_tilt_position(self.sensors[0], **kwargs)

    # def read_with_polling(self, **_):
    #     raise NotImplementedError('Polling mode not supported.')


def main():
    app = KX126TiltLogger([KX126Driver])
    app.enable_data_logging()
    app.run(KX126TiltStream, pin_index=2)


if __name__ == '__main__':
    main()
