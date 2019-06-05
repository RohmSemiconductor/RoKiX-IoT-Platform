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
		self.KX224_XHP_L                                          = 0x00         # x- hp filter output
		self.KX224_XHP_H                                          = 0x01         
		self.KX224_YHP_L                                          = 0x02         # y- hp filter output
		self.KX224_YHP_H                                          = 0x03         
		self.KX224_ZHP_L                                          = 0x04         # z- hpfilteroutput
		self.KX224_ZHP_H                                          = 0x05         
		self.KX224_XOUT_L                                         = 0x06         # output register x
		self.KX224_XOUT_H                                         = 0x07         
		self.KX224_YOUT_L                                         = 0x08         # output register y
		self.KX224_YOUT_H                                         = 0x09         
		self.KX224_ZOUT_L                                         = 0x0A         # output register z
		self.KX224_ZOUT_H                                         = 0x0B         
		self.KX224_COTR                                           = 0x0C         # communication selftest
		self.KX224_WHO_AM_I                                       = 0x0F         # WHO_AM_I
		self.KX224_TSCP                                           = 0x10         # current sixfacet posititions
		self.KX224_TSPP                                           = 0x11         # previous six facet positions
		self.KX224_INS1                                           = 0x12         # This register indicates the triggering axis when a tap/double tap interrupt occurs.
		self.KX224_INS2                                           = 0x13         # This register tells witch function caused an interrupt.
		self.KX224_INS3                                           = 0x14         # This register reports the axis and direction of detected motion.
		self.KX224_STATUS_REG                                     = 0x15         # This register reports the status of the interrupt.
		self.KX224_INT_REL                                        = 0x17         # Latched interrupt source information (INS1,INS2, INS3 except WMI/BFI and INT when WMI/BFI is zero) is cleared and physical interrupt latched pin is changed to its inactive state when this register is read. Read value is dummy.
		self.KX224_CNTL1                                          = 0x18         # Read/write control register that controls the main feature set.
		self.KX224_CNTL2                                          = 0x19         # 2' control register
		self.KX224_CNTL3                                          = 0x1A         # 3' controlregister
		self.KX224_ODCNTL                                         = 0x1B         # This register is responsible for configuring ODR (output data rate) and filter settings
		self.KX224_INC1                                           = 0x1C         # This register controls the settings for the physical interrupt pin INT1
		self.KX224_INC2                                           = 0x1D         # This register controls which axis and direction of detected motion can cause an interrupt.
		self.KX224_INC3                                           = 0x1E         # This register controls which axis and direction of tap/double tap can cause an interrup
		self.KX224_INC4                                           = 0x1F         # This register controls routing of an interrupt reporting to physical interrupt pin INT1
		self.KX224_INC5                                           = 0x20         # This register controls the settings for the physical interrupt pin INT2.
		self.KX224_INC6                                           = 0x21         # This register controls routing of interrupt reporting to physical interrupt pin INT2
		self.KX224_TILT_TIMER                                     = 0x22         # This register is the initial count register for the tilt position state timer
		self.KX224_WUFC                                           = 0x23         # This register is the initial count register for the motion detection timer
		self.KX224_TDTRC                                          = 0x24         # This register is responsible for enableing/disabling reporting of Tap/Double Tap.
		self.KX224_TDTC                                           = 0x25         # This register contains counter information for the detection of a double tap event.
		self.KX224_TTH                                            = 0x26         # This register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KX224_TTL                                            = 0x27         # This register represents the 8-bit (0d 255d) jerk low threshold to determine if a tap is detected.
		self.KX224_FTD                                            = 0x28         # This register contains counter information for the detection of any tap event.
		self.KX224_STD                                            = 0x29         # This register contains counter information for the detection of a double tap event
		self.KX224_TLT                                            = 0x2A         # This register contains counter information for the detection of a tap event.
		self.KX224_TWS                                            = 0x2B         # This register contains counter information for the detection of single and double taps.
		self.KX224_FFTH                                           = 0x2C         # Free Fall Threshold
		self.KX224_FFC                                            = 0x2D         # Free Fall Counter
		self.KX224_FFCNTL                                         = 0x2E         # Free Fall Control: This register contains the counter setting of the Free fall detection.
		self.KX224_ATH                                            = 0x30         # This register sets the threshold for wake-up (motion detect) interrupt is set.
		self.KX224_TILT_ANGLE_LL                                  = 0x32         # This register sets the low level threshold for tilt angle detection.
		self.KX224_TILT_ANGLE_HL                                  = 0x33         # This register sets the high level threshold for tilt angle detection.
		self.KX224_HYST_SET                                       = 0x34         # This register sets the Hysteresis that is placed in between the Screen Rotation states
		self.KX224_LP_CNTL                                        = 0x35         # Low Power Control sets the number of samples of accelerometer output to be average
		self.KX224_BUF_CNTL1                                      = 0x3A         # Read/write control register that controls the buffer sample threshold
		self.KX224_BUF_CNTL2                                      = 0x3B         # Read/write control register that controls sample buffer operation
		self.KX224_BUF_STATUS_1                                   = 0x3C         # This register reports the status of the sample buffer
		self.KX224_BUF_STATUS_2                                   = 0x3D         # This register reports the status of the sample buffer trigger function
		self.KX224_BUF_CLEAR                                      = 0x3E         # Latched buffer status information and the entire sample buffer are cleared when any data is written to this register.
		self.KX224_BUF_READ                                       = 0x3F         # Buffer output register
		self.KX224_SELF_TEST                                      = 0x60         # When 0xCA is written to this register, the MEMS self-test function is enabled. Electrostatic-actuation of the accelerometer, results in a DC shift of the X, Y and Z axis outputs. Writing 0x00 to this register will return the accelerometer to normal operation
		self.KX222_WHO_AM_I                                       = 0x0F         # WHO_AM_I
