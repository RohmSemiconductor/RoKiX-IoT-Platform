# The MIT License (MIT)
#
# Copyright (c) 2018 Rohm Semiconductor
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
# Copyright (c) 2017 Rohm Semiconductor
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
		self.BM1422AGMV_REGISTER_DUMP_START                       = 0x0D         
		self.BM1422AGMV_INFO_LSB                                  = 0x0D         # Information Register [7:0]
		self.BM1422AGMV_INFO_MSB                                  = 0x0E         # Information Register [15:8]
		self.BM1422AGMV_WIA                                       = 0x0F         # WIA Register
		self.BM1422AGMV_DATAX_LSB                                 = 0x10         # Xch Output value LSB
		self.BM1422AGMV_DATAX_MSB                                 = 0x11         # Xch Output value MSB
		self.BM1422AGMV_DATAY_LSB                                 = 0x12         # Ych Output value LSB
		self.BM1422AGMV_DATAY_MSB                                 = 0x13         # Ych Output value MSB
		self.BM1422AGMV_DATAZ_LSB                                 = 0x14         # Zch Output value LSB
		self.BM1422AGMV_DATAZ_MSB                                 = 0x15         # Zch Output value MSB
		self.BM1422AGMV_STA1                                      = 0x18         # Status Register
		self.BM1422AGMV_CNTL1                                     = 0x1B         # Control setting1 Register
		self.BM1422AGMV_CNTL2                                     = 0x1C         # Control setting2 register
		self.BM1422AGMV_CNTL3                                     = 0x1D         # Control setting3 register
		self.BM1422AGMV_AVE_A                                     = 0x40         # Average time Register
		self.BM1422AGMV_CNTL4_LSB                                 = 0x5C         # Control setting4 Register (reserved) [7:0]
		self.BM1422AGMV_CNTL4_MSB                                 = 0x5D         # Control setting4 Register [15:8]
		self.BM1422AGMV_TEMP_LSB                                  = 0x60         # Temperature value LSB
		self.BM1422AGMV_TEMP_MSB                                  = 0x61         # Temperature value MSB
		self.BM1422AGMV_OFF_X_LSB                                 = 0x6C         # Xch Offset value
		self.BM1422AGMV_OFF_Y_LSB                                 = 0x72         # Ych Offset value
		self.BM1422AGMV_OFF_Z_LSB                                 = 0x78         # Zch Offset value
		self.BM1422AGMV_FINEOUTPUTX_LSB                           = 0x90         # DATAX value per OFF_X LSB
		self.BM1422AGMV_FINEOUTPUTX_MSB                           = 0x91         # DATAX value per OFF_X MSB
		self.BM1422AGMV_FINEOUTPUTY_LSB                           = 0x92         # DATAY value per OFF_Y LSB
		self.BM1422AGMV_FINEOUTPUTY_MSB                           = 0x93         # DATAY value per OFF_Y MSB
		self.BM1422AGMV_FINEOUTPUTZ_LSB                           = 0x94         # DATAZ value per OFF_Z LSB
		self.BM1422AGMV_FINEOUTPUTZ_MSB                           = 0x95         # DATAZ value per OFF_Z MSB
		self.BM1422AGMV_GAIN_PARA_X_LSB                           = 0x9C         # Axis interference Xch to Zch
		self.BM1422AGMV_GAIN_PARA_X_MSB                           = 0x9D         # Axis interference Xch to Ych
		self.BM1422AGMV_GAIN_PARA_Y_LSB                           = 0x9E         # Axis interference Ych to Zch
		self.BM1422AGMV_GAIN_PARA_Y_MSB                           = 0x9F         # Axis interference Ych to Xch
		self.BM1422AGMV_GAIN_PARA_Z_LSB                           = 0xA0         # Axis interference Zch to Ych
		self.BM1422AGMV_GAIN_PARA_Z_MSB                           = 0xA1         # Axis interference Zch to Xch
		self.BM1422AGMV_REGISTER_DUMP_END                         = 0xA1         
