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
		self.KXTJ3_XOUT_L                                         = 0x06         # output register x
		self.KXTJ3_XOUT_H                                         = 0x07         
		self.KXTJ3_YOUT_L                                         = 0x08         # output register y
		self.KXTJ3_YOUT_H                                         = 0x09         
		self.KXTJ3_ZOUT_L                                         = 0x0A         # output register z
		self.KXTJ3_ZOUT_H                                         = 0x0B         
		self.KXTJ3_DCST_RESP                                      = 0x0C         # This register can be used to verify proper integrated circuit functionality
		self.KXTJ3_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition, as it can be factory written to a known byte value.
		self.KXTJ3_INT_SOURCE1                                    = 0x16         # This register reports which function caused an interrupt.
		self.KXTJ3_INT_SOURCE2                                    = 0x17         # This register reports the axis and direction of detected motion
		self.KXTJ3_STATUS_REG                                     = 0x18         # This register reports the status of the interrupt
		self.KXTJ3_INT_REL                                        = 0x1A         # Latched interrupt source information
		self.KXTJ3_CTRL_REG1                                      = 0x1B         # Read/write control register that controls the main feature set
		self.KXTJ3_CTRL_REG2                                      = 0x1D         # Read/write control register that provides more feature set control
		self.KXTJ3_INT_CTRL_REG1                                  = 0x1E         # This register controls the settings for the physical interrupt pin
		self.KXTJ3_INT_CTRL_REG2                                  = 0x1F         # This register controls which axis and direction of detected motion can cause an interrupt
		self.KXTJ3_DATA_CTRL_REG                                  = 0x21         # Read/write control register that configures the acceleration outputs
		self.KXTJ3_WAKEUP_COUNTER                                 = 0x29         # This register sets the time motion must be present before a wake-up interrupt is set
		self.KXTJ3_NA_COUNTER                                     = 0x2A         # This register sets the non-activity time required before another wake-up interrupt can be set
		self.KXTJ3_SELF_TEST                                      = 0x3A         # When 0xCA is written to this register, the MEMS self-test function is enabled
		self.KXTJ3_WAKEUP_THRESHOLD_H                             = 0x6A         # Those registers (12-bits)sets the threshold for wake-up (motion detect) interrupt is set
		self.KXTJ3_WAKEUP_THRESHOLD_L                             = 0x6B         # lsb part
		self.KXCJC_WHO_AM_I                                       = 0x0F         # This register can be used for supplier recognition, as it can be factory written to a known byte value.