class bits(register_base):
	def __init__(self):
		self.KX224_COTR_DCSTR_BEFORE                              = (0x55 << 0)  # before set
		self.KX224_COTR_DCSTR_AFTER                               = (0xAA << 0)  # after set
		self.KX224_WHO_AM_I_WIA_ID                                = (0x2B << 0)  # WHO_AM_I -value for KX224
		self.KX224_TSCP_LE                                        = (0x01 << 5)  # x-left
		self.KX224_TSCP_RI                                        = (0x01 << 4)  # x+right
		self.KX224_TSCP_DO                                        = (0x01 << 3)  # y-down
		self.KX224_TSCP_UP                                        = (0x01 << 2)  # y+up
		self.KX224_TSCP_FD                                        = (0x01 << 1)  # z-facedown
		self.KX224_TSCP_FU                                        = (0x01 << 0)  # z+faceup
		self.KX224_TSPP_LE                                        = (0x01 << 5)  # x-left
		self.KX224_TSPP_RI                                        = (0x01 << 4)  # x+right
		self.KX224_TSPP_DO                                        = (0x01 << 3)  # y-down
		self.KX224_TSPP_UP                                        = (0x01 << 2)  # y+up
		self.KX224_TSPP_FD                                        = (0x01 << 1)  # z-facedown
		self.KX224_TSPP_FU                                        = (0x01 << 0)  # z+faceup
		self.KX224_INS1_TLE                                       = (0x01 << 5)  # x-
		self.KX224_INS1_TRI                                       = (0x01 << 4)  # x+
		self.KX224_INS1_TDO                                       = (0x01 << 3)  # y-
		self.KX224_INS1_TUP                                       = (0x01 << 2)  # y+
		self.KX224_INS1_TFD                                       = (0x01 << 1)  # z-
		self.KX224_INS1_TFU                                       = (0x01 << 0)  # z+
		self.KX224_INS2_FFS                                       = (0x01 << 7)  # Free fall. This bit is cleared when the interrupt latch release register (INL) is read..
		self.KX224_INS2_BFI                                       = (0x01 << 6)  # indicates buffer full interrupt. Automatically cleared when buffer is read.
		self.KX224_INS2_WMI                                       = (0x01 << 5)  # Watermark interrupt, bit is set to one when FIFO has filled up to the value stored in the sample bits.This bit is automatically cleared when FIFO/FILO is read and the content returns to a value below the value stored in the sample bits.
		self.KX224_INS2_DRDY                                      = (0x01 << 4)  # indicates that new acceleration data (0x06h to 0x0Bh) is available. This bit is cleared when acceleration data is read or the interrupt release register INT_REL is read.
		self.KX224_INS2_TDTS_NOTAP                                = (0x00 << 2)  # no tap
		self.KX224_INS2_TDTS_SINGLE                               = (0x01 << 2)  # single tap event
		self.KX224_INS2_TDTS_DOUBLE                               = (0x02 << 2)  # double tap event
		self.KX224_INS2_TDTS_NA                                   = (0x03 << 2)  # do not exist
		self.KX224_INS2_WUFS                                      = (0x01 << 1)  # Status of Wake up. This bit is cleared when the interrupt release register INT_REL is read.
		self.KX224_INS2_TPS                                       = (0x01 << 0)  # Tilt Position status. This bit is cleared when the interrupt release register INT_REL is read.
		self.KX224_INS3_XNWU                                      = (0x01 << 5)  # x-
		self.KX224_INS3_XPWU                                      = (0x01 << 4)  # x+
		self.KX224_INS3_YNWU                                      = (0x01 << 3)  # y-
		self.KX224_INS3_YPWU                                      = (0x01 << 2)  # y+
		self.KX224_INS3_ZNWU                                      = (0x01 << 1)  # z-
		self.KX224_INS3_ZPWU                                      = (0x01 << 0)  # z+
		self.KX224_STATUS_REG_INT                                 = (0x01 << 4)  # INT reports the combined (OR) interrupt information of all features.
		self.KX224_CNTL1_PC1                                      = (0x01 << 7)  # controls the operating mode of the KX122.
		self.KX224_CNTL1_RES                                      = (0x01 << 6)  # determines the performance mode of the KX122. The noise varies with ODR, RES and different LP_CNTL settings possibly reducing the effective resolution.
		self.KX224_CNTL1_DRDYE                                    = (0x01 << 5)  # enables the reporting of the availability of new acceleration data as an interrupt
		self.KX224_CNTL1_GSEL_8G                                  = (0x00 << 3)  # 8g range
		self.KX224_CNTL1_GSEL_16G                                 = (0x01 << 3)  # 16g range
		self.KX224_CNTL1_GSEL_32G                                 = (0x02 << 3)  # 32g range
		self.KX224_CNTL1_GSEL_NA                                  = (0x03 << 3)  # not valid settings
		self.KX224_CNTL1_TDTE                                     = (0x01 << 2)  # enables the Directional Tap function that will detect single and double tap events.
		self.KX224_CNTL1_WUFE                                     = (0x01 << 1)  # enables the Wake Up (motion detect) function
		self.KX224_CNTL1_TPE                                      = (0x01 << 0)  # enables the Tilt Position function that will detect changes in device orientation.
		self.KX224_CNTL2_SRST                                     = (0x01 << 7)  # initiates software reset, which performs the RAM reboot routine
		self.KX224_CNTL2_COTC                                     = (0x01 << 6)  # command test control
		self.KX224_CNTL2_LEM                                      = (0x01 << 5)  # x-
		self.KX224_CNTL2_RIM                                      = (0x01 << 4)  # x+
		self.KX224_CNTL2_DOM                                      = (0x01 << 3)  # y-
		self.KX224_CNTL2_UPM                                      = (0x01 << 2)  # y+
		self.KX224_CNTL2_FDM                                      = (0x01 << 1)  # z-
		self.KX224_CNTL2_FUM                                      = (0x01 << 0)  # z+
		self.KX224_CNTL3_OTP_1P563                                = (0x00 << 6)  # 1.5Hz
		self.KX224_CNTL3_OTP_6P25                                 = (0x01 << 6)  # 6.25Hz
		self.KX224_CNTL3_OTP_12P5                                 = (0x02 << 6)  # 12.5Hz
		self.KX224_CNTL3_OTP_50                                   = (0x03 << 6)  # 50Hz
		self.KX224_CNTL3_OTDT_50                                  = (0x00 << 3)  # 50Hz
		self.KX224_CNTL3_OTDT_100                                 = (0x01 << 3)  # 100Hz
		self.KX224_CNTL3_OTDT_200                                 = (0x02 << 3)  # 200Hz
		self.KX224_CNTL3_OTDT_400                                 = (0x03 << 3)  # 400Hz
		self.KX224_CNTL3_OTDT_12P5                                = (0x04 << 3)  # 12.5Hz
		self.KX224_CNTL3_OTDT_25                                  = (0x05 << 3)  # 25Hz
		self.KX224_CNTL3_OTDT_800                                 = (0x06 << 3)  # 800Hz
		self.KX224_CNTL3_OTDT_1600                                = (0x07 << 3)  # 1600Hz
		self.KX224_CNTL3_OWUF_0P781                               = (0x00 << 0)  # 0.78Hz
		self.KX224_CNTL3_OWUF_1P563                               = (0x01 << 0)  # 1.563Hz
		self.KX224_CNTL3_OWUF_3P125                               = (0x02 << 0)  # 3.125Hz
		self.KX224_CNTL3_OWUF_6P25                                = (0x03 << 0)  # 6.25Hz
		self.KX224_CNTL3_OWUF_12P5                                = (0x04 << 0)  # 12.5Hz
		self.KX224_CNTL3_OWUF_25                                  = (0x05 << 0)  # 25Hz
		self.KX224_CNTL3_OWUF_50                                  = (0x06 << 0)  # 50Hz
		self.KX224_CNTL3_OWUF_100                                 = (0x07 << 0)  # 100Hz
		self.KX224_ODCNTL_IIR_BYPASS                              = (0x01 << 7)  # low-pass filter roll off control
		self.KX224_ODCNTL_LPRO_ODR_9                              = (0x00 << 6)  # filter corner frequency set to ODR/9
		self.KX224_ODCNTL_LPRO_ODR_2                              = (0x01 << 6)  # filter corner frequency set to ODR/2
		self.KX224_ODCNTL_LPRO                                    = (0x01 << 6)  # low pass filter enable
		self.KX224_ODCNTL_OSA_12P5                                = (0x00 << 0)  # 12.5Hz
		self.KX224_ODCNTL_OSA_25                                  = (0x01 << 0)  # 25Hz
		self.KX224_ODCNTL_OSA_50                                  = (0x02 << 0)  # 50Hz
		self.KX224_ODCNTL_OSA_100                                 = (0x03 << 0)  # 100Hz
		self.KX224_ODCNTL_OSA_200                                 = (0x04 << 0)  # 200Hz
		self.KX224_ODCNTL_OSA_400                                 = (0x05 << 0)  # 400Hz
		self.KX224_ODCNTL_OSA_800                                 = (0x06 << 0)  # 800Hz
		self.KX224_ODCNTL_OSA_1600                                = (0x07 << 0)  # 1600Hz
		self.KX224_ODCNTL_OSA_0P781                               = (0x08 << 0)  # 0.78Hz
		self.KX224_ODCNTL_OSA_1P563                               = (0x09 << 0)  # 1.563Hz
		self.KX224_ODCNTL_OSA_3P125                               = (0x0A << 0)  # 3.125Hz
		self.KX224_ODCNTL_OSA_6P25                                = (0x0B << 0)  # 6.25Hz
		self.KX224_ODCNTL_OSA_3200                                = (0x0C << 0)  # 3200Hz
		self.KX224_ODCNTL_OSA_6400                                = (0x0D << 0)  # 6400Hz
		self.KX224_ODCNTL_OSA_12800                               = (0x0E << 0)  # 12800Hz
		self.KX224_ODCNTL_OSA_25600                               = (0x0F << 0)  # 25600Hz
		self.KX224_INC1_PWSEL1_50US_10US                          = (0x00 << 6)  # pulse 50us, 10us 1600ODR and over
		self.KX224_INC1_PWSEL1_1XOSA                              = (0x01 << 6)  # 1*OSA period
		self.KX224_INC1_PWSEL1_2XOSA                              = (0x02 << 6)  # 2*OSA period
		self.KX224_INC1_PWSEL1_4XOSA                              = (0x03 << 6)  # 4*OSA period
		self.KX224_INC1_IEN1                                      = (0x01 << 5)  # enables/disables the physical interrupt
		self.KX224_INC1_IEA1                                      = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KX224_INC1_IEL1                                      = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KX224_INC1_STPOL                                     = (0x01 << 1)  # sets the polarity of Self Test
		self.KX224_INC1_SPI3E                                     = (0x01 << 0)  # sets the 3-wire SPI interface
		self.KX224_INC2_AOI_OR                                    = (0x00 << 6)  # OR combination between selected directions
		self.KX224_INC2_AOI_AND                                   = (0x01 << 6)  # AND combination between selected axes
		self.KX224_INC2_AOI                                       = (0x01 << 6)  # AND OR configuration for motion detection
		self.KX224_INC2_XNWUE                                     = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KX224_INC2_XPWUE                                     = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KX224_INC2_YNWUE                                     = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KX224_INC2_YPWUE                                     = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KX224_INC2_ZNWUE                                     = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KX224_INC2_ZPWUE                                     = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KX224_INC3_TLEM                                      = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KX224_INC3_TRIM                                      = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KX224_INC3_TDOM                                      = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KX224_INC3_TUPM                                      = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KX224_INC3_TFDM                                      = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KX224_INC3_TFUM                                      = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KX224_INC4_FFI1                                      = (0x01 << 7)  # Free fall interrupt reported on physical interrupt INT1
		self.KX224_INC4_BFI1                                      = (0x01 << 6)  # Buffer full interrupt reported on physical interrupt pin INT1
		self.KX224_INC4_WMI1                                      = (0x01 << 5)  # Watermark interrupt reported on physical interrupt pin INT1
		self.KX224_INC4_DRDYI1                                    = (0x01 << 4)  # Data ready interrupt reported on physical interrupt pin INT1
		self.KX224_INC4_TDTI1                                     = (0x01 << 2)  # Tap/Double Tap interrupt reported on physical interrupt pin INT1
		self.KX224_INC4_WUFI1                                     = (0x01 << 1)  # Wake-Up (motion detect) interrupt reported on physical interrupt pin INT1
		self.KX224_INC4_TPI1                                      = (0x01 << 0)  # Tilt position interrupt reported on physical interrupt pin INT1
		self.KX224_INC5_PWSEL2_50US_10US                          = (0x00 << 6)  # pulse 50us, 10us 1600ODR and over
		self.KX224_INC5_PWSEL2_1XOSA                              = (0x01 << 6)  # 1*OSA period
		self.KX224_INC5_PWSEL2_2XOSA                              = (0x02 << 6)  # 2*OSA period
		self.KX224_INC5_PWSEL2_4XOSA                              = (0x03 << 6)  # 4*OSA period
		self.KX224_INC5_IEN2                                      = (0x01 << 5)  # enables/disables the physical interrupt
		self.KX224_INC5_IEA2                                      = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KX224_INC5_IEL2                                      = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KX224_INC5_ACLR2                                     = (0x01 << 1)  # Interrupt source automatic clear at interup 2 trailing edge
		self.KX224_INC5_ACLR1                                     = (0x01 << 0)  # Interrupt source automatic clear at interup 1 trailing edge
		self.KX224_INC6_FFI2                                      = (0x01 << 7)  # FFI2  Free fall interrupt reported on physical interrupt INT2
		self.KX224_INC6_BFI2                                      = (0x01 << 6)  # BFI2  Buffer full interrupt reported on physical interrupt pin INT2
		self.KX224_INC6_WMI2                                      = (0x01 << 5)  # WMI2 - Watermark interrupt reported on physical interrupt pin INT2
		self.KX224_INC6_DRDYI2                                    = (0x01 << 4)  # DRDYI2  Data ready interrupt reported on physical interrupt pin INT2
		self.KX224_INC6_TDTI2                                     = (0x01 << 2)  # TDTI2 - Tap/Double Tap interrupt reported on physical interrupt pin INT2
		self.KX224_INC6_WUFI2                                     = (0x01 << 1)  # WUFI2  Wake-Up (motion detect) interrupt reported on physical interrupt pin INT2
		self.KX224_INC6_TPI2                                      = (0x01 << 0)  # TPI2  Tilt position interrupt reported on physical interrupt pin INT2
		self.KX224_TDTRC_DTRE                                     = (0x01 << 1)  # enables/disables the double tap interrupt
		self.KX224_TDTRC_STRE                                     = (0x01 << 0)  # enables/disables single tap interrupt
		self.KX224_FFCNTL_FFIE                                    = (0x01 << 7)  # Free fall engine enable
		self.KX224_FFCNTL_ULMODE                                  = (0x01 << 6)  # Free fall interrupt latch/un-latch control
		self.KX224_FFCNTL_DCRM                                    = (0x01 << 3)  # Debounce methodology control
		self.KX224_FFCNTL_OFFI_12P5                               = (0x00 << 0)  # 12.5Hz
		self.KX224_FFCNTL_OFFI_25                                 = (0x01 << 0)  # 25Hz
		self.KX224_FFCNTL_OFFI_50                                 = (0x02 << 0)  # 50Hz
		self.KX224_FFCNTL_OFFI_100                                = (0x03 << 0)  # 100Hz
		self.KX224_FFCNTL_OFFI_200                                = (0x04 << 0)  # 200Hz
		self.KX224_FFCNTL_OFFI_400                                = (0x05 << 0)  # 400Hz
		self.KX224_FFCNTL_OFFI_800                                = (0x06 << 0)  # 800Hz
		self.KX224_FFCNTL_OFFI_1600                               = (0x07 << 0)  # 1600Hz
		self.KX224_LP_CNTL_AVC_NO_AVG                             = (0x00 << 4)  # No Averaging
		self.KX224_LP_CNTL_AVC_2_SAMPLE_AVG                       = (0x01 << 4)  # 2 Samples Averaged
		self.KX224_LP_CNTL_AVC_4_SAMPLE_AVG                       = (0x02 << 4)  # 4 Samples Averaged
		self.KX224_LP_CNTL_AVC_8_SAMPLE_AVG                       = (0x03 << 4)  # 8 Samples Averaged
		self.KX224_LP_CNTL_AVC_16_SAMPLE_AVG                      = (0x04 << 4)  # 16 Samples Averaged (default)
		self.KX224_LP_CNTL_AVC_32_SAMPLE_AVG                      = (0x05 << 4)  # 32 Samples Averaged
		self.KX224_LP_CNTL_AVC_64_SAMPLE_AVG                      = (0x06 << 4)  # 64 Samples Averaged
		self.KX224_LP_CNTL_AVC_128_SAMPLE_AVG                     = (0x07 << 4)  # 128 Samples Averaged
		self.KX224_BUF_CNTL1_SMP_TH0_7                            = (0xFF << 0)  
		self.KX224_BUF_CNTL2_BUFE                                 = (0x01 << 7)  # controls activation of the sample buffer
		self.KX224_BUF_CNTL2_BRES                                 = (0x01 << 6)  # determines the resolution of the acceleration data samples collected by the sample
		self.KX224_BUF_CNTL2_BFIE                                 = (0x01 << 5)  # buffer full interrupt enable bit
		self.KX224_BUF_CNTL2_SMP_TH8_9                            = (0x0C << 2)  # watermark level bits 8 and 9
		self.KX224_BUF_CNTL2_BUF_M_FIFO                           = (0x00 << 0)  # The buffer collects 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values and then stops collecting data, collecting new data only when the buffer is not full
		self.KX224_BUF_CNTL2_BUF_M_STREAM                         = (0x01 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data.
		self.KX224_BUF_CNTL2_BUF_M_TRIGGER                        = (0x02 << 0)  # When a trigger event occurs, the buffer holds the last data set of SMP[9:0] samples before the trigger event and then continues to collect data until full. New data is collected only when the buffer is not full.
		self.KX224_BUF_CNTL2_BUF_M_FILO                           = (0x03 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data. Reading from the buffer in this mode will return the most recent data first.
		self.KX224_BUF_STATUS_1_SMP_LEV0_7                        = (0xFF << 0)  
		self.KX224_BUF_STATUS_2_BUF_TRIG                          = (0x01 << 7)  # reports the status of the buffers trigger function if this mode has been selected
		self.KX224_BUF_STATUS_2_SMP_LEV8_10                       = (0x07 << 0)  # level High mask
		self.KX224_SELF_TEST_MEMS_TEST_OFF                        = (0x00 << 0)  # MEMS Test OFF
		self.KX224_SELF_TEST_MEMS_TEST_ON                         = (0xCA << 0)  # MEMS Test ON
		self.KX222_WHO_AM_I_WIA_ID                                = (0x2C << 0)  # WHO_AM_I -value for KX222
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KX224_SELF_TEST_MEMS_TEST={
			'ON':_b.KX224_SELF_TEST_MEMS_TEST_ON,
			'OFF':_b.KX224_SELF_TEST_MEMS_TEST_OFF,
		}
		self.KX224_BUF_CNTL2_BUF_M={
			'TRIGGER':_b.KX224_BUF_CNTL2_BUF_M_TRIGGER,
			'FILO':_b.KX224_BUF_CNTL2_BUF_M_FILO,
			'FIFO':_b.KX224_BUF_CNTL2_BUF_M_FIFO,
			'STREAM':_b.KX224_BUF_CNTL2_BUF_M_STREAM,
		}
		self.KX224_LP_CNTL_AVC={
			'4_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_4_SAMPLE_AVG,
			'16_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_16_SAMPLE_AVG,
			'8_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_8_SAMPLE_AVG,
			'NO_AVG':_b.KX224_LP_CNTL_AVC_NO_AVG,
			'128_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_128_SAMPLE_AVG,
			'2_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_2_SAMPLE_AVG,
			'64_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_64_SAMPLE_AVG,
			'32_SAMPLE_AVG':_b.KX224_LP_CNTL_AVC_32_SAMPLE_AVG,
		}
		self.KX224_CNTL3_OWUF={
			'25':_b.KX224_CNTL3_OWUF_25,
			'0P781':_b.KX224_CNTL3_OWUF_0P781,
			'12P5':_b.KX224_CNTL3_OWUF_12P5,
			'50':_b.KX224_CNTL3_OWUF_50,
			'1P563':_b.KX224_CNTL3_OWUF_1P563,
			'3P125':_b.KX224_CNTL3_OWUF_3P125,
			'100':_b.KX224_CNTL3_OWUF_100,
			'6P25':_b.KX224_CNTL3_OWUF_6P25,
		}
		self.KX224_INC5_PWSEL2={
			'50US_10US':_b.KX224_INC5_PWSEL2_50US_10US,
			'2XOSA':_b.KX224_INC5_PWSEL2_2XOSA,
			'4XOSA':_b.KX224_INC5_PWSEL2_4XOSA,
			'1XOSA':_b.KX224_INC5_PWSEL2_1XOSA,
		}
		self.KX224_FFCNTL_OFFI={
			'25':_b.KX224_FFCNTL_OFFI_25,
			'200':_b.KX224_FFCNTL_OFFI_200,
			'12P5':_b.KX224_FFCNTL_OFFI_12P5,
			'1600':_b.KX224_FFCNTL_OFFI_1600,
			'50':_b.KX224_FFCNTL_OFFI_50,
			'400':_b.KX224_FFCNTL_OFFI_400,
			'100':_b.KX224_FFCNTL_OFFI_100,
			'800':_b.KX224_FFCNTL_OFFI_800,
		}
		self.KX224_CNTL3_OTP={
			'1P563':_b.KX224_CNTL3_OTP_1P563,
			'12P5':_b.KX224_CNTL3_OTP_12P5,
			'6P25':_b.KX224_CNTL3_OTP_6P25,
			'50':_b.KX224_CNTL3_OTP_50,
		}
		self.KX224_ODCNTL_OSA={
			'200':_b.KX224_ODCNTL_OSA_200,
			'6400':_b.KX224_ODCNTL_OSA_6400,
			'0P781':_b.KX224_ODCNTL_OSA_0P781,
			'3200':_b.KX224_ODCNTL_OSA_3200,
			'12P5':_b.KX224_ODCNTL_OSA_12P5,
			'1600':_b.KX224_ODCNTL_OSA_1600,
			'50':_b.KX224_ODCNTL_OSA_50,
			'1P563':_b.KX224_ODCNTL_OSA_1P563,
			'25600':_b.KX224_ODCNTL_OSA_25600,
			'3P125':_b.KX224_ODCNTL_OSA_3P125,
			'25':_b.KX224_ODCNTL_OSA_25,
			'12800':_b.KX224_ODCNTL_OSA_12800,
			'400':_b.KX224_ODCNTL_OSA_400,
			'100':_b.KX224_ODCNTL_OSA_100,
			'800':_b.KX224_ODCNTL_OSA_800,
			'6P25':_b.KX224_ODCNTL_OSA_6P25,
		}
		self.KX224_COTR_DCSTR={
			'AFTER':_b.KX224_COTR_DCSTR_AFTER,
			'BEFORE':_b.KX224_COTR_DCSTR_BEFORE,
		}
		self.KX224_CNTL1_GSEL={
			'NA':_b.KX224_CNTL1_GSEL_NA,
			'16G':_b.KX224_CNTL1_GSEL_16G,
			'8G':_b.KX224_CNTL1_GSEL_8G,
			'32G':_b.KX224_CNTL1_GSEL_32G,
		}
		self.KX224_INC2_AOI={
			'AND':_b.KX224_INC2_AOI_AND,
			'OR':_b.KX224_INC2_AOI_OR,
		}
		self.KX224_CNTL3_OTDT={
			'200':_b.KX224_CNTL3_OTDT_200,
			'25':_b.KX224_CNTL3_OTDT_25,
			'12P5':_b.KX224_CNTL3_OTDT_12P5,
			'1600':_b.KX224_CNTL3_OTDT_1600,
			'50':_b.KX224_CNTL3_OTDT_50,
			'400':_b.KX224_CNTL3_OTDT_400,
			'100':_b.KX224_CNTL3_OTDT_100,
			'800':_b.KX224_CNTL3_OTDT_800,
		}
		self.KX224_INC1_PWSEL1={
			'50US_10US':_b.KX224_INC1_PWSEL1_50US_10US,
			'2XOSA':_b.KX224_INC1_PWSEL1_2XOSA,
			'4XOSA':_b.KX224_INC1_PWSEL1_4XOSA,
			'1XOSA':_b.KX224_INC1_PWSEL1_1XOSA,
		}
		self.KX224_INS2_TDTS={
			'DOUBLE':_b.KX224_INS2_TDTS_DOUBLE,
			'SINGLE':_b.KX224_INS2_TDTS_SINGLE,
			'NOTAP':_b.KX224_INS2_TDTS_NOTAP,
			'NA':_b.KX224_INS2_TDTS_NA,
		}
		self.KX224_ODCNTL_LPRO={
			'ODR_9':_b.KX224_ODCNTL_LPRO_ODR_9,
			'ODR_2':_b.KX224_ODCNTL_LPRO_ODR_2,
		}
class masks(register_base):
	def __init__(self):
		self.KX224_COTR_DCSTR_MASK                                = 0xFF         
		self.KX224_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KX224_INS2_TDTS_MASK                                 = 0x0C         # status of tap/double tap, bit is released when interrupt release register INT_REL is read.
		self.KX224_CNTL1_GSEL_MASK                                = 0x18         # selects the acceleration range of the accelerometer outputs
		self.KX224_CNTL3_OTP_MASK                                 = 0xC0         # sets the output data rate for the Tilt Position function
		self.KX224_CNTL3_OTDT_MASK                                = 0x38         # sets the output data rate for the Directional TapTM function
		self.KX224_CNTL3_OWUF_MASK                                = 0x07         # sets the output data rate for the general motion detection function and the high-pass filtered outputs
		self.KX224_ODCNTL_LPRO_MASK                               = 0x40         # low pass filter enable
		self.KX224_ODCNTL_OSA_MASK                                = 0x0F         # acceleration output data rate.
		self.KX224_INC1_PWSEL1_MASK                               = 0xC0         # Pulse interrupt 1 width configuration
		self.KX224_INC2_AOI_MASK                                  = 0x40         # AND OR configuration for motion detection
		self.KX224_INC2_WUE_MASK                                  = 0x3F         
		self.KX224_INC3_TM_MASK                                   = 0x3F         # tap directions
		self.KX224_INC5_PWSEL2_MASK                               = 0xC0         # Pulse interrupt 2 width configuration
		self.KX224_FFCNTL_OFFI_MASK                               = 0x07         # Output Data Rate at which the Free fall engine performs its function.
		self.KX224_HYST_SET_HYST_MASK                             = 0x3F         
		self.KX224_LP_CNTL_AVC_MASK                               = 0x70         # Averaging Filter Control
		self.KX224_BUF_CNTL1_SMP_TH0_MASK                         = 0xFF         
		self.KX224_BUF_CNTL1_SMP_TH0_7_MASK                       = 0xFF         
		self.KX224_BUF_CNTL2_SMP_TH8_MASK                         = 0x0C         
		self.KX224_BUF_CNTL2_SMP_TH8_9_MASK                       = 0x0C         
		self.KX224_BUF_CNTL2_BUF_M_MASK                           = 0x03         # selects the operating mode of the sample buffer
		self.KX224_BUF_STATUS_1_SMP_LEV0_MASK                     = 0xFF         
		self.KX224_BUF_STATUS_1_SMP_LEV0_7_MASK                   = 0xFF         
		self.KX224_BUF_STATUS_2_SMP_LEV8_MASK                     = 0x07         
		self.KX224_BUF_STATUS_2_SMP_LEV8_10_MASK                  = 0x07         
		self.KX224_SELF_TEST_MEMS_TEST_MASK                       = 0xFF         
		self.KX222_WHO_AM_I_WIA_MASK                              = 0xFF         