class bits(register_base):
	def __init__(self):
		self.BM1422AGMV_WIA_WIA_ID                                = (0x41 << 0)  # Who I am : 0x41
		self.BM1422AGMV_STA1_RD_DRDY_NOTREADY                     = (0x00 << 6)  # Not ready NG
		self.BM1422AGMV_STA1_RD_DRDY_READY                        = (0x01 << 6)  # Ready OK
		self.BM1422AGMV_STA1_RD_DRDY                              = (0x01 << 6)  # Preparation status of the measured data
		self.BM1422AGMV_CNTL1_PC1_OFF                             = (0x00 << 7)  # PowerDown
		self.BM1422AGMV_CNTL1_PC1_ON                              = (0x01 << 7)  # Active
		self.BM1422AGMV_CNTL1_PC1                                 = (0x01 << 7)  # Power Control
		self.BM1422AGMV_CNTL1_OUT_BIT_12                          = (0x00 << 6)  # 12bit Output
		self.BM1422AGMV_CNTL1_OUT_BIT_14                          = (0x01 << 6)  # 14bit Output
		self.BM1422AGMV_CNTL1_OUT_BIT                             = (0x01 << 6)  # Output Data bit setting
		self.BM1422AGMV_CNTL1_RST_LV_RELEASE                      = (0x00 << 5)  # Reset release
		self.BM1422AGMV_CNTL1_RST_LV_RESET                        = (0x01 << 5)  # Reset
		self.BM1422AGMV_CNTL1_RST_LV                              = (0x01 << 5)  # Logic reset control; reset release at RST_LV(CNTL1)=0 & RSTB_LV(CNTL4)=1
		self.BM1422AGMV_CNTL1_ODR_10                              = (0x00 << 3)  # 10Hz
		self.BM1422AGMV_CNTL1_ODR_100                             = (0x01 << 3)  # 100Hz
		self.BM1422AGMV_CNTL1_ODR_20                              = (0x02 << 3)  # 20Hz
		self.BM1422AGMV_CNTL1_ODR_1000                            = (0x03 << 3)  # 1kHz
		self.BM1422AGMV_CNTL1_FS1_CONT                            = (0x00 << 1)  # Continuous mode
		self.BM1422AGMV_CNTL1_FS1_SINGLE                          = (0x01 << 1)  # Single mode
		self.BM1422AGMV_CNTL1_FS1                                 = (0x01 << 1)  # Measurement mode setting
		self.BM1422AGMV_CNTL2_DREN_DISABLED                       = (0x00 << 3)  # Disable
		self.BM1422AGMV_CNTL2_DREN_ENABLED                        = (0x01 << 3)  # Enable
		self.BM1422AGMV_CNTL2_DREN                                = (0x01 << 3)  # DRDY terminal enable setting
		self.BM1422AGMV_CNTL2_DRP_LOW_ACTIVE                      = (0x00 << 2)  # Low active
		self.BM1422AGMV_CNTL2_DRP_HIGH_ACTIVE                     = (0x01 << 2)  # High active
		self.BM1422AGMV_CNTL2_DRP                                 = (0x01 << 2)  # DRDY terminal active setting
		self.BM1422AGMV_CNTL3_FORCE_START                         = (0x01 << 6)  # Start measurement
		self.BM1422AGMV_CNTL3_FORCE                               = (0x01 << 6)  # AD start measurement trigger at continuous mode (FS1=0) and single mode (FS1=1). (Autocleared)
		self.BM1422AGMV_AVE_A_AVE_A_4TIMES                        = (0x00 << 2)  # 4times
		self.BM1422AGMV_AVE_A_AVE_A_1TIMES                        = (0x01 << 2)  # 1times
		self.BM1422AGMV_AVE_A_AVE_A_2TIMES                        = (0x02 << 2)  # 2times
		self.BM1422AGMV_AVE_A_AVE_A_8TIMES                        = (0x03 << 2)  # 8times
		self.BM1422AGMV_AVE_A_AVE_A_16TIMES                       = (0x04 << 2)  # 16times
		self.BM1422AGMV_CNTL4_MSB_RSTB_LV                         = (0x01 << 0)  # RSTB_LV=1 when register written (data irrelevant), RSTB_LV=0 when PC1=0 written.
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BM1422AGMV_STA1_RD_DRDY={
			'NOTREADY':_b.BM1422AGMV_STA1_RD_DRDY_NOTREADY,
			'READY':_b.BM1422AGMV_STA1_RD_DRDY_READY,
		}
		self.BM1422AGMV_CNTL1_PC1={
			'OFF':_b.BM1422AGMV_CNTL1_PC1_OFF,
			'ON':_b.BM1422AGMV_CNTL1_PC1_ON,
		}
		self.BM1422AGMV_CNTL1_OUT_BIT={
			'12':_b.BM1422AGMV_CNTL1_OUT_BIT_12,
			'14':_b.BM1422AGMV_CNTL1_OUT_BIT_14,
		}
		self.BM1422AGMV_CNTL1_RST_LV={
			'RELEASE':_b.BM1422AGMV_CNTL1_RST_LV_RELEASE,
			'RESET':_b.BM1422AGMV_CNTL1_RST_LV_RESET,
		}
		self.BM1422AGMV_CNTL1_ODR={
			'10':_b.BM1422AGMV_CNTL1_ODR_10,
			'100':_b.BM1422AGMV_CNTL1_ODR_100,
			'20':_b.BM1422AGMV_CNTL1_ODR_20,
			'1000':_b.BM1422AGMV_CNTL1_ODR_1000,
		}
		self.BM1422AGMV_CNTL1_FS1={
			'CONT':_b.BM1422AGMV_CNTL1_FS1_CONT,
			'SINGLE':_b.BM1422AGMV_CNTL1_FS1_SINGLE,
		}
		self.BM1422AGMV_CNTL2_DREN={
			'DISABLED':_b.BM1422AGMV_CNTL2_DREN_DISABLED,
			'ENABLED':_b.BM1422AGMV_CNTL2_DREN_ENABLED,
		}
		self.BM1422AGMV_CNTL2_DRP={
			'LOW_ACTIVE':_b.BM1422AGMV_CNTL2_DRP_LOW_ACTIVE,
			'HIGH_ACTIVE':_b.BM1422AGMV_CNTL2_DRP_HIGH_ACTIVE,
		}
		self.BM1422AGMV_AVE_A_AVE_A={
			'4TIMES':_b.BM1422AGMV_AVE_A_AVE_A_4TIMES,
			'1TIMES':_b.BM1422AGMV_AVE_A_AVE_A_1TIMES,
			'2TIMES':_b.BM1422AGMV_AVE_A_AVE_A_2TIMES,
			'8TIMES':_b.BM1422AGMV_AVE_A_AVE_A_8TIMES,
			'16TIMES':_b.BM1422AGMV_AVE_A_AVE_A_16TIMES,
		}
