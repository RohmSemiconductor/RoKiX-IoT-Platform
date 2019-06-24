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
		self.KX126_MAN_ID                                         = 0x00         # A burst read (reading using the auto-increment) of 4 bytes starting at address 00, returns the manufacturing ID: "K" "i" "o" "n" in ascii codes "0x4B" "0x69" "0x6F" "0x6E"
		self.KX126_PART_ID                                        = 0x01         # A burst read (reading using the auto-increment) of 2 bytes starting at address 01, returns Who-Am-I value ("WAI") as the first byte (LSB) and a 2nd byte (MSB) that returns silicon specific ID.
		self.KX126_XHP_L                                          = 0x02         # x - hp filter output.
		self.KX126_XHP_H                                          = 0x03         # msb
		self.KX126_YHP_L                                          = 0x04         # y - hp filter output
		self.KX126_YHP_H                                          = 0x05         # msb
		self.KX126_ZHP_L                                          = 0x06         # z - hpfilteroutput
		self.KX126_ZHP_H                                          = 0x07         # msb
		self.KX126_XOUT_L                                         = 0x08         # output register x
		self.KX126_XOUT_H                                         = 0x09         # msb
		self.KX126_YOUT_L                                         = 0x0A         # output register y
		self.KX126_YOUT_H                                         = 0x0B         # msb
		self.KX126_ZOUT_L                                         = 0x0C         # output register z
		self.KX126_ZOUT_H                                         = 0x0D         # msb
		self.KX126_PED_STP_L                                      = 0x0E         # 16bit pedometer step counter register
		self.KX126_PED_STP_H                                      = 0x0F         # msb
		self.KX126_COTR                                           = 0x10         # The Command Test Response (COTR) register is used to verify proper integrated circuit functionality
		self.KX126_WHO_AM_I                                       = 0x11         # This register can be used for supplier recognition
		self.KX126_TSCP                                           = 0x12         # The Tilt Status Current Position (TSCP) register reports the current tilt position.
		self.KX126_TSPP                                           = 0x13         # The Tilt Status Previous Position (TSPP) register reports previous tilt position.
		self.KX126_INS1                                           = 0x14         # The Interrupt Source 1 (INS1) register contains 2 step counter interrupts and contains the Tap/Double-TapTM axis specific interrupts.
		self.KX126_INS2                                           = 0x15         # This Register tells witch function caused an interrupt.
		self.KX126_INS3                                           = 0x16         # The Interrupt Source 3 (INS3) register reports the interrupt status of the Wake-Up and Back-to-Sleep functions, as well as the axis and direction of the Wake-Up detected motion.
		self.KX126_STAT                                           = 0x17         # The Status Register reports the status of whether the interrupt is present.
		self.KX126_INT_REL                                        = 0x19         # Latched interrupt source information (INS1,INS2 except WMI/BFI and STAT when WMI/BFI is zero) is cleared and physical interrupt latched pin is changed to it's inactive state when this register is read.  Read value is dummy.
		self.KX126_CNTL1                                          = 0x1A         # Control register 1. Read/write control register that controls the main feature set.
		self.KX126_CNTL2                                          = 0x1B         # The Control 2 (CNTL2) register primarily controls tilt position state enabling.
		self.KX126_CNTL3                                          = 0x1C         # The Control 3 (CNTL3) register sets the output data rates for Tilt, Directional-TapTM, and the Motion Wake-Up digital engines.
		self.KX126_CNTL4                                          = 0x1D         # The Control 4 (CNTL4) register 4 provides more feature set control
		self.KX126_CNTL5                                          = 0x1E         # The Control 5 (CNTL5) register provides additional controls for wake-sleep engine
		self.KX126_ODCNTL                                         = 0x1F         # The ODR Control (ODCNTL) register is responsible for configuring Output Data Rate (ODR) and low-pass filter settings.
		self.KX126_INC1                                           = 0x20         # The Interrupt Control 1 (INC1) register controls the settings for the physical interrupt pin INT1, the Self-test function, and 3-wire SPI interface.
		self.KX126_INC2                                           = 0x21         # The Interrupt Control 2 (INC2) register controls which axis and direction of detected motion can cause an interrupt.
		self.KX126_INC3                                           = 0x22         # The Interrupt Control 3 (INC3) register controls which axis and direction of Tap/Double-TapTM can cause an interrupt.
		self.KX126_INC4                                           = 0x23         # The Interrupt Control 4 (INC4) register controls routing of an interrupt reporting to physical interrupt pin INT1.
		self.KX126_INC5                                           = 0x24         # The Interrupt Control 5 (INC5) register controls the settings for the physical interrupt pin INT2.
		self.KX126_INC6                                           = 0x25         # The Interrupt Control 6 (INC6) register controls routing of interrupt reporting to physical interrupt pin INT2.
		self.KX126_INC7                                           = 0x26         # The Interrupt Control 7 (INC7) register controls the pedometer (step counter) engine.
		self.KX126_TILT_TIMER                                     = 0x27         # Tilt Position State Timer. This register is the initial count register for Tilt Position State timer. (0 to 255).  New state must be valid as many measurement periods before change is accepted. Reset applied for any write to TSC with TPE enabled
		self.KX126_TDTRC                                          = 0x28         # The Tap/Double-TapTM Report Control (TDTRC) register is responsible for enabling/disabling reporting of Tap/Double-TapTM events.
		self.KX126_TDTC                                           = 0x29         # The Tap/Double-TapTM Counter (TDTC) register contains counter information for the detection of a double tap event.
		self.KX126_TTH                                            = 0x2A         # The Tap Threshold High (TTH) register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KX126_TTL                                            = 0x2B         # The Tap Threshold Low (TTL) register represents the 8-bit (0 255) jerk low threshold to determine if a tap is detected.
		self.KX126_FTD                                            = 0x2C         # This register contains counter information for the detection of any tap event.
		self.KX126_STD                                            = 0x2D         # This register contains counter information for the detection of a double tap event.
		self.KX126_TLT                                            = 0x2E         # This register contains counter information for the detection of a tap event.
		self.KX126_TWS                                            = 0x2F         # This register contains counter information for the detection of single and double taps.
		self.KX126_FFTH                                           = 0x30         # The Free Fall Threshold (FFTH) register contains the threshold of the Free fall detection.
		self.KX126_FFC                                            = 0x31         # The Free Fall Counter (FFC) register contains the counter setting of the Free fall detection.
		self.KX126_FFCNTL                                         = 0x32         # The Free Fall Control (FFCNTL) register contains the control setting of the Free fall detection.
		self.KX126_TILT_ANGLE_LL                                  = 0x34         # Tilt Angle Low Limit: This register sets the low-level threshold for tilt angle detection.
		self.KX126_TILT_ANGLE_HL                                  = 0x35         # Tilt Angle High Limit: This register sets the high-level threshold for tilt angle detection.
		self.KX126_HYST_SET                                       = 0x36         # This register sets the Hysteresis that is placed in between the Screen Rotation states.
		self.KX126_LP_CNTL                                        = 0x37         # Low Power Control
		self.KX126_WUFTH                                          = 0x3C         # Wake-up Function Threshold (WUFTH), Back-to-Sleep and Wake-Up Function Threshold (BTSWUFTH), and Back-to-Sleep Threshold (BTSTH) registers set the thresholds for Wake-up and Back-to-Sleep engines.
		self.KX126_BTSWUFTH                                       = 0x3D         # Wake-up Function Threshold (WUFTH), Back-to-Sleep and Wake-Up Function Threshold (BTSWUFTH), and Back-to-Sleep Threshold (BTSTH) registers set the thresholds for Wake-up and Back-to-Sleep engines.
		self.KX126_BTSTH                                          = 0x3E         # Wake-up Function Threshold (WUFTH), Back-to-Sleep and Wake-Up Function Threshold (BTSWUFTH), and Back-to-Sleep Threshold (BTSTH) registers set the thresholds for Wake-up and Back-to-Sleep engines.
		self.KX126_BTSC                                           = 0x3F         # This register is the initial count register for the BTS motion detection timer (0 to 255 counts)
		self.KX126_WUFC                                           = 0x40         # The Wake-Up Function Counter (WUFC) is the initial count register for the motion detection timer (0 to 255 counts)
		self.KX126_PED_STPWM_L                                    = 0x41         # Pedometer Step Counter Watermark Low and High registers set the 16-bit count value used as a watermark threshold for step counting.
		self.KX126_PED_STPWM_H                                    = 0x42         # msb
		self.KX126_PED_CNTL1                                      = 0x43         # Pedometer Control register 1 (PED_CNTL1). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL2                                      = 0x44         # Pedometer control register 2.
		self.KX126_PED_CNTL3                                      = 0x45         # Pedometer Control register 3 (PED_CNTL3).
		self.KX126_PED_CNTL4                                      = 0x46         # Pedometer Control register 4 (PED_CNTL4).
		self.KX126_PED_CNTL5                                      = 0x47         # Pedometer Control register 5 (PED_CNTL5). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL6                                      = 0x48         # Pedometer Control register 6 (PED_CNTL6). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL7                                      = 0x49         # Pedometer Control register 7 (PED_CNTL7).
		self.KX126_PED_CNTL8                                      = 0x4A         # Pedometer Control register 8 (PED_CNTL8). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL9                                      = 0x4B         # Pedometer Control register 9 (PED_CNTL9). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL10                                     = 0x4C         # Pedometer Control register 10 (PED_CNTL10). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_SELF_TEST                                      = 0x4D         # Self test initiation
		self.KX126_BUF_CNTL1                                      = 0x5A         # The Buffer Control 1 (BUF_CNTL1) register controls the buffer sample threshold
		self.KX126_BUF_CNTL2                                      = 0x5B         # The Buffer Control 2 (BUF_CNTL2) register controls sample buffer operation
		self.KX126_BUF_STATUS_1                                   = 0x5C         # Buffer Status: These register reports the status of the sample buffer.
		self.KX126_BUF_STATUS_2                                   = 0x5D         # Buffer Status: These register reports the status of the sample buffer.
		self.KX126_BUF_CLEAR                                      = 0x5E         # Latched buffer status information and the entire sample buffer are cleared when any data is written to this register.
		self.KX126_BUF_READ                                       = 0x5F         # Buffer output register
		self.KX127_WHO_AM_I                                       = 0x11         # This register can be used for supplier recognition
