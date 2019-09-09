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
# pylint: skip-file
# The MIT License (MIT)
# Copyright (c) 2017 Kionix Inc.
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
class register_base: pass
class registers(register_base):
	def __init__(self):
		self.KX122_XHP_L                                          = 0x00         # x- hp filter output.
		self.KX122_XHP_H                                          = 0x01         # msb
		self.KX122_YHP_L                                          = 0x02         # y- hp filter output
		self.KX122_YHP_H                                          = 0x03         # msb
		self.KX122_ZHP_L                                          = 0x04         # z- hpfilteroutput
		self.KX122_ZHP_H                                          = 0x05         # msb
		self.KX122_XOUT_L                                         = 0x06         # output register x
		self.KX122_XOUT_H                                         = 0x07         # msb
		self.KX122_YOUT_L                                         = 0x08         # output register y
		self.KX122_YOUT_H                                         = 0x09         # msb
		self.KX122_ZOUT_L                                         = 0x0A         # output register z
		self.KX122_ZOUT_H                                         = 0x0B         # msb
		self.KX122_COTR                                           = 0x0C         # communication selftest
		self.KX122_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition
		self.KX122_TSCP                                           = 0x10         # Current Tilt Position Register.
		self.KX122_TSPP                                           = 0x11         # Previous Tilt Positon Register.
		self.KX122_INS1                                           = 0x12         # The Interrupt Source 1 (INS1) register indicates the triggering axis when a Tap/Double interrupt occurs
		self.KX122_INS2                                           = 0x13         # The Interrupt Source 2 (INS2) register reports which function caused an interrupt.
		self.KX122_INS3                                           = 0x14         # The Interrupt Source 3 (INS3) register reports the axis and direction of detected motion.
		self.KX122_STATUS_REG                                     = 0x15         # The Status Register reports the status of whether the interrupt is present.
		self.KX122_INT_REL                                        = 0x17         # Latched interrupt source information (INS1,INS2, INS3 except WMI/BFI and INT when WMI/BFI is zero) is cleared and physical interrupt latched pin is changed to its inactive state when this register is read. Read value is dummy.
		self.KX122_CNTL1                                          = 0x18         # The Control 1 (CNTL1) register controls the main feature set of the accelerometer.
		self.KX122_CNTL2                                          = 0x19         # The Control 2 (CNTL2) register provides additional feature set control.
		self.KX122_CNTL3                                          = 0x1A         # The Control 3 (CNTL3) register sets the output data rates for Tilt, Directional-TapTM, and the Motion Wake-Up digital engines.
		self.KX122_ODCNTL                                         = 0x1B         # The ODR Control (ODCNTL) register is responsible for configuring Output Data Rate (ODR) and lowpass filter settings.
		self.KX122_INC1                                           = 0x1C         # The Interrupt Control 1 (INC1) register controls the settings for the physical interrupt pin INT1, the Selftest function, and 3-wire SPI interface.
		self.KX122_INC2                                           = 0x1D         # The Interrupt Control 2 (INC2) register controls which axis and direction of detected motion can cause an interrupt.
		self.KX122_INC3                                           = 0x1E         # The Interrupt Control 3 (INC3) register controls which axis and direction of Tap/Double-TapTM can cause an interrupt.
		self.KX122_INC4                                           = 0x1F         # The Interrupt Control 4 (INC4) register controls routing of an interrupt reporting to physical interrupt pin INT1
		self.KX122_INC5                                           = 0x20         # The Interrupt Control 5 (INC5) register controls the settings for the physical interrupt pin INT2.
		self.KX122_INC6                                           = 0x21         # The Interrupt Control 6 (INC6) register controls routing of interrupt reporting to physical interrupt pin INT2.
		self.KX122_TILT_TIMER                                     = 0x22         # This register is the initial count register for the tilt position state timer (0 to 255 counts).
		self.KX122_WUFC                                           = 0x23         # The Wake-Up Function Counter (WUFC) is the initial count register for the motion detection timer (0 to 255)
		self.KX122_TDTRC                                          = 0x24         # The Tap/Double-TapTM Report Control (TDTRC) register is responsible for enabling/disabling reporting of Tap/Double-TapTM events.
		self.KX122_TDTC                                           = 0x25         # The Tap/Double-TapTM Counter (TDTC) register contains counter information for the detection of a double tap event.
		self.KX122_TTH                                            = 0x26         # The Tap Threshold High (TTH) register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KX122_TTL                                            = 0x27         # The Tap Threshold Low (TTL) register represents the 8-bit (0-255) jerk low threshold to determine if a tap is detected.
		self.KX122_FTD                                            = 0x28         # This register contains counter information for the detection of any tap event.
		self.KX122_STD                                            = 0x29         # This register contains counter information for the detection of a double tap event.
		self.KX122_TLT                                            = 0x2A         # This register contains counter information for the detection of a tap event.
		self.KX122_TWS                                            = 0x2B         # This register contains counter information for the detection of single and double taps.
		self.KX122_FFTH                                           = 0x2C         # The Free Fall Threshold (FFTH) register contains the threshold of the Free fall detection.
		self.KX122_FFC                                            = 0x2D         # The Free Fall Counter (FFC) register contains the counter setting of the Free fall detection.
		self.KX122_FFCNTL                                         = 0x2E         # The Free Fall Control (FFCNTL) register contains the control setting of the Free fall detection.
		self.KX122_ATH                                            = 0x30         # The Activity Threshold (ATH) register sets the threshold for wake-up (motion detect) interrupt is set.
		self.KX122_TILT_ANGLE_LL                                  = 0x32         # Tilt Angle Low Limit: This register sets the low-level threshold for tilt angle detection.
		self.KX122_TILT_ANGLE_HL                                  = 0x33         # Tilt Angle High Limit: This register sets the high-level threshold for tilt angle detection
		self.KX122_HYST_SET                                       = 0x34         # This register sets the Hysteresis that is placed in between the Screen Rotation states.
		self.KX122_LP_CNTL                                        = 0x35         # The Averaging Filter Control set
		self.KX122_BUF_CNTL1                                      = 0x3A         # Read/write control register that controls the buffer sample threshold
		self.KX122_BUF_CNTL2                                      = 0x3B         # Read/write control register that controls sample buffer operation
		self.KX122_BUF_STATUS_1                                   = 0x3C         # This register reports the status of the sample buffer
		self.KX122_BUF_STATUS_2                                   = 0x3D         # This register reports the status of the sample buffer trigger function
		self.KX122_BUF_CLEAR                                      = 0x3E         # Latched buffer status information and the entire sample buffer are cleared when any data is written to this register.
		self.KX122_BUF_READ                                       = 0x3F         # Buffer output register
		self.KX122_SELF_TEST                                      = 0x60         # When 0xCA is written to this register, the MEMS self-test function is enabled. Electrostatic-actuation of the accelerometer, results in a DC shift of the X, Y and Z axis outputs. Writing 0x00 to this register will return the accelerometer to normal operation
		self.KX112_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition
		self.KX123_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition
		self.KX124_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition
class bits(register_base):
	def __init__(self):
		self.KX122_COTR_DCSTR_BEFORE                              = (0x55 << 0)  # before set
		self.KX122_COTR_DCSTR_AFTER                               = (0xAA << 0)  # after set
		self.KX122_WHO_AM_I_WIA_ID                                = (0x1B << 0)  # WHO_AM_I -value for KX122
		self.KX122_TSCP_LE                                        = (0x01 << 5)  # x-left
		self.KX122_TSCP_RI                                        = (0x01 << 4)  # x+right
		self.KX122_TSCP_DO                                        = (0x01 << 3)  # y-down
		self.KX122_TSCP_UP                                        = (0x01 << 2)  # y+up
		self.KX122_TSCP_FD                                        = (0x01 << 1)  # z-facedown
		self.KX122_TSCP_FU                                        = (0x01 << 0)  # z+faceup
		self.KX122_TSPP_LE                                        = (0x01 << 5)  # x-left
		self.KX122_TSPP_RI                                        = (0x01 << 4)  # x+right
		self.KX122_TSPP_DO                                        = (0x01 << 3)  # y-down
		self.KX122_TSPP_UP                                        = (0x01 << 2)  # y+up
		self.KX122_TSPP_FD                                        = (0x01 << 1)  # z-facedown
		self.KX122_TSPP_FU                                        = (0x01 << 0)  # z+faceup
		self.KX122_INS1_TLE                                       = (0x01 << 5)  # x-
		self.KX122_INS1_TRI                                       = (0x01 << 4)  # x+
		self.KX122_INS1_TDO                                       = (0x01 << 3)  # y-
		self.KX122_INS1_TUP                                       = (0x01 << 2)  # y+
		self.KX122_INS1_TFD                                       = (0x01 << 1)  # z-
		self.KX122_INS1_TFU                                       = (0x01 << 0)  # z+
		self.KX122_INS2_FFS                                       = (0x01 << 7)  # Free fall. This bit is cleared when the interrupt latch release register (INL) is read..
		self.KX122_INS2_BFI                                       = (0x01 << 6)  # indicates buffer full interrupt. Automatically cleared when buffer is read.
		self.KX122_INS2_WMI                                       = (0x01 << 5)  # Watermark interrupt, bit is set to one when FIFO has filled up to the value stored in the sample bits.This bit is automatically cleared when FIFO/FILO is read and the content returns to a value below the value stored in the sample bits.
		self.KX122_INS2_DRDY                                      = (0x01 << 4)  # indicates that new acceleration data (0x06h to 0x0Bh) is available. This bit is cleared when acceleration data is read or the interrupt release register INT_REL is read.
		self.KX122_INS2_TDTS_NOTAP                                = (0x00 << 2)  # no tap
		self.KX122_INS2_TDTS_SINGLE                               = (0x01 << 2)  # single tap event
		self.KX122_INS2_TDTS_DOUBLE                               = (0x02 << 2)  # double tap event
		self.KX122_INS2_TDTS_NA                                   = (0x03 << 2)  # do not exist
		self.KX122_INS2_WUFS                                      = (0x01 << 1)  # Status of Wake up. This bit is cleared when the interrupt release register INT_REL is read.
		self.KX122_INS2_TPS                                       = (0x01 << 0)  # Tilt Position status. This bit is cleared when the interrupt release register INT_REL is read.
		self.KX122_INS3_XNWU                                      = (0x01 << 5)  # x-
		self.KX122_INS3_XPWU                                      = (0x01 << 4)  # x+
		self.KX122_INS3_YNWU                                      = (0x01 << 3)  # y-
		self.KX122_INS3_YPWU                                      = (0x01 << 2)  # y+
		self.KX122_INS3_ZNWU                                      = (0x01 << 1)  # z-
		self.KX122_INS3_ZPWU                                      = (0x01 << 0)  # z+
		self.KX122_STATUS_REG_INT                                 = (0x01 << 4)  # INT reports the combined (OR) interrupt information of all features.
		self.KX122_CNTL1_PC1                                      = (0x01 << 7)  # controls the operating mode of the KX122.
		self.KX122_CNTL1_RES                                      = (0x01 << 6)  # determines the performance mode of the KX122. The noise varies with ODR, RES and different LP_CNTL settings possibly reducing the effective resolution.
		self.KX122_CNTL1_DRDYE                                    = (0x01 << 5)  # The Data Ready Enable bit enables the reporting of the availability of new acceleration data as an interrupt.
		self.KX122_CNTL1_GSEL_2G                                  = (0x00 << 3)  # 2g range
		self.KX122_CNTL1_GSEL_4G                                  = (0x01 << 3)  # 4g range
		self.KX122_CNTL1_GSEL_8G                                  = (0x02 << 3)  # 8g range
		self.KX122_CNTL1_GSEL_NA                                  = (0x03 << 3)  # not valid settings
		self.KX122_CNTL1_TDTE                                     = (0x01 << 2)  # enables the Directional Tap function that will detect single and double tap events.
		self.KX122_CNTL1_WUFE                                     = (0x01 << 1)  # enables the Wake Up (motion detect) function
		self.KX122_CNTL1_TPE                                      = (0x01 << 0)  # enables the Tilt Position function that will detect changes in device orientation.
		self.KX122_CNTL2_SRST                                     = (0x01 << 7)  # initiates software reset, which performs the RAM reboot routine
		self.KX122_CNTL2_COTC                                     = (0x01 << 6)  # The Command Test Control bit is used to verify proper ASIC functionality
		self.KX122_CNTL2_LEM                                      = (0x01 << 5)  # x-
		self.KX122_CNTL2_RIM                                      = (0x01 << 4)  # x+
		self.KX122_CNTL2_DOM                                      = (0x01 << 3)  # y-
		self.KX122_CNTL2_UPM                                      = (0x01 << 2)  # y+
		self.KX122_CNTL2_FDM                                      = (0x01 << 1)  # z-
		self.KX122_CNTL2_FUM                                      = (0x01 << 0)  # z+
		self.KX122_CNTL3_OTP_1P563                                = (0x00 << 6)  # 1.5Hz
		self.KX122_CNTL3_OTP_6P25                                 = (0x01 << 6)  # 6.25Hz
		self.KX122_CNTL3_OTP_12P5                                 = (0x02 << 6)  # 12.5Hz
		self.KX122_CNTL3_OTP_50                                   = (0x03 << 6)  # 50Hz
		self.KX122_CNTL3_OTDT_50                                  = (0x00 << 3)  # 50Hz
		self.KX122_CNTL3_OTDT_100                                 = (0x01 << 3)  # 100Hz
		self.KX122_CNTL3_OTDT_200                                 = (0x02 << 3)  # 200Hz
		self.KX122_CNTL3_OTDT_400                                 = (0x03 << 3)  # 400Hz
		self.KX122_CNTL3_OTDT_12P5                                = (0x04 << 3)  # 12.5Hz
		self.KX122_CNTL3_OTDT_25                                  = (0x05 << 3)  # 25Hz
		self.KX122_CNTL3_OTDT_800                                 = (0x06 << 3)  # 800Hz
		self.KX122_CNTL3_OTDT_1600                                = (0x07 << 3)  # 1600Hz
		self.KX122_CNTL3_OWUF_0P781                               = (0x00 << 0)  # 0.78Hz
		self.KX122_CNTL3_OWUF_1P563                               = (0x01 << 0)  # 1.563Hz
		self.KX122_CNTL3_OWUF_3P125                               = (0x02 << 0)  # 3.125Hz
		self.KX122_CNTL3_OWUF_6P25                                = (0x03 << 0)  # 6.25Hz
		self.KX122_CNTL3_OWUF_12P5                                = (0x04 << 0)  # 12.5Hz
		self.KX122_CNTL3_OWUF_25                                  = (0x05 << 0)  # 25Hz
		self.KX122_CNTL3_OWUF_50                                  = (0x06 << 0)  # 50Hz
		self.KX122_CNTL3_OWUF_100                                 = (0x07 << 0)  # 100Hz
		self.KX122_ODCNTL_IIR_BYPASS_APPLY                        = (0x00 << 7)  # filtering applied
		self.KX122_ODCNTL_IIR_BYPASS_BYPASS                       = (0x01 << 7)  # filter bypassed
		self.KX122_ODCNTL_IIR_BYPASS                              = (0x01 << 7)  # filter bypass mode
		self.KX122_ODCNTL_LPRO_ODR_9                              = (0x00 << 6)  # filter corner frequency set to ODR/9
		self.KX122_ODCNTL_LPRO_ODR_2                              = (0x01 << 6)  # filter corner frequency set to ODR/2
		self.KX122_ODCNTL_LPRO                                    = (0x01 << 6)  # low-pass filter roll off control
		self.KX122_ODCNTL_OSA_12P5                                = (0x00 << 0)  # 12.5Hz
		self.KX122_ODCNTL_OSA_25                                  = (0x01 << 0)  # 25Hz
		self.KX122_ODCNTL_OSA_50                                  = (0x02 << 0)  # 50Hz
		self.KX122_ODCNTL_OSA_100                                 = (0x03 << 0)  # 100Hz
		self.KX122_ODCNTL_OSA_200                                 = (0x04 << 0)  # 200Hz
		self.KX122_ODCNTL_OSA_400                                 = (0x05 << 0)  # 400Hz
		self.KX122_ODCNTL_OSA_800                                 = (0x06 << 0)  # 800Hz
		self.KX122_ODCNTL_OSA_1600                                = (0x07 << 0)  # 1600Hz
		self.KX122_ODCNTL_OSA_0P781                               = (0x08 << 0)  # 0.78Hz
		self.KX122_ODCNTL_OSA_1P563                               = (0x09 << 0)  # 1.563Hz
		self.KX122_ODCNTL_OSA_3P125                               = (0x0A << 0)  # 3.125Hz
		self.KX122_ODCNTL_OSA_6P25                                = (0x0B << 0)  # 6.25Hz
		self.KX122_ODCNTL_OSA_3200                                = (0x0C << 0)  # 3200Hz
		self.KX122_ODCNTL_OSA_6400                                = (0x0D << 0)  # 6400Hz
		self.KX122_ODCNTL_OSA_12800                               = (0x0E << 0)  # 12800Hz
		self.KX122_ODCNTL_OSA_25600                               = (0x0F << 0)  # 25600Hz
		self.KX122_INC1_PWSEL1_50US_10US                          = (0x00 << 6)  # pulse 50us, 10us 1600ODR and over
		self.KX122_INC1_PWSEL1_1XOSA                              = (0x01 << 6)  # 1*OSA period
		self.KX122_INC1_PWSEL1_2XOSA                              = (0x02 << 6)  # 2*OSA period
		self.KX122_INC1_PWSEL1_4XOSA                              = (0x03 << 6)  # 4*OSA period
		self.KX122_INC1_IEN1                                      = (0x01 << 5)  # enables/disables the physical interrupt
		self.KX122_INC1_IEA1                                      = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KX122_INC1_IEL1                                      = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KX122_INC1_STPOL                                     = (0x01 << 1)  # sets the polarity of Self Test
		self.KX122_INC1_SPI3E                                     = (0x01 << 0)  # sets the 3-wire SPI interface
		self.KX122_INC2_AOI_OR                                    = (0x00 << 6)  # OR combination between selected directions
		self.KX122_INC2_AOI_AND                                   = (0x01 << 6)  # AND combination between selected axes
		self.KX122_INC2_AOI                                       = (0x01 << 6)  # AND OR configuration for motion detection
		self.KX122_INC2_XNWUE                                     = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KX122_INC2_XPWUE                                     = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KX122_INC2_YNWUE                                     = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KX122_INC2_YPWUE                                     = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KX122_INC2_ZNWUE                                     = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KX122_INC2_ZPWUE                                     = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KX122_INC3_TLEM                                      = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KX122_INC3_TRIM                                      = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KX122_INC3_TDOM                                      = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KX122_INC3_TUPM                                      = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KX122_INC3_TFDM                                      = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KX122_INC3_TFUM                                      = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KX122_INC4_FFI1                                      = (0x01 << 7)  # Free fall interrupt reported on physical interrupt INT1
		self.KX122_INC4_BFI1                                      = (0x01 << 6)  # Buffer full interrupt reported on physical interrupt pin INT1
		self.KX122_INC4_WMI1                                      = (0x01 << 5)  # Watermark interrupt reported on physical interrupt pin INT1
		self.KX122_INC4_DRDYI1                                    = (0x01 << 4)  # Data ready interrupt reported on physical interrupt pin INT1
		self.KX122_INC4_TDTI1                                     = (0x01 << 2)  # Tap/Double Tap interrupt reported on physical interrupt pin INT1
		self.KX122_INC4_WUFI1                                     = (0x01 << 1)  # Wake-Up (motion detect) interrupt reported on physical interrupt pin INT1
		self.KX122_INC4_TPI1                                      = (0x01 << 0)  # Tilt position interrupt reported on physical interrupt pin INT1
		self.KX122_INC5_PWSEL2_50US_10US                          = (0x00 << 6)  # pulse 50us, 10us 1600ODR and over
		self.KX122_INC5_PWSEL2_1XOSA                              = (0x01 << 6)  # 1*OSA period
		self.KX122_INC5_PWSEL2_2XOSA                              = (0x02 << 6)  # 2*OSA period
		self.KX122_INC5_PWSEL2_4XOSA                              = (0x03 << 6)  # 4*OSA period
		self.KX122_INC5_IEN2                                      = (0x01 << 5)  # enables/disables the physical interrupt
		self.KX122_INC5_IEA2                                      = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KX122_INC5_IEL2                                      = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KX122_INC5_ACLR2                                     = (0x01 << 1)  # Interrupt source automatic clear at interup 2 trailing edge
		self.KX122_INC5_ACLR1                                     = (0x01 << 0)  # Interrupt source automatic clear at interup 1 trailing edge
		self.KX122_INC6_FFI2                                      = (0x01 << 7)  # FFI2  Free fall interrupt reported on physical interrupt INT2
		self.KX122_INC6_BFI2                                      = (0x01 << 6)  # BFI2  Buffer full interrupt reported on physical interrupt pin INT2
		self.KX122_INC6_WMI2                                      = (0x01 << 5)  # WMI2 - Watermark interrupt reported on physical interrupt pin INT2
		self.KX122_INC6_DRDYI2                                    = (0x01 << 4)  # DRDYI2  Data ready interrupt reported on physical interrupt pin INT2
		self.KX122_INC6_TDTI2                                     = (0x01 << 2)  # TDTI2 - Tap/Double Tap interrupt reported on physical interrupt pin INT2
		self.KX122_INC6_WUFI2                                     = (0x01 << 1)  # WUFI2  Wake-Up (motion detect) interrupt reported on physical interrupt pin INT2
		self.KX122_INC6_TPI2                                      = (0x01 << 0)  # TPI2  Tilt position interrupt reported on physical interrupt pin INT2
		self.KX122_TDTRC_DTRE                                     = (0x01 << 1)  # enables/disables the double tap interrupt
		self.KX122_TDTRC_STRE                                     = (0x01 << 0)  # enables/disables single tap interrupt
		self.KX122_FFCNTL_FFIE                                    = (0x01 << 7)  # Free fall engine enable
		self.KX122_FFCNTL_ULMODE                                  = (0x01 << 6)  # Free fall interrupt latch/un-latch control
		self.KX122_FFCNTL_DCRM                                    = (0x01 << 3)  # Debounce methodology control
		self.KX122_FFCNTL_OFFI_12P5                               = (0x00 << 0)  # 12.5Hz
		self.KX122_FFCNTL_OFFI_25                                 = (0x01 << 0)  # 25Hz
		self.KX122_FFCNTL_OFFI_50                                 = (0x02 << 0)  # 50Hz
		self.KX122_FFCNTL_OFFI_100                                = (0x03 << 0)  # 100Hz
		self.KX122_FFCNTL_OFFI_200                                = (0x04 << 0)  # 200Hz
		self.KX122_FFCNTL_OFFI_400                                = (0x05 << 0)  # 400Hz
		self.KX122_FFCNTL_OFFI_800                                = (0x06 << 0)  # 800Hz
		self.KX122_FFCNTL_OFFI_1600                               = (0x07 << 0)  # 1600Hz
		self.KX122_LP_CNTL_AVC_NO_AVG                             = (0x00 << 4)  # No Averaging
		self.KX122_LP_CNTL_AVC_2_SAMPLE_AVG                       = (0x01 << 4)  # 2 Samples Averaged
		self.KX122_LP_CNTL_AVC_4_SAMPLE_AVG                       = (0x02 << 4)  # 4 Samples Averaged
		self.KX122_LP_CNTL_AVC_8_SAMPLE_AVG                       = (0x03 << 4)  # 8 Samples Averaged
		self.KX122_LP_CNTL_AVC_16_SAMPLE_AVG                      = (0x04 << 4)  # 16 Samples Averaged (default)
		self.KX122_LP_CNTL_AVC_32_SAMPLE_AVG                      = (0x05 << 4)  # 32 Samples Averaged
		self.KX122_LP_CNTL_AVC_64_SAMPLE_AVG                      = (0x06 << 4)  # 64 Samples Averaged
		self.KX122_LP_CNTL_AVC_128_SAMPLE_AVG                     = (0x07 << 4)  # 128 Samples Averaged
		self.KX122_BUF_CNTL2_BUFE                                 = (0x01 << 7)  # controls activation of the sample buffer
		self.KX122_BUF_CNTL2_BRES                                 = (0x01 << 6)  # determines the resolution of the acceleration data samples collected by the sample
		self.KX122_BUF_CNTL2_BFIE                                 = (0x01 << 5)  # buffer full interrupt enable bit
		self.KX122_BUF_CNTL2_BUF_M_FIFO                           = (0x00 << 0)  # The buffer collects 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values and then stops collecting data, collecting new data only when the buffer is not full
		self.KX122_BUF_CNTL2_BUF_M_STREAM                         = (0x01 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data.
		self.KX122_BUF_CNTL2_BUF_M_TRIGGER                        = (0x02 << 0)  # When a trigger event occurs, the buffer holds the last data set of SMP[9:0] samples before the trigger event and then continues to collect data until full. New data is collected only when the buffer is not full.
		self.KX122_BUF_CNTL2_BUF_M_FILO                           = (0x03 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data. Reading from the buffer in this mode will return the most recent data first.
		self.KX122_BUF_STATUS_2_BUF_TRIG                          = (0x01 << 7)  # reports the status of the buffers trigger function if this mode has been selected
		self.KX122_SELF_TEST_MEMS_TEST_OFF                        = (0x00 << 0)  # MEMS Test OFF
		self.KX122_SELF_TEST_MEMS_TEST_ON                         = (0xCA << 0)  # MEMS Test ON
		self.KX112_WHO_AM_I_WIA_ID                                = (0x22 << 0)  # WHO_AM_I -value for KX112
		self.KX123_WHO_AM_I_WIA_ID                                = (0x20 << 0)  # WHO_AM_I -value for KX123
		self.KX124_WHO_AM_I_WIA_ID                                = (0x28 << 0)  # WHO_AM_I -value for KX124
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KX122_COTR_DCSTR={
			'BEFORE':_b.KX122_COTR_DCSTR_BEFORE,
			'AFTER':_b.KX122_COTR_DCSTR_AFTER,
		}
		self.KX122_INS2_TDTS={
			'NOTAP':_b.KX122_INS2_TDTS_NOTAP,
			'SINGLE':_b.KX122_INS2_TDTS_SINGLE,
			'DOUBLE':_b.KX122_INS2_TDTS_DOUBLE,
			'NA':_b.KX122_INS2_TDTS_NA,
		}
		self.KX122_CNTL1_GSEL={
			'2G':_b.KX122_CNTL1_GSEL_2G,
			'4G':_b.KX122_CNTL1_GSEL_4G,
			'8G':_b.KX122_CNTL1_GSEL_8G,
			'NA':_b.KX122_CNTL1_GSEL_NA,
		}
		self.KX122_CNTL3_OTP={
			'1P563':_b.KX122_CNTL3_OTP_1P563,
			'6P25':_b.KX122_CNTL3_OTP_6P25,
			'12P5':_b.KX122_CNTL3_OTP_12P5,
			'50':_b.KX122_CNTL3_OTP_50,
		}
		self.KX122_CNTL3_OTDT={
			'50':_b.KX122_CNTL3_OTDT_50,
			'100':_b.KX122_CNTL3_OTDT_100,
			'200':_b.KX122_CNTL3_OTDT_200,
			'400':_b.KX122_CNTL3_OTDT_400,
			'12P5':_b.KX122_CNTL3_OTDT_12P5,
			'25':_b.KX122_CNTL3_OTDT_25,
			'800':_b.KX122_CNTL3_OTDT_800,
			'1600':_b.KX122_CNTL3_OTDT_1600,
		}
		self.KX122_CNTL3_OWUF={
			'0P781':_b.KX122_CNTL3_OWUF_0P781,
			'1P563':_b.KX122_CNTL3_OWUF_1P563,
			'3P125':_b.KX122_CNTL3_OWUF_3P125,
			'6P25':_b.KX122_CNTL3_OWUF_6P25,
			'12P5':_b.KX122_CNTL3_OWUF_12P5,
			'25':_b.KX122_CNTL3_OWUF_25,
			'50':_b.KX122_CNTL3_OWUF_50,
			'100':_b.KX122_CNTL3_OWUF_100,
		}
		self.KX122_ODCNTL_IIR_BYPASS={
			'APPLY':_b.KX122_ODCNTL_IIR_BYPASS_APPLY,
			'BYPASS':_b.KX122_ODCNTL_IIR_BYPASS_BYPASS,
		}
		self.KX122_ODCNTL_LPRO={
			'ODR_9':_b.KX122_ODCNTL_LPRO_ODR_9,
			'ODR_2':_b.KX122_ODCNTL_LPRO_ODR_2,
		}
		self.KX122_ODCNTL_OSA={
			'12P5':_b.KX122_ODCNTL_OSA_12P5,
			'25':_b.KX122_ODCNTL_OSA_25,
			'50':_b.KX122_ODCNTL_OSA_50,
			'100':_b.KX122_ODCNTL_OSA_100,
			'200':_b.KX122_ODCNTL_OSA_200,
			'400':_b.KX122_ODCNTL_OSA_400,
			'800':_b.KX122_ODCNTL_OSA_800,
			'1600':_b.KX122_ODCNTL_OSA_1600,
			'0P781':_b.KX122_ODCNTL_OSA_0P781,
			'1P563':_b.KX122_ODCNTL_OSA_1P563,
			'3P125':_b.KX122_ODCNTL_OSA_3P125,
			'6P25':_b.KX122_ODCNTL_OSA_6P25,
			'3200':_b.KX122_ODCNTL_OSA_3200,
			'6400':_b.KX122_ODCNTL_OSA_6400,
			'12800':_b.KX122_ODCNTL_OSA_12800,
			'25600':_b.KX122_ODCNTL_OSA_25600,
		}
		self.KX122_INC1_PWSEL1={
			'50US_10US':_b.KX122_INC1_PWSEL1_50US_10US,
			'1XOSA':_b.KX122_INC1_PWSEL1_1XOSA,
			'2XOSA':_b.KX122_INC1_PWSEL1_2XOSA,
			'4XOSA':_b.KX122_INC1_PWSEL1_4XOSA,
		}
		self.KX122_INC2_AOI={
			'OR':_b.KX122_INC2_AOI_OR,
			'AND':_b.KX122_INC2_AOI_AND,
		}
		self.KX122_INC5_PWSEL2={
			'50US_10US':_b.KX122_INC5_PWSEL2_50US_10US,
			'1XOSA':_b.KX122_INC5_PWSEL2_1XOSA,
			'2XOSA':_b.KX122_INC5_PWSEL2_2XOSA,
			'4XOSA':_b.KX122_INC5_PWSEL2_4XOSA,
		}
		self.KX122_FFCNTL_OFFI={
			'12P5':_b.KX122_FFCNTL_OFFI_12P5,
			'25':_b.KX122_FFCNTL_OFFI_25,
			'50':_b.KX122_FFCNTL_OFFI_50,
			'100':_b.KX122_FFCNTL_OFFI_100,
			'200':_b.KX122_FFCNTL_OFFI_200,
			'400':_b.KX122_FFCNTL_OFFI_400,
			'800':_b.KX122_FFCNTL_OFFI_800,
			'1600':_b.KX122_FFCNTL_OFFI_1600,
		}
		self.KX122_LP_CNTL_AVC={
			'NO_AVG':_b.KX122_LP_CNTL_AVC_NO_AVG,
			'2_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_2_SAMPLE_AVG,
			'4_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_4_SAMPLE_AVG,
			'8_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_8_SAMPLE_AVG,
			'16_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_16_SAMPLE_AVG,
			'32_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_32_SAMPLE_AVG,
			'64_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_64_SAMPLE_AVG,
			'128_SAMPLE_AVG':_b.KX122_LP_CNTL_AVC_128_SAMPLE_AVG,
		}
		self.KX122_BUF_CNTL2_BUF_M={
			'FIFO':_b.KX122_BUF_CNTL2_BUF_M_FIFO,
			'STREAM':_b.KX122_BUF_CNTL2_BUF_M_STREAM,
			'TRIGGER':_b.KX122_BUF_CNTL2_BUF_M_TRIGGER,
			'FILO':_b.KX122_BUF_CNTL2_BUF_M_FILO,
		}
		self.KX122_SELF_TEST_MEMS_TEST={
			'OFF':_b.KX122_SELF_TEST_MEMS_TEST_OFF,
			'ON':_b.KX122_SELF_TEST_MEMS_TEST_ON,
		}
class masks(register_base):
	def __init__(self):
		self.KX122_COTR_DCSTR_MASK                                = 0xFF         # test value
		self.KX122_WHO_AM_I_WIA_MASK                              = 0xFF         # Who Am I value
		self.KX122_INS2_TDTS_MASK                                 = 0x0C         # status of tap/double tap, bit is released when interrupt release register INT_REL is read.
		self.KX122_CNTL1_GSEL_MASK                                = 0x18         # The G-Select bits allow to select the acceleration range of the accelerometer outputs
		self.KX122_CNTL3_OTP_MASK                                 = 0xC0         # sets the output data rate for the Tilt Position function
		self.KX122_CNTL3_OTDT_MASK                                = 0x38         # sets the output data rate for the Directional TapTM function
		self.KX122_CNTL3_OWUF_MASK                                = 0x07         # sets the output data rate for the general motion detection function and the high-pass filtered outputs
		self.KX122_ODCNTL_IIR_BYPASS_MASK                         = 0x80         # filter bypass mode
		self.KX122_ODCNTL_LPRO_MASK                               = 0x40         # low-pass filter roll off control
		self.KX122_ODCNTL_OSA_MASK                                = 0x0F         # acceleration output data rate.
		self.KX122_INC1_PWSEL1_MASK                               = 0xC0         # Pulse interrupt 1 width configuration
		self.KX122_INC2_AOI_MASK                                  = 0x40         # AND OR configuration for motion detection
		self.KX122_INC5_PWSEL2_MASK                               = 0xC0         # Pulse interrupt 2 width configuration
		self.KX122_TILT_TIMER_TSC_MASK                            = 0xFF         # This register is the initial count register for the tilt position state timer (0 to 255 counts).
		self.KX122_WUFC_WUFC_MASK                                 = 0xFF         # The Wake-Up Function Counter (WUFC) is the initial count register for the motion detection timer (0 to 255)
		self.KX122_TDTC_TDTC_MASK                                 = 0xFF         # The Tap/Double-TapTM Counter (TDTC) register contains counter information for the detection of a double tap event.
		self.KX122_TTH_TTH_MASK                                   = 0xFF         # The Tap Threshold High (TTH) register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KX122_TTL_TTL_MASK                                   = 0xFF         # The Tap Threshold Low (TTL) register represents the 8-bit (0-255) jerk low threshold to determine if a tap is detected.
		self.KX122_FTD_FTDH_MASK                                  = 0xF8         # Detection tap for the high limit
		self.KX122_FTD_FTDL_MASK                                  = 0x07         # Detection tap for the low limit
		self.KX122_STD_STD_MASK                                   = 0xFF         # This register contains counter information for the detection of a double tap event.
		self.KX122_TLT_TLT_MASK                                   = 0xFF         # This register contains counter information for the detection of a tap event.
		self.KX122_TWS_TWS_MASK                                   = 0xFF         # This register contains counter information for the detection of single and double taps.
		self.KX122_FFTH_FFTH_MASK                                 = 0xFF         # The Free Fall Threshold (FFTH) register contains the threshold of the Free fall detection.
		self.KX122_FFC_FFC_MASK                                   = 0xFF         # The Free Fall Counter (FFC) register contains the counter setting of the Free fall detection.
		self.KX122_FFCNTL_OFFI_MASK                               = 0x07         # Output Data Rate at which the Free fall engine performs its function.
		self.KX122_ATH_ATH_MASK                                   = 0xFF         # The Activity Threshold (ATH) register sets the threshold for wake-up (motion detect) interrupt is set.
		self.KX122_TILT_ANGLE_LL_TA_MASK                          = 0xFF         # Tilt Angle Low Limit: This register sets the low-level threshold for tilt angle detection.
		self.KX122_TILT_ANGLE_HL_HL_MASK                          = 0xFF         # Tilt Angle High Limit: This register sets the high-level threshold for tilt angle detection
		self.KX122_HYST_SET_HYST_MASK                             = 0x3F         # Tilt angle hysteresis value
		self.KX122_LP_CNTL_AVC_MASK                               = 0x70         # Averaging Filter Control
		self.KX122_BUF_CNTL2_SMP_TH8_9_MASK                       = 0x0C         # buffer sample control threshold msb part
		self.KX122_BUF_CNTL2_BUF_M_MASK                           = 0x03         # selects the operating mode of the sample buffer
		self.KX122_BUF_STATUS_2_SMP_LEV8_10_MASK                  = 0x07         # buffer status sample level msb part
		self.KX122_SELF_TEST_MEMS_TEST_MASK                       = 0xFF         # self test value
		self.KX112_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KX123_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KX124_WHO_AM_I_WIA_MASK                              = 0xFF         