class bits(register_base):
	def __init__(self):
		self.KXTJ3_DCST_RESP_DCSTR_BEFORE                         = (0x55 << 0)  # before set
		self.KXTJ3_DCST_RESP_DCSTR_AFTER                          = (0xAA << 0)  # after set
		self.KXTJ3_WHO_AM_I_WIA_ID                                = (0x35 << 0)  # WHO_AM_I -value for KXTJ3
		self.KXTJ3_INT_SOURCE1_DRDY                               = (0x01 << 4)  # indicates that new acceleration data
		self.KXTJ3_INT_SOURCE1_WUFS                               = (0x01 << 1)  # Wake up
		self.KXTJ3_INT_SOURCE2_XNWU                               = (0x01 << 5)  # x-
		self.KXTJ3_INT_SOURCE2_XPWU                               = (0x01 << 4)  # x+
		self.KXTJ3_INT_SOURCE2_YNWU                               = (0x01 << 3)  # y-
		self.KXTJ3_INT_SOURCE2_YPWU                               = (0x01 << 2)  # y+
		self.KXTJ3_INT_SOURCE2_ZNWU                               = (0x01 << 1)  # z-
		self.KXTJ3_INT_SOURCE2_ZPWU                               = (0x01 << 0)  # z+
		self.KXTJ3_STATUS_REG_INT                                 = (0x01 << 4)  # reports the combined (OR) interrupt information of DRDY and WUFS in the interrupt source register
		self.KXTJ3_CTRL_REG1_PC                                   = (0x01 << 7)  # controls the operating mode of the KXTJ3
		self.KXTJ3_CTRL_REG1_RES                                  = (0x01 << 6)  # determines the performance mode of the KXTJ3
		self.KXTJ3_CTRL_REG1_DRDYE                                = (0x01 << 5)  # enables the reporting of the availability of new acceleration data as an interrupt
		self.KXTJ3_CTRL_REG1_GSEL_2G                              = (0x00 << 2)  # 2g range
		self.KXTJ3_CTRL_REG1_GSEL_16G                             = (0x01 << 2)  # 16g range
		self.KXTJ3_CTRL_REG1_GSEL_4G                              = (0x02 << 2)  # 4g range
		self.KXTJ3_CTRL_REG1_GSEL_16G2                            = (0x03 << 2)  # 16g range
		self.KXTJ3_CTRL_REG1_GSEL_8G                              = (0x04 << 2)  # 8g range
		self.KXTJ3_CTRL_REG1_GSEL_16G3                            = (0x05 << 2)  # 16g range
		self.KXTJ3_CTRL_REG1_GSEL_8G_14                           = (0x06 << 2)  # 8g range with 14b resolution
		self.KXTJ3_CTRL_REG1_GSEL_16G_14                          = (0x07 << 2)  # 16g range with 14b resolution
		self.KXTJ3_CTRL_REG1_EN16G                                = (0x01 << 2)  # enables 14-bit mode if GSEL = '11'
		self.KXTJ3_CTRL_REG1_WUFE                                 = (0x01 << 1)  # enables the Wake Up (motion detect) function.
		self.KXTJ3_CTRL_REG2_SRST                                 = (0x01 << 7)  # initiates software reset
		self.KXTJ3_CTRL_REG2_DCST                                 = (0x01 << 4)  # initiates the digital communication self-test function.
		self.KXTJ3_CTRL_REG2_OWUF_0P781                           = (0x00 << 0)  # 0.78Hz
		self.KXTJ3_CTRL_REG2_OWUF_1P563                           = (0x01 << 0)  # 1.563Hz
		self.KXTJ3_CTRL_REG2_OWUF_3P125                           = (0x02 << 0)  # 3.125Hz
		self.KXTJ3_CTRL_REG2_OWUF_6P25                            = (0x03 << 0)  # 6.25Hz
		self.KXTJ3_CTRL_REG2_OWUF_12P5                            = (0x04 << 0)  # 12.5Hz
		self.KXTJ3_CTRL_REG2_OWUF_25                              = (0x05 << 0)  # 25Hz
		self.KXTJ3_CTRL_REG2_OWUF_50                              = (0x06 << 0)  # 50Hz
		self.KXTJ3_CTRL_REG2_OWUF_100                             = (0x07 << 0)  # 100Hz
		self.KXTJ3_INT_CTRL_REG1_IEN                              = (0x01 << 5)  # enables/disables the physical interrupt pin
		self.KXTJ3_INT_CTRL_REG1_IEA                              = (0x01 << 4)  # sets the polarity of the physical interrupt pin
		self.KXTJ3_INT_CTRL_REG1_IEL                              = (0x01 << 3)  # sets the response of the physical interrupt pin
		self.KXTJ3_INT_CTRL_REG1_STPOL                            = (0x01 << 1)  # selftest polarity
		self.KXTJ3_INT_CTRL_REG2_ULMODE                           = (0x01 << 7)  # Unlatched mode motion  interrupt; 0=disabled,1=enabled
		self.KXTJ3_INT_CTRL_REG2_XNWU                             = (0x01 << 5)  # x-
		self.KXTJ3_INT_CTRL_REG2_XPWU                             = (0x01 << 4)  # x+
		self.KXTJ3_INT_CTRL_REG2_YNWU                             = (0x01 << 3)  # y-
		self.KXTJ3_INT_CTRL_REG2_YPWU                             = (0x01 << 2)  # y+
		self.KXTJ3_INT_CTRL_REG2_ZNWU                             = (0x01 << 1)  # z-
		self.KXTJ3_INT_CTRL_REG2_ZPWU                             = (0x01 << 0)  # z+
		self.KXTJ3_DATA_CTRL_REG_OSA_12P5                         = (0x00 << 0)  # 12.5Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_25                           = (0x01 << 0)  # 25Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_50                           = (0x02 << 0)  # 50Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_100                          = (0x03 << 0)  # 100Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_200                          = (0x04 << 0)  # 200Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_400                          = (0x05 << 0)  # 400Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_800                          = (0x06 << 0)  # 800Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_1600                         = (0x07 << 0)  # 1600Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_0P781                        = (0x08 << 0)  # 0.78Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_1P563                        = (0x09 << 0)  # 1.563Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_3P125                        = (0x0A << 0)  # 3.125Hz
		self.KXTJ3_DATA_CTRL_REG_OSA_6P25                         = (0x0B << 0)  # 6.25Hz
		self.KXTJ3_SELF_TEST_MEMS_TEST_ENABLE                     = (0xCA << 0)  # charge on
		self.KXTJ3_SELF_TEST_MEMS_TEST_DISABLE                    = (0x00 << 0)  # charge off
		self.KXCJC_WHO_AM_I_WIA_ID                                = (0x36 << 0)  # WHO_AM_I -value for KXCJC
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KXTJ3_SELF_TEST_MEMS_TEST={
			'ENABLE':_b.KXTJ3_SELF_TEST_MEMS_TEST_ENABLE,
			'DISABLE':_b.KXTJ3_SELF_TEST_MEMS_TEST_DISABLE,
		}
		self.KXTJ3_CTRL_REG1_GSEL={
			'8G_14':_b.KXTJ3_CTRL_REG1_GSEL_8G_14,
			'16G':_b.KXTJ3_CTRL_REG1_GSEL_16G,
			'8G':_b.KXTJ3_CTRL_REG1_GSEL_8G,
			'16G2':_b.KXTJ3_CTRL_REG1_GSEL_16G2,
			'16G3':_b.KXTJ3_CTRL_REG1_GSEL_16G3,
			'2G':_b.KXTJ3_CTRL_REG1_GSEL_2G,
			'4G':_b.KXTJ3_CTRL_REG1_GSEL_4G,
			'16G_14':_b.KXTJ3_CTRL_REG1_GSEL_16G_14,
		}
		self.KXTJ3_DATA_CTRL_REG_OSA={
			'25':_b.KXTJ3_DATA_CTRL_REG_OSA_25,
			'0P781':_b.KXTJ3_DATA_CTRL_REG_OSA_0P781,
			'200':_b.KXTJ3_DATA_CTRL_REG_OSA_200,
			'12P5':_b.KXTJ3_DATA_CTRL_REG_OSA_12P5,
			'1600':_b.KXTJ3_DATA_CTRL_REG_OSA_1600,
			'50':_b.KXTJ3_DATA_CTRL_REG_OSA_50,
			'1P563':_b.KXTJ3_DATA_CTRL_REG_OSA_1P563,
			'3P125':_b.KXTJ3_DATA_CTRL_REG_OSA_3P125,
			'400':_b.KXTJ3_DATA_CTRL_REG_OSA_400,
			'100':_b.KXTJ3_DATA_CTRL_REG_OSA_100,
			'800':_b.KXTJ3_DATA_CTRL_REG_OSA_800,
			'6P25':_b.KXTJ3_DATA_CTRL_REG_OSA_6P25,
		}
		self.KXTJ3_CTRL_REG2_OWUF={
			'25':_b.KXTJ3_CTRL_REG2_OWUF_25,
			'0P781':_b.KXTJ3_CTRL_REG2_OWUF_0P781,
			'12P5':_b.KXTJ3_CTRL_REG2_OWUF_12P5,
			'50':_b.KXTJ3_CTRL_REG2_OWUF_50,
			'1P563':_b.KXTJ3_CTRL_REG2_OWUF_1P563,
			'3P125':_b.KXTJ3_CTRL_REG2_OWUF_3P125,
			'100':_b.KXTJ3_CTRL_REG2_OWUF_100,
			'6P25':_b.KXTJ3_CTRL_REG2_OWUF_6P25,
		}
		self.KXTJ3_DCST_RESP_DCSTR={
			'AFTER':_b.KXTJ3_DCST_RESP_DCSTR_AFTER,
			'BEFORE':_b.KXTJ3_DCST_RESP_DCSTR_BEFORE,
		}
class masks(register_base):
	def __init__(self):
		self.KXTJ3_DCST_RESP_DCSTR_MASK                           = 0xFF         
		self.KXTJ3_WHO_AM_I_WIA_MASK                              = 0xFF         
		self.KXTJ3_CTRL_REG1_GSEL_MASK                            = 0x1C         # selects the acceleration range of the accelerometer outputs
		self.KXTJ3_CTRL_REG2_OWUF_MASK                            = 0x07         # sets the Output Data Rate for the Wake Up function
		self.KXTJ3_DATA_CTRL_REG_OSA_MASK                         = 0x0F         # sets the output data rate (ODR)
		self.KXTJ3_SELF_TEST_MEMS_TEST_MASK                       = 0xFF         
		self.KXCJC_WHO_AM_I_WIA_MASK                              = 0xFF         