class bits(register_base):
	def __init__(self):
		self.KX126_COTR_DCSTR_BEFORE                              = (0x55 << 0)  # before set
		self.KX126_COTR_DCSTR_AFTER                               = (0xAA << 0)  # after set
		self.KX126_WHO_AM_I_WAI_ID                                = (0x38 << 0)  # WAI value for KX126
		self.KX126_TSCP_LE                                        = (0x01 << 5)  # LE - Left state X' negative (x-)
		self.KX126_TSCP_RI                                        = (0x01 << 4)  # RI - Right state X' positive (x+)
		self.KX126_TSCP_DO                                        = (0x01 << 3)  # DO - Down state Y' negative (y-)
		self.KX126_TSCP_UP                                        = (0x01 << 2)  # UP - Up state Y' positive (y+)
		self.KX126_TSCP_FD                                        = (0x01 << 1)  # FD - Face Down state Z negative (z-)
		self.KX126_TSCP_FU                                        = (0x01 << 0)  # FU - Face Up Z positive (z+)
		self.KX126_TSPP_LE                                        = (0x01 << 5)  # LE - Left state X' negative (x-)
		self.KX126_TSPP_RI                                        = (0x01 << 4)  # RI - Right state X' positive (x+)
		self.KX126_TSPP_DO                                        = (0x01 << 3)  # DO - Down state Y' negative (y-)
		self.KX126_TSPP_UP                                        = (0x01 << 2)  # UP - Up state Y' positive (y+)
		self.KX126_TSPP_FD                                        = (0x01 << 1)  # FD - Face Down state Z negative (z-)
		self.KX126_TSPP_FU                                        = (0x01 << 0)  # FU - Face Up Z positive (z+)
		self.KX126_INS1_STPOVI                                    = (0x01 << 7)  # STPOVI - Step counter Overflow interrupt
		self.KX126_INS1_STPWMI                                    = (0x01 << 6)  # STPWMI - Step counter Watermark Interrupt
		self.KX126_INS1_TLE                                       = (0x01 << 5)  # TLE - X' negative (x-)
		self.KX126_INS1_TRI                                       = (0x01 << 4)  # TRI - X' positive (x+)
		self.KX126_INS1_TDO                                       = (0x01 << 3)  # TDO - Y' negative (y-)
		self.KX126_INS1_TUP                                       = (0x01 << 2)  # TUP - Y' positive (y+)
		self.KX126_INS1_TFD                                       = (0x01 << 1)  # TFD - Z  negative (z-)
		self.KX126_INS1_TFU                                       = (0x01 << 0)  # TFU - Z  positive (z+)
		self.KX126_INS2_FFS                                       = (0x01 << 7)  # FFS - Freefall, 0=not in freefall state, 1=freefall is detected. FFS is released to 0 when INL is read.
		self.KX126_INS2_BFI                                       = (0x01 << 6)  # BFI - indicates buffer full interrupt.  Automatically cleared when buffer is read.
		self.KX126_INS2_WMI                                       = (0x01 << 5)  # WMI - Watermark interrupt, bit is set to one when FIFO has filled up to the value stored in the sample bits.This bit is automatically cleared when FIFO/FILO is read and the content returns to a value below the value stored in the sample bits.
		self.KX126_INS2_DRDY                                      = (0x01 << 4)  # DRDY - indicates that new acceleration data((00h,06h) to (00h,0Bh)) is available.  This bit is cleared when acceleration data is read or the interrupt release register (INL (00h,17h)) is read. 0= new acceleration data not available, 1= new acceleration data available
		self.KX126_INS2_TDTS_NOTAP                                = (0x00 << 2)  # 00 = no tap
		self.KX126_INS2_TDTS_SINGLE                               = (0x01 << 2)  # 01 = single tap
		self.KX126_INS2_TDTS_DOUBLE                               = (0x02 << 2)  # 10 = double tap
		self.KX126_INS2_TDTS_NA                                   = (0x03 << 2)  # 11 = does not exist
		self.KX126_INS2_STPINCI                                   = (0x01 << 1)  # STPINCI - Step counter increment interrupt
		self.KX126_INS2_TPS                                       = (0x01 << 0)  # TPS - Tilt Position status.  0=state not changed, 1=state changed.  TPS is released to 0 when INL is read.
		self.KX126_INS3_WUFS                                      = (0x01 << 7)  # WUFS - Wake up, This bit is cleared when the interrupt source latch register (INL (00h,1Ah)) is read. 1=Motion has activated the interrupt,  0= No motion
		self.KX126_INS3_BTS                                       = (0x01 << 6)  # BTS - Back to sleep interrupt
		self.KX126_INS3_XNWU                                      = (0x01 << 5)  # XNWU - X' negative (x-)
		self.KX126_INS3_XPWU                                      = (0x01 << 4)  # XPWU - X' positive (x+)
		self.KX126_INS3_YNWU                                      = (0x01 << 3)  # YNWU - Y' negative (y-)
		self.KX126_INS3_YPWU                                      = (0x01 << 2)  # YPWU - Y' positive (y+)
		self.KX126_INS3_ZNWU                                      = (0x01 << 1)  # ZNWU - Z  negative (z-)
		self.KX126_INS3_ZPWU                                      = (0x01 << 0)  # ZPWU - Z  positive (z+)
		self.KX126_STAT_INT                                       = (0x01 << 4)  # INT - reports the combined (OR) interrupt information of all features.  0= no interrupt event, 1= interrupt event has occurred.  When BFI and WMI in INS2 are 0, the INT bit is released to 0 when INL is read.  If WMI or BFI is 1, INT bit remains at 1 until they are cleared
		self.KX126_STAT_WAKE                                      = (0x01 << 0)  # wake - reports the wake or sleep state, 0=sleep , 1=wake
		self.KX126_CNTL1_PC1                                      = (0x01 << 7)  # PC1 - controls the operating mode.  0= stand-by mode,  1= operating mode.
		self.KX126_CNTL1_RES                                      = (0x01 << 6)  # RES - enables full power mode
		self.KX126_CNTL1_DRDYE                                    = (0x01 << 5)  # DRDYE - enables the reporting of the availability of new acceleration data ((00h,06h) to (00h,0Bh)) on the interrupt pin. 0= availability of new acceleration data not reflected on interrupt pin, 1= availability of new acceleration data reflected on interrupt pin.
		self.KX126_CNTL1_GSEL_2G                                  = (0x00 << 3)  # 00 = +/- 2g
		self.KX126_CNTL1_GSEL_4G                                  = (0x01 << 3)  # 01 = +/- 4g
		self.KX126_CNTL1_GSEL_8G                                  = (0x02 << 3)  # 1X = +/- 8g
		self.KX126_CNTL1_GSEL_8G_2                                = (0x03 << 3)  # 1X = +/- 8g
		self.KX126_CNTL1_TDTE                                     = (0x01 << 2)  # TDTE - enables the Tap / Double Tap function. 0 = disabled, 1 = enabled.
		self.KX126_CNTL1_PDE                                      = (0x01 << 1)  # PDE - enables Pedometer function
		self.KX126_CNTL1_TPE                                      = (0x01 << 0)  # TPE - enables the Tilt Position function. 0=disabled, 1 = enabled
		self.KX126_CNTL2_SRST                                     = (0x01 << 7)  # SRST - Soft Reset performs the POR routine. 0= no action. 1= start POR routine.
		self.KX126_CNTL2_COTC                                     = (0x01 << 6)  # COTC - Command test control. 0= no action, 1 sets AAh to STR @ 0Ch register, when STR register is read COTC is cleared and STR=55h.
		self.KX126_CNTL2_LEM                                      = (0x01 << 5)  # LEM - Tilt Left state mask
		self.KX126_CNTL2_RIM                                      = (0x01 << 4)  # RIM - Tilt Right state mask
		self.KX126_CNTL2_DOM                                      = (0x01 << 3)  # DOM - Tilt Down state mask
		self.KX126_CNTL2_UPM                                      = (0x01 << 2)  # UPM - Tilt Up state mask
		self.KX126_CNTL2_FDM                                      = (0x01 << 1)  # FDM - Tilt Face Down state mask
		self.KX126_CNTL2_FUM                                      = (0x01 << 0)  # FUM - Tilt Face Up state mask
		self.KX126_CNTL3_OTP_1P563                                = (0x00 << 6)  # 1.5Hz
		self.KX126_CNTL3_OTP_6P25                                 = (0x01 << 6)  # 6.25Hz
		self.KX126_CNTL3_OTP_12P5                                 = (0x02 << 6)  # 12.5Hz
		self.KX126_CNTL3_OTP_50                                   = (0x03 << 6)  # 50Hz
		self.KX126_CNTL3_OTDT_50                                  = (0x00 << 3)  # 50Hz
		self.KX126_CNTL3_OTDT_100                                 = (0x01 << 3)  # 100Hz
		self.KX126_CNTL3_OTDT_200                                 = (0x02 << 3)  # 200Hz
		self.KX126_CNTL3_OTDT_400                                 = (0x03 << 3)  # 400Hz
		self.KX126_CNTL3_OTDT_12P5                                = (0x04 << 3)  # 12.5Hz
		self.KX126_CNTL3_OTDT_25                                  = (0x05 << 3)  # 25Hz
		self.KX126_CNTL3_OTDT_800                                 = (0x06 << 3)  # 800Hz
		self.KX126_CNTL3_OTDT_1600                                = (0x07 << 3)  # 1600Hz
		self.KX126_CNTL3_OWUF_0P781                               = (0x00 << 0)  # 0.78Hz
		self.KX126_CNTL3_OWUF_1P563                               = (0x01 << 0)  # 1.563Hz
		self.KX126_CNTL3_OWUF_3P125                               = (0x02 << 0)  # 3.125Hz
		self.KX126_CNTL3_OWUF_6P25                                = (0x03 << 0)  # 6.25Hz
		self.KX126_CNTL3_OWUF_12P5                                = (0x04 << 0)  # 12.5Hz
		self.KX126_CNTL3_OWUF_25                                  = (0x05 << 0)  # 25Hz
		self.KX126_CNTL3_OWUF_50                                  = (0x06 << 0)  # 50Hz
		self.KX126_CNTL3_OWUF_100                                 = (0x07 << 0)  # 100Hz
		self.KX126_CNTL4_C_MODE                                   = (0x01 << 7)  # c_mode - Define debounce counter clear mode 0: clear 1: decrement
		self.KX126_CNTL4_TH_MODE                                  = (0x01 << 6)  # th_mode: 0: absolute threshold 1: relative threshold (default)
		self.KX126_CNTL4_WUFE                                     = (0x01 << 5)  # WUFE - enables the Wake Up (motion detect) function that will detect a general motion event. 0= disabled, 1= enabled.
		self.KX126_CNTL4_BTSE                                     = (0x01 << 4)  # BTSE - enables the Back to sleep function
		self.KX126_CNTL4_HPE                                      = (0x01 << 3)  # HPE - High-pass enable
		self.KX126_CNTL4_OBTS_0P781                               = (0x00 << 0)  # 000 = 0.78125Hz
		self.KX126_CNTL4_OBTS_1P563                               = (0x01 << 0)  # 001 = 1.5625Hz
		self.KX126_CNTL4_OBTS_3P125                               = (0x02 << 0)  # 010 = 3.125Hz
		self.KX126_CNTL4_OBTS_6P25                                = (0x03 << 0)  # 011 = 6.25Hz
		self.KX126_CNTL4_OBTS_12P5                                = (0x04 << 0)  # 100 = 12.5Hz
		self.KX126_CNTL4_OBTS_25                                  = (0x05 << 0)  # 101 = 25Hz
		self.KX126_CNTL4_OBTS_50                                  = (0x06 << 0)  # 110 = 50Hz
		self.KX126_CNTL4_OBTS_100                                 = (0x07 << 0)  # 111 = 100Hz
		self.KX126_CNTL5_MAN_WAKE                                 = (0x01 << 1)  # The manual wake overwrite bit
		self.KX126_CNTL5_MAN_SLEEP                                = (0x01 << 0)  # The manual sleep overwrite bit
		self.KX126_ODCNTL_IIR_BYPASS                              = (0x01 << 7)  # IIR_BYPASS - IIR filter bypass mode for debugging averaging filter.
		self.KX126_ODCNTL_LPRO                                    = (0x01 << 6)  # LPRO - Low pass filter roll off control, 0=ODR/9, 1=ODR/2
		self.KX126_ODCNTL_OSA_12P5                                = (0x00 << 0)  # 0000 = 12.5Hz Low power mode available
		self.KX126_ODCNTL_OSA_25                                  = (0x01 << 0)  # 0001 = 25Hz  Low power mode available
		self.KX126_ODCNTL_OSA_50                                  = (0x02 << 0)  # 0010 = 50Hz  Low power mode available
		self.KX126_ODCNTL_OSA_100                                 = (0x03 << 0)  # 0011 = 100Hz  Low power mode available
		self.KX126_ODCNTL_OSA_200                                 = (0x04 << 0)  # 0100 = 200Hz  Low power mode available
		self.KX126_ODCNTL_OSA_400                                 = (0x05 << 0)  # 0101 = 400Hz
		self.KX126_ODCNTL_OSA_800                                 = (0x06 << 0)  # 0110 = 800Hz
		self.KX126_ODCNTL_OSA_1600                                = (0x07 << 0)  # 0111 = 1600Hz
		self.KX126_ODCNTL_OSA_0P781                               = (0x08 << 0)  # 1000 = 0.781Hz  Low power mode available
		self.KX126_ODCNTL_OSA_1P563                               = (0x09 << 0)  # 1001 = 1.563Hz  Low power mode available
		self.KX126_ODCNTL_OSA_3P125                               = (0x0A << 0)  # 1010 = 3.125Hz  Low power mode available
		self.KX126_ODCNTL_OSA_6P25                                = (0x0B << 0)  # 1011 = 6.25Hz  Low power mode available
		self.KX126_ODCNTL_OSA_3200                                = (0x0C << 0)  # 1100 = 3200Hz
		self.KX126_ODCNTL_OSA_6400                                = (0x0D << 0)  # 1101 = 6400Hz
		self.KX126_ODCNTL_OSA_12800                               = (0x0E << 0)  # 1110 = 12800Hz
		self.KX126_ODCNTL_OSA_25600                               = (0x0F << 0)  # 1111 = 25600Hz
		self.KX126_INC1_PW1_50US_10US                             = (0x00 << 6)  # 0 : default width - 50us(10us when ODR>1600Hz)
		self.KX126_INC1_PW1_1XODR                                 = (0x01 << 6)  # width 1*ODR period
		self.KX126_INC1_PW1_2XODR                                 = (0x02 << 6)  # width 2*ODR period
		self.KX126_INC1_PW1_4XODR                                 = (0x03 << 6)  # width 4*ODR period
		self.KX126_INC1_IEN1                                      = (0x01 << 5)  # IEN1 - Enable/disable physical interrupt pin 1, 0=disable, 1=enable.
		self.KX126_INC1_IEA1                                      = (0x01 << 4)  # IEA1 - Interrupt active level control for interrupt pin 1, 0=active low, 1=active high.
		self.KX126_INC1_IEL1                                      = (0x01 << 3)  # IEL1 - Interrupt latch control for interrupt pin 1, 0=latched, 1=one pulse
		self.KX126_INC1_STPOL                                     = (0x01 << 1)  # STPOL - ST polarity, This bit is ignored when STNULL is set.
		self.KX126_INC1_SPI3E                                     = (0x01 << 0)  # SPI3E - 3-wired SPI interface, 0=disable, 1=enable.
		self.KX126_INC2_AOI_OR                                    = (0x00 << 6)  # 0=Or combination of selected directions
		self.KX126_INC2_AOI_AND                                   = (0x01 << 6)  # 1=And combination of selected axes
		self.KX126_INC2_AOI                                       = (0x01 << 6)  # AOI - And-Or configuration, 0=Or combination of selected directions, 1=And combination of selected axes
		self.KX126_INC2_XNWUE                                     = (0x01 << 5)  # XNWUE - x negative (x-) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC2_XPWUE                                     = (0x01 << 4)  # XPWUE - x positive (x+) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC2_YNWUE                                     = (0x01 << 3)  # YNWUE - y negative (y-) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC2_YPWUE                                     = (0x01 << 2)  # YPWUE - y positive (y+) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC2_ZNWUE                                     = (0x01 << 1)  # ZNWUE - z negative (z-) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC2_ZPWUE                                     = (0x01 << 0)  # ZPWUE - z positive (z+) mask for WUF, 0=disable, 1=enable.
		self.KX126_INC3_TMEN                                      = (0x01 << 6)  # enables/disables alternate tap masking scheme
		self.KX126_INC3_TLEM                                      = (0x01 << 5)  # x negative (x-): 0 = disabled, 1 = enabled
		self.KX126_INC3_TRIM                                      = (0x01 << 4)  # x positive (x+): 0 = disabled, 1 = enabled
		self.KX126_INC3_TDOM                                      = (0x01 << 3)  # y negative (y-): 0 = disabled, 1 = enabled
		self.KX126_INC3_TUPM                                      = (0x01 << 2)  # y positive (y+): 0 = disabled, 1 = enabled
		self.KX126_INC3_TFDM                                      = (0x01 << 1)  # z negative (z-): 0 = disabled, 1 = enabled
		self.KX126_INC3_TFUM                                      = (0x01 << 0)  # z positive (z+): 0 = disabled, 1 = enabled
		self.KX126_INC4_FFI1                                      = (0x01 << 7)  # FFI1 - Freefall interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_BFI1                                      = (0x01 << 6)  # BFI1 - Buffer full interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_WMI1                                      = (0x01 << 5)  # WMI1 - Watermark interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_DRDYI1                                    = (0x01 << 4)  # DRDYI1 - Data ready interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_BTSI1                                     = (0x01 << 3)  # BTSI1 - Back to sleep interrupt reported in interrupt pin 1
		self.KX126_INC4_TDTI1                                     = (0x01 << 2)  # TDTI1 - Tap/Double Tap interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_WUFI1                                     = (0x01 << 1)  # WUFI1 - Wake Up (motion detect) interrupt reported pn physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC4_TPI1                                      = (0x01 << 0)  # TPI1 - Tilt position interrupt reported on physical interrupt pin 1, 0=disable, 1=enable (and IEN1=1).
		self.KX126_INC5_PW2_50US_10US                             = (0x00 << 6)  # 0 : default width - 50us(10us when ODR>1600Hz)
		self.KX126_INC5_PW2_1XODR                                 = (0x01 << 6)  # width 1*ODR period
		self.KX126_INC5_PW2_2XODR                                 = (0x02 << 6)  # width 2*ODR period
		self.KX126_INC5_PW2_4XODR                                 = (0x03 << 6)  # width 4*ODR period
		self.KX126_INC5_IEN2                                      = (0x01 << 5)  # IEN2 - Enable/disable physical interrupt pin 2, 0=disable, 1=enable.
		self.KX126_INC5_IEA2                                      = (0x01 << 4)  # IEA2 - Interrupt active level control for interrupt pin 2, 0=active low, 1=active high.
		self.KX126_INC5_IEL2                                      = (0x01 << 3)  # IEL2 - Interrupt latch control for interrupt pin 2, 0=latched, 1=one pulse
		self.KX126_INC5_ACLR2                                     = (0x01 << 1)  # ACLR2 - Auto interrupt clear(same as INL) for the following event, only available in pulse interrupt mode, 0=disable, 1=enable.
		self.KX126_INC5_ACLR1                                     = (0x01 << 0)  # ACLR1 - Auto interrupt clear(same as INL) for the following event, only available in pulse interrupt mode, 0=disable, 1=enable.
		self.KX126_INC6_FFI2                                      = (0x01 << 7)  # FFI2 - Freefall interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_BFI2                                      = (0x01 << 6)  # BFI2 - Buffer full interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_WMI2                                      = (0x01 << 5)  # WMI2 - Watermark interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_DRDYI2                                    = (0x01 << 4)  # DRDYI2 - Data ready interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_BTSI2                                     = (0x01 << 3)  # BTSI2 - Back to sleep interrupt reported in interrupt pin 2
		self.KX126_INC6_TDTI2                                     = (0x01 << 2)  # TDTI2 - Tap/Double Tap interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_WUFI2                                     = (0x01 << 1)  # WUFI2 - Wake Up (motion detect) interrupt reported pn physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC6_TPI2                                      = (0x01 << 0)  # TPI2 - Tilt position interrupt reported on physical interrupt pin 2, 0=disable, 1=enable (and IEN2=1).
		self.KX126_INC7_STPOVI2                                   = (0x01 << 6)  # STPOVI2 - Step counter overflow interrupt on interrupt pin 2
		self.KX126_INC7_STPWMI2                                   = (0x01 << 5)  # STPWMI2 - Step counter watermark interrupt on interrupt pin 2
		self.KX126_INC7_STPINCI2                                  = (0x01 << 4)  # STPINCI2 - Step counter increment interrupt on interrupt pin 2
		self.KX126_INC7_STPOVI1                                   = (0x01 << 2)  # STPOVI1 - Step counter overflow interrupt on interrupt pin 1
		self.KX126_INC7_STPWMI1                                   = (0x01 << 1)  # STPWMI1 - Step counter watermark interrupt on interrupt pin 1
		self.KX126_INC7_STPINCI1                                  = (0x01 << 0)  # STPINCI1 - Step counter increment interrupt on interrupt pin 1
		self.KX126_TDTRC_DTRE                                     = (0x01 << 1)  # DTRE - Double tap report Enable.  When DTRE is set to 1, update INS1 and DTDS in INS2 with double tap events. When DTRE is set to 0, do not update INS1 or DTDS if double tap occurs.
		self.KX126_TDTRC_STRE                                     = (0x01 << 0)  # STRE - Single tap report Enable.  When STRE is set to 1, update INS1 and DTDS in INS2 single tap events. When DTRE is set to 0, do not update INS1 or DTDS if single tap occurs.
		self.KX126_FFCNTL_FFIE                                    = (0x01 << 7)  # FFIE - Freefall engine enable, 0=disabled, 1=enabled.
		self.KX126_FFCNTL_ULMODE                                  = (0x01 << 6)  # ULMODE - Interrupt latch/un-latch control, 0=latched, 1=unlatched.
		self.KX126_FFCNTL_DCRM                                    = (0x01 << 3)  # DCRM - Debounce methodology control, 0=count up/down, 1=count up/reset.
		self.KX126_FFCNTL_OFFI_12P5                               = (0x00 << 0)  # 000 = 12.5Hz
		self.KX126_FFCNTL_OFFI_25                                 = (0x01 << 0)  # 001 = 25Hz
		self.KX126_FFCNTL_OFFI_50                                 = (0x02 << 0)  # 010 = 50Hz
		self.KX126_FFCNTL_OFFI_100                                = (0x03 << 0)  # 011 = 100Hz
		self.KX126_FFCNTL_OFFI_200                                = (0x04 << 0)  # 100 = 200Hz
		self.KX126_FFCNTL_OFFI_400                                = (0x05 << 0)  # 101 = 400Hz
		self.KX126_FFCNTL_OFFI_800                                = (0x06 << 0)  # 110 = 800Hz
		self.KX126_FFCNTL_OFFI_1600                               = (0x07 << 0)  # 111 = 1600Hz
		self.KX126_LP_CNTL_AVC_NO_AVG                             = (0x00 << 4)  # No Averaging
		self.KX126_LP_CNTL_AVC_2_SAMPLE_AVG                       = (0x01 << 4)  # 2 Samples Averaged
		self.KX126_LP_CNTL_AVC_4_SAMPLE_AVG                       = (0x02 << 4)  # 4 Samples Averaged
		self.KX126_LP_CNTL_AVC_8_SAMPLE_AVG                       = (0x03 << 4)  # 8 Samples Averaged
		self.KX126_LP_CNTL_AVC_16_SAMPLE_AVG                      = (0x04 << 4)  # 16 Samples Averaged (default)
		self.KX126_LP_CNTL_AVC_32_SAMPLE_AVG                      = (0x05 << 4)  # 32 Samples Averaged
		self.KX126_LP_CNTL_AVC_64_SAMPLE_AVG                      = (0x06 << 4)  # 64 Samples Averaged
		self.KX126_LP_CNTL_AVC_128_SAMPLE_AVG                     = (0x07 << 4)  # 128 Samples Averaged
		self.KX126_PED_CNTL1_STP_TH_NO_STEP                       = (0x00 << 4)  # No threshold count for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_2                        = (0x01 << 4)  # 2 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_4                        = (0x02 << 4)  # 4 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_6                        = (0x03 << 4)  # 6 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_8                        = (0x04 << 4)  # 8 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_10                       = (0x05 << 4)  # 10 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_12                       = (0x06 << 4)  # 12 step threshold for start counting
		self.KX126_PED_CNTL1_STP_TH_STEP_14                       = (0x07 << 4)  # 14 step threshold for start counting
		self.KX126_PED_CNTL2_PED_ODR_50                           = (0x06 << 0)  # Pedometer ODR 50Hz
		self.KX126_PED_CNTL2_PED_ODR_100                          = (0x0C << 0)  # Pedometer ODR 100Hz
		self.KX126_PED_CNTL3_FCA_1                                = (0x00 << 0)  # Scaling factor 1
		self.KX126_PED_CNTL3_FCA_2                                = (0x01 << 0)  # Scaling factor 2
		self.KX126_PED_CNTL3_FCA_4                                = (0x02 << 0)  # Scaling factor 4
		self.KX126_PED_CNTL3_FCA_8                                = (0x03 << 0)  # Scaling factor 8
		self.KX126_PED_CNTL3_FCA_16                               = (0x04 << 0)  # Scaling factor 16
		self.KX126_PED_CNTL3_FCA_32                               = (0x05 << 0)  # Scaling factor 32
		self.KX126_PED_CNTL3_FCA_64                               = (0x06 << 0)  # Scaling factor 64
		self.KX126_PED_CNTL3_FCA_128                              = (0x07 << 0)  # Scaling factor 128
		self.KX126_BUF_CNTL2_BUFE                                 = (0x01 << 7)  # controls activation of the sample buffer
		self.KX126_BUF_CNTL2_BRES                                 = (0x01 << 6)  # determines the resolution of the acceleration data samples collected by the sample
		self.KX126_BUF_CNTL2_BFIE                                 = (0x01 << 5)  # buffer full interrupt enable bit
		self.KX126_BUF_CNTL2_BUF_BM_FIFO                          = (0x00 << 0)  # The buffer collects 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values and then stops collecting data, collecting new data only when the buffer is not full
		self.KX126_BUF_CNTL2_BUF_BM_STREAM                        = (0x01 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data.
		self.KX126_BUF_CNTL2_BUF_BM_TRIGGER                       = (0x02 << 0)  # When a trigger event occurs, the buffer holds the last data set of SMP[9:0] samples before the trigger event and then continues to collect data until full. New data is collected only when the buffer is not full.
		self.KX126_BUF_CNTL2_BUF_BM_FILO                          = (0x03 << 0)  # The buffer holds the last 681 sets of 8-bit low resolution values or 339 sets of 16-bit high resolution values. Once the buffer is full, the oldest data is discarded to make room for newer data. Reading from the buffer in this mode will return the most recent data first.
		self.KX126_BUF_STATUS_2_BUF_TRIG                          = (0x01 << 7)  # reports the status of the buffers trigger function if this mode has been selected
		self.KX127_WHO_AM_I_WAI_ID                                = (0x3B << 0)  # WAI value for KX127
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KX126_ODCNTL_OSA={
			'200':_b.KX126_ODCNTL_OSA_200,
			'6400':_b.KX126_ODCNTL_OSA_6400,
			'0P781':_b.KX126_ODCNTL_OSA_0P781,
			'3200':_b.KX126_ODCNTL_OSA_3200,
			'12P5':_b.KX126_ODCNTL_OSA_12P5,
			'1600':_b.KX126_ODCNTL_OSA_1600,
			'50':_b.KX126_ODCNTL_OSA_50,
			'1P563':_b.KX126_ODCNTL_OSA_1P563,
			'25600':_b.KX126_ODCNTL_OSA_25600,
			'3P125':_b.KX126_ODCNTL_OSA_3P125,
			'25':_b.KX126_ODCNTL_OSA_25,
			'12800':_b.KX126_ODCNTL_OSA_12800,
			'400':_b.KX126_ODCNTL_OSA_400,
			'100':_b.KX126_ODCNTL_OSA_100,
			'800':_b.KX126_ODCNTL_OSA_800,
			'6P25':_b.KX126_ODCNTL_OSA_6P25,
		}
		self.KX126_PED_CNTL3_FCA={
			'16':_b.KX126_PED_CNTL3_FCA_16,
			'32':_b.KX126_PED_CNTL3_FCA_32,
			'1':_b.KX126_PED_CNTL3_FCA_1,
			'2':_b.KX126_PED_CNTL3_FCA_2,
			'64':_b.KX126_PED_CNTL3_FCA_64,
			'4':_b.KX126_PED_CNTL3_FCA_4,
			'128':_b.KX126_PED_CNTL3_FCA_128,
			'8':_b.KX126_PED_CNTL3_FCA_8,
		}
		self.KX126_PED_CNTL2_PED_ODR={
			'100':_b.KX126_PED_CNTL2_PED_ODR_100,
			'50':_b.KX126_PED_CNTL2_PED_ODR_50,
		}
		self.KX126_INC2_AOI={
			'AND':_b.KX126_INC2_AOI_AND,
			'OR':_b.KX126_INC2_AOI_OR,
		}
		self.KX126_CNTL3_OWUF={
			'25':_b.KX126_CNTL3_OWUF_25,
			'0P781':_b.KX126_CNTL3_OWUF_0P781,
			'12P5':_b.KX126_CNTL3_OWUF_12P5,
			'50':_b.KX126_CNTL3_OWUF_50,
			'1P563':_b.KX126_CNTL3_OWUF_1P563,
			'3P125':_b.KX126_CNTL3_OWUF_3P125,
			'100':_b.KX126_CNTL3_OWUF_100,
			'6P25':_b.KX126_CNTL3_OWUF_6P25,
		}
		self.KX126_CNTL3_OTDT={
			'200':_b.KX126_CNTL3_OTDT_200,
			'25':_b.KX126_CNTL3_OTDT_25,
			'12P5':_b.KX126_CNTL3_OTDT_12P5,
			'1600':_b.KX126_CNTL3_OTDT_1600,
			'50':_b.KX126_CNTL3_OTDT_50,
			'400':_b.KX126_CNTL3_OTDT_400,
			'100':_b.KX126_CNTL3_OTDT_100,
			'800':_b.KX126_CNTL3_OTDT_800,
		}
		self.KX126_INC1_PW1={
			'50US_10US':_b.KX126_INC1_PW1_50US_10US,
			'4XODR':_b.KX126_INC1_PW1_4XODR,
			'1XODR':_b.KX126_INC1_PW1_1XODR,
			'2XODR':_b.KX126_INC1_PW1_2XODR,
		}
		self.KX126_PED_CNTL1_STP_TH={
			'NO_STEP':_b.KX126_PED_CNTL1_STP_TH_NO_STEP,
			'STEP_2':_b.KX126_PED_CNTL1_STP_TH_STEP_2,
			'STEP_10':_b.KX126_PED_CNTL1_STP_TH_STEP_10,
			'STEP_14':_b.KX126_PED_CNTL1_STP_TH_STEP_14,
			'STEP_12':_b.KX126_PED_CNTL1_STP_TH_STEP_12,
			'STEP_8':_b.KX126_PED_CNTL1_STP_TH_STEP_8,
			'STEP_6':_b.KX126_PED_CNTL1_STP_TH_STEP_6,
			'STEP_4':_b.KX126_PED_CNTL1_STP_TH_STEP_4,
		}
		self.KX126_INC5_PW2={
			'50US_10US':_b.KX126_INC5_PW2_50US_10US,
			'4XODR':_b.KX126_INC5_PW2_4XODR,
			'1XODR':_b.KX126_INC5_PW2_1XODR,
			'2XODR':_b.KX126_INC5_PW2_2XODR,
		}
		self.KX126_FFCNTL_OFFI={
			'25':_b.KX126_FFCNTL_OFFI_25,
			'200':_b.KX126_FFCNTL_OFFI_200,
			'12P5':_b.KX126_FFCNTL_OFFI_12P5,
			'1600':_b.KX126_FFCNTL_OFFI_1600,
			'50':_b.KX126_FFCNTL_OFFI_50,
			'400':_b.KX126_FFCNTL_OFFI_400,
			'100':_b.KX126_FFCNTL_OFFI_100,
			'800':_b.KX126_FFCNTL_OFFI_800,
		}
		self.KX126_CNTL1_GSEL={
			'8G_2':_b.KX126_CNTL1_GSEL_8G_2,
			'4G':_b.KX126_CNTL1_GSEL_4G,
			'2G':_b.KX126_CNTL1_GSEL_2G,
			'8G':_b.KX126_CNTL1_GSEL_8G,
		}
		self.KX126_CNTL3_OTP={
			'1P563':_b.KX126_CNTL3_OTP_1P563,
			'12P5':_b.KX126_CNTL3_OTP_12P5,
			'6P25':_b.KX126_CNTL3_OTP_6P25,
			'50':_b.KX126_CNTL3_OTP_50,
		}
		self.KX126_BUF_CNTL2_BUF_BM={
			'TRIGGER':_b.KX126_BUF_CNTL2_BUF_BM_TRIGGER,
			'FILO':_b.KX126_BUF_CNTL2_BUF_BM_FILO,
			'FIFO':_b.KX126_BUF_CNTL2_BUF_BM_FIFO,
			'STREAM':_b.KX126_BUF_CNTL2_BUF_BM_STREAM,
		}
		self.KX126_LP_CNTL_AVC={
			'4_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_4_SAMPLE_AVG,
			'16_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_16_SAMPLE_AVG,
			'8_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_8_SAMPLE_AVG,
			'NO_AVG':_b.KX126_LP_CNTL_AVC_NO_AVG,
			'128_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_128_SAMPLE_AVG,
			'2_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_2_SAMPLE_AVG,
			'64_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_64_SAMPLE_AVG,
			'32_SAMPLE_AVG':_b.KX126_LP_CNTL_AVC_32_SAMPLE_AVG,
		}
		self.KX126_COTR_DCSTR={
			'AFTER':_b.KX126_COTR_DCSTR_AFTER,
			'BEFORE':_b.KX126_COTR_DCSTR_BEFORE,
		}
		self.KX126_INS2_TDTS={
			'DOUBLE':_b.KX126_INS2_TDTS_DOUBLE,
			'SINGLE':_b.KX126_INS2_TDTS_SINGLE,
			'NOTAP':_b.KX126_INS2_TDTS_NOTAP,
			'NA':_b.KX126_INS2_TDTS_NA,
		}
		self.KX126_CNTL4_OBTS={
			'25':_b.KX126_CNTL4_OBTS_25,
			'0P781':_b.KX126_CNTL4_OBTS_0P781,
			'12P5':_b.KX126_CNTL4_OBTS_12P5,
			'50':_b.KX126_CNTL4_OBTS_50,
			'1P563':_b.KX126_CNTL4_OBTS_1P563,
			'3P125':_b.KX126_CNTL4_OBTS_3P125,
			'100':_b.KX126_CNTL4_OBTS_100,
			'6P25':_b.KX126_CNTL4_OBTS_6P25,
		}
class masks(register_base):
	def __init__(self):
		self.KX126_COTR_DCSTR_MASK                                = 0xFF         # Command Test Response
		self.KX126_WHO_AM_I_WAI_MASK                              = 0xFF         # WAI value for KX126
		self.KX126_INS2_TDTS_MASK                                 = 0x0C         # TDTS(1,0) - status of tap/double tap, bit is released when interrupt latch release register (INL (00h,17h)) is read.
		self.KX126_CNTL1_GSEL_MASK                                = 0x18         # Gsel - Selectable g-range bits
		self.KX126_CNTL3_OTP_MASK                                 = 0xC0         # sets the output data rate for the Tilt Position function
		self.KX126_CNTL3_OTDT_MASK                                = 0x38         # sets the output data rate for the Directional TapTM function
		self.KX126_CNTL3_OWUF_MASK                                = 0x07         # sets the output data rate for the general motion detection function and the high-pass filtered outputs
		self.KX126_CNTL4_OBTS_MASK                                = 0x07         # OBTS<2:0> - Back to sleep function output data rate
		self.KX126_ODCNTL_OSA_MASK                                = 0x0F         # OSA<3:0> - Acceleration Output data rate.* Low power mode available, all other data rates will default to full power mode.
		self.KX126_INC1_PW1_MASK                                  = 0xC0         # Pulse interrupt 1 width configuration.
		self.KX126_INC2_AOI_MASK                                  = 0x40         # AOI - And-Or configuration, 0=Or combination of selected directions, 1=And combination of selected axes
		self.KX126_INC5_PW2_MASK                                  = 0xC0         # PW2 - Pulse interrupt width on INT2
		self.KX126_TILT_TIMER_TSC_MASK                            = 0xFF         # Tilt Position State Timer. This register is the initial count register for Tilt Position State timer. (0 to 255).  New state must be valid as many measurement periods before change is accepted. Reset applied for any write to TSC with TPE enabled
		self.KX126_TDTC_TDTC_MASK                                 = 0xFF         # The Tap/Double-TapTM Counter (TDTC) register contains counter information for the detection of a double tap event.
		self.KX126_TTH_TTH_MASK                                   = 0xFF         # The Tap Threshold High (TTH) register represents the 8-bit jerk high threshold to determine if a tap is detected.
		self.KX126_TTL_TTL_MASK                                   = 0xFF         # The Tap Threshold Low (TTL) register represents the 8-bit (0 255) jerk low threshold to determine if a tap is detected.
		self.KX126_FTD_FTD_MASK                                   = 0xFF         # This register contains counter information for the detection of any tap event.
		self.KX126_STD_STD_MASK                                   = 0xFF         # This register contains counter information for the detection of a double tap event.
		self.KX126_TLT_TLT_MASK                                   = 0xFF         # This register contains counter information for the detection of a tap event.
		self.KX126_TWS_TWS_MASK                                   = 0xFF         # This register contains counter information for the detection of single and double taps.
		self.KX126_FFTH_FFTH_MASK                                 = 0xFF         # The Free Fall Threshold (FFTH) register contains the threshold of the Free fall detection.
		self.KX126_FFC_FFC_MASK                                   = 0xFF         # The Free Fall Counter (FFC) register contains the counter setting of the Free fall detection.
		self.KX126_FFCNTL_OFFI_MASK                               = 0x07         # OFFI<2:0> - Freefall function output data rate
		self.KX126_TILT_ANGLE_LL_LL_MASK                          = 0xFF         # Tilt Angle Low Limit: This register sets the low-level threshold for tilt angle detection.
		self.KX126_TILT_ANGLE_HL_HL_MASK                          = 0xFF         # Tilt Angle High Limit: This register sets the high-level threshold for tilt angle detection.
		self.KX126_HYST_SET_HYST_MASK                             = 0xFF         # This register sets the Hysteresis that is placed in between the Screen Rotation states.
		self.KX126_LP_CNTL_AVC_MASK                               = 0x70         # Averaging Filter Control
		self.KX126_BTSWUFTH_BTSTH8_10_MASK                        = 0x70         # msb part of BTS threshold
		self.KX126_BTSWUFTH_WUFTH8_10_MASK                        = 0x07         # msb part of WUF threshold
		self.KX126_BTSC_BTSC_MASK                                 = 0xFF         # This register is the initial count register for the BTS motion detection timer (0 to 255 counts)
		self.KX126_WUFC_WUFC_MASK                                 = 0xFF         # The Wake-Up Function Counter (WUFC) is the initial count register for the motion detection timer (0 to 255 counts)
		self.KX126_PED_STPWM_L_PED_STPWM_L_MASK                   = 0xFF         # Pedometer Step Counter Watermark Low and High registers set the 16-bit count value used as a watermark threshold for step counting.
		self.KX126_PED_STPWM_H_PED_STPWM_H_MASK                   = 0xFF         # msb
		self.KX126_PED_CNTL1_STP_TH_MASK                          = 0x70         # STP_TH<2:0> ; A threshold for discarding counting if not enough steps coming. Values: 0, 1, ..., 7. -> 0, 1, 2, 4, ..., 15. Reset applied for any write to PED_CNTL1 with PDE enabled
		self.KX126_PED_CNTL1_MAG_SCALE_MASK                       = 0x0F         # MAG_SCALE<3:0>. Scaling factor for the input signal (x,y,z). Bit shift. Values: 16 bit data, 6; 12 bit data, 1; Reset applied for any write to PED_CNTL1 with PDE enabled
		self.KX126_PED_CNTL2_HPS_MASK                             = 0x70         # hps = 3. Scaling factor for the output from the high-pass filter. Bit shift operation. Values: 0, 1, ..., 7. -> 1, 2, ..., 128. Reset applied for any write to PED_CNTL2 with PDE enabled
		self.KX126_PED_CNTL2_PED_ODR_MASK                         = 0x0F         # The length of the low-pass filter (as ODR 50 or 100Hz)
		self.KX126_PED_CNTL3_FCB_MASK                             = 0x38         # Scaling factor inside high-pass filter
		self.KX126_PED_CNTL3_FCA_MASK                             = 0x07         # Scaling factor inside high-pass filter
		self.KX126_PED_CNTL4_B_CNT_MASK                           = 0x70         # B_CNT<2:0> below_count[2:0] = 2; Samples below the zero threshold before setting e.g. Area == 0. Originally this was 0 samples. Values: 0, 1, ..., 7. -> 0, 2, 4, ..., 14. Reset applied for any write to PED_CNTL4 with PDE enabled
		self.KX126_PED_CNTL4_A_H_MASK                             = 0x0F         # A_h = 15;  // Maximum area of the peak (maximum impact from the floor). Values: 0, 1, ..., 15: with Ah_fc -> 0, 1024, ..., 15360.  Reset applied for any write to PED_CNTL4 with PDE enabled
		self.KX126_PED_CNTL5_A_L_MASK                             = 0xFF         # Pedometer Control register 5 (PED_CNTL5). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL6_M_H5_MASK                            = 0x3F         # Maximum time interval for the peak
		self.KX126_PED_CNTL7_M_L_MASK                             = 0xFF         # Pedometer Control register 7 (PED_CNTL7).
		self.KX126_PED_CNTL8_T_L_MASK                             = 0xFF         # Pedometer Control register 8 (PED_CNTL8). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL9_T_M_MASK                             = 0xFF         # Pedometer Control register 9 (PED_CNTL9). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_PED_CNTL10_T_P_MASK                            = 0xFF         # Pedometer Control register 10 (PED_CNTL10). The setting of this register is affected by pedometer engine ODR selection.
		self.KX126_SELF_TEST_MEMS_TEST_MASK                       = 0xFF         # When 0xCA is written to this register, the MEMS self-test function is enabled. Electrostatic-actuation of the accelerometer, results in a DC shift of the X, Y and Z axis outputs. Writing 0x00 to this register will return the accelerometer to normal operation
		self.KX126_BUF_CNTL2_SMP_TH8_9_MASK                       = 0x0C         # buffer sample control threshold msb
		self.KX126_BUF_CNTL2_BUF_BM_MASK                          = 0x03         # selects the operating mode of the sample buffer
		self.KX126_BUF_STATUS_2_SMP_LEV8_11_MASK                  = 0x0F         # buffer sample status level msb
		self.KX127_WHO_AM_I_WAI_MASK                              = 0xFF         