class masks(register_base):
	def __init__(self):
		self.BM1422AGMV_WIA_WIA_MASK                              = 0xFF         
		self.BM1422AGMV_STA1_RD_DRDY_MASK                         = 0x40         # Preparation status of the measured data
		self.BM1422AGMV_CNTL1_PC1_MASK                            = 0x80         # Power Control
		self.BM1422AGMV_CNTL1_OUT_BIT_MASK                        = 0x40         # Output Data bit setting
		self.BM1422AGMV_CNTL1_RST_LV_MASK                         = 0x20         # Logic reset control; reset release at RST_LV(CNTL1)=0 & RSTB_LV(CNTL4)=1
		self.BM1422AGMV_CNTL1_ODR_MASK                            = 0x18         # Measurement output data rates
		self.BM1422AGMV_CNTL1_FS1_MASK                            = 0x02         # Measurement mode setting
		self.BM1422AGMV_CNTL2_DREN_MASK                           = 0x08         # DRDY terminal enable setting
		self.BM1422AGMV_CNTL2_DRP_MASK                            = 0x04         # DRDY terminal active setting
		self.BM1422AGMV_CNTL3_FORCE_MASK                          = 0x40         # AD start measurement trigger at continuous mode (FS1=0) and single mode (FS1=1). (Autocleared)
		self.BM1422AGMV_AVE_A_AVE_A_MASK                          = 0x1C         # Average Time