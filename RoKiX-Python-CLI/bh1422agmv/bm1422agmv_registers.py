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
		self.BM1422AGMV_INFO                                      = 0x0D         # Information 16bit
		self.BM1422AGMV_INFO_MSB                                  = 0x0E         
		self.BM1422AGMV_WHO_AM_I                                  = 0x0F         # This register can be used for supplier recognition, as it can be factory written to a known byte value.
		self.BM1422AGMV_DATAX                                     = 0x10         # Xch Output value
		self.BM1422AGMV_DATAX_MSB                                 = 0x11         
		self.BM1422AGMV_DATAY                                     = 0x12         # Ych Output value
		self.BM1422AGMV_DATAY_MSB                                 = 0x13         
		self.BM1422AGMV_DATAZ                                     = 0x14         # Zch Output value
		self.BM1422AGMV_DATAZ_MSB                                 = 0x15         
		self.BM1422AGMV_STA1                                      = 0x18         # Data ready status
		self.BM1422AGMV_CNTL1                                     = 0x1B         # Control setting
		self.BM1422AGMV_CNTL2                                     = 0x1C         # Control setting 2
		self.BM1422AGMV_CNTL3                                     = 0x1D         # Control setting 3
		self.BM1422AGMV_PRET                                      = 0x30         # Preset time register
		self.BM1422AGMV_AVER                                      = 0x40         # Average time setting
		self.BM1422AGMV_CNTL4_LSB                                 = 0x5C         # Control setting. Reserved
		self.BM1422AGMV_CNTL4_MSB                                 = 0x5D         # Control setting. RSTB_LV=1 when register written (data irrelevant), RSTB_LV=0 when PC1=0 written.
		self.BM1422AGMV_TEMP                                      = 0x60         # Temperature value
		self.BM1422AGMV_TEMP_MSB                                  = 0x61         
		self.BM1422AGMV_OFF_X                                     = 0x6C         # Xch offset value
		self.BM1422AGMV_OFF_Y                                     = 0x72         # Ych offset value
		self.BM1422AGMV_OFF_Z                                     = 0x78         # Zch offset value
		self.BM1422AGMV_FINEOUTPUTX                               = 0x90         # DATAX value per OFF_X
		self.BM1422AGMV_FINEOUTPUTX_MSB                           = 0x91         
		self.BM1422AGMV_FINEOUTPUTY                               = 0x92         # DATAY value per OFF_Y
		self.BM1422AGMV_FINEOUTPUTY_MSB                           = 0x93         
		self.BM1422AGMV_FINEOUTPUTZ                               = 0x94         # DATAZ value per OFF_Z
		self.BM1422AGMV_FINEOUTPUTZ_MSB                           = 0x95         
		self.BM1422AGMV_SENSX                                     = 0x96         # Reserved
		self.BM1422AGMV_SENSX_MSB                                 = 0x97         
		self.BM1422AGMV_SENSY                                     = 0x98         # Reserved
		self.BM1422AGMV_SENSY_MSB                                 = 0x99         
		self.BM1422AGMV_SENSZ                                     = 0x9A         # Reserved
		self.BM1422AGMV_SENSZ_MSB                                 = 0x9B         
		self.BM1422AGMV_GAIN_PARA_X_Z                             = 0x9C         # Axis interference Xch to Zch
		self.BM1422AGMV_GAIN_PARA_X_Y                             = 0x9D         # Axis interference Xch to Ych
		self.BM1422AGMV_GAIN_PARA_Y_Z                             = 0x9E         # Axis interference Ych to Zch
		self.BM1422AGMV_GAIN_PARA_Y_X                             = 0x9F         # Axis interference Ych to Xch
		self.BM1422AGMV_GAIN_PARA_Z_Y                             = 0xA0         # Axis interference Zch to Ych
		self.BM1422AGMV_GAIN_PARA_Z_X                             = 0xA1         # Axis interference Zch to Xch
		self.BM1422AGMV_OFFZEROX                                  = 0xF8         # Reserved
		self.BM1422AGMV_OFFZEROX_MSB                              = 0xF9         
		self.BM1422AGMV_OFFZEROY                                  = 0xFA         # Reserved
		self.BM1422AGMV_OFFZEROY_MSB                              = 0xFB         
		self.BM1422AGMV_OFFZEROZ                                  = 0xFC         # Reserved
		self.BM1422AGMV_OFFZEROZ_MSB                              = 0xFD         
		self.BM1422AGMV_REGISTER_DUMP_END                         = 0x1E         
class bits(register_base):
	def __init__(self):
		self.BM1422AGMV_WHO_AM_I_WIA_ID                           = (0x41 << 0)  # WHO_AM_I -value
		self.BM1422AGMV_STA1_DRDY_READY                           = (0x01 << 6)  
		self.BM1422AGMV_STA1_DRDY                                 = (0x01 << 6)  # Data ready status
		self.BM1422AGMV_CNTL1_PC1_OFF                             = (0x00 << 7)  # PowerDown
		self.BM1422AGMV_CNTL1_PC1_ON                              = (0x01 << 7)  # Active
		self.BM1422AGMV_CNTL1_PC1                                 = (0x01 << 7)  # Power Control
		self.BM1422AGMV_CNTL1_OUT_BIT_12                          = (0x00 << 6)  # 12bit resolution
		self.BM1422AGMV_CNTL1_OUT_BIT_14                          = (0x01 << 6)  # 14bit resolution
		self.BM1422AGMV_CNTL1_OUT_BIT                             = (0x01 << 6)  # Output data bit setting
		self.BM1422AGMV_CNTL1_RST_LV_RELEASE                      = (0x00 << 5)  # Reset release
		self.BM1422AGMV_CNTL1_RST_LV_RESET                        = (0x01 << 5)  # Reset (POR)
		self.BM1422AGMV_CNTL1_RST_LV                              = (0x01 << 5)  # Reset release (RST_LV=0 & RSTB_LV=1)
		self.BM1422AGMV_CNTL1_ODR_10                              = (0x00 << 3)  
		self.BM1422AGMV_CNTL1_ODR_100                             = (0x01 << 3)  
		self.BM1422AGMV_CNTL1_ODR_20                              = (0x02 << 3)  
		self.BM1422AGMV_CNTL1_ODR_1000                            = (0x03 << 3)  
		self.BM1422AGMV_CNTL1_FS1_CONT                            = (0x00 << 1)  # Continuous mode
		self.BM1422AGMV_CNTL1_FS1_SINGLE                          = (0x01 << 1)  # Single mode
		self.BM1422AGMV_CNTL1_FS1                                 = (0x01 << 1)  # Measurement mode
		self.BM1422AGMV_CNTL2_DREN_DISABLED                       = (0x00 << 3)  
		self.BM1422AGMV_CNTL2_DREN_ENABLED                        = (0x01 << 3)  
		self.BM1422AGMV_CNTL2_DREN                                = (0x01 << 3)  # DRDY enable setting. (0:Disable, 1:Enable)
		self.BM1422AGMV_CNTL2_DRP_LOWACTIVE                       = (0x00 << 2)  
		self.BM1422AGMV_CNTL2_DRP_HIGHACTIVE                      = (0x01 << 2)  
		self.BM1422AGMV_CNTL2_DRP                                 = (0x01 << 2)  # DRDY active setting. (0:Low active, 1:High active)
		self.BM1422AGMV_CNTL3_FORCE_START                         = (0x01 << 6)  
		self.BM1422AGMV_CNTL3_FORCE                               = (0x01 << 6)  # AD start measurement trigger at continuous mode and single mode. (Autocleared)
		self.BM1422AGMV_PRET_PS                                   = (0x01 << 0)  # write "0"
		self.BM1422AGMV_AVER_AVG_4TIMES                           = (0x00 << 2)  
		self.BM1422AGMV_AVER_AVG_1TIMES                           = (0x01 << 2)  
		self.BM1422AGMV_AVER_AVG_2TIMES                           = (0x02 << 2)  
		self.BM1422AGMV_AVER_AVG_8TIMES                           = (0x03 << 2)  
		self.BM1422AGMV_AVER_AVG_16TIMES                          = (0x04 << 2)  
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BM1422AGMV_CNTL2_DREN={
			'DISABLED':_b.BM1422AGMV_CNTL2_DREN_DISABLED,
			'ENABLED':_b.BM1422AGMV_CNTL2_DREN_ENABLED,
		}
		self.BM1422AGMV_CNTL1_PC1={
			'ON':_b.BM1422AGMV_CNTL1_PC1_ON,
			'OFF':_b.BM1422AGMV_CNTL1_PC1_OFF,
		}
		self.BM1422AGMV_CNTL1_FS1={
			'SINGLE':_b.BM1422AGMV_CNTL1_FS1_SINGLE,
			'CONT':_b.BM1422AGMV_CNTL1_FS1_CONT,
		}
		self.BM1422AGMV_CNTL2_DRP={
			'HIGHACTIVE':_b.BM1422AGMV_CNTL2_DRP_HIGHACTIVE,
			'LOWACTIVE':_b.BM1422AGMV_CNTL2_DRP_LOWACTIVE,
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
		self.BM1422AGMV_CNTL1_OUT_BIT={
			'12':_b.BM1422AGMV_CNTL1_OUT_BIT_12,
			'14':_b.BM1422AGMV_CNTL1_OUT_BIT_14,
		}
		self.BM1422AGMV_AVER_AVG={
			'4TIMES':_b.BM1422AGMV_AVER_AVG_4TIMES,
			'2TIMES':_b.BM1422AGMV_AVER_AVG_2TIMES,
			'8TIMES':_b.BM1422AGMV_AVER_AVG_8TIMES,
			'16TIMES':_b.BM1422AGMV_AVER_AVG_16TIMES,
			'1TIMES':_b.BM1422AGMV_AVER_AVG_1TIMES,
		}
class masks(register_base):
	def __init__(self):
		self.BM1422AGMV_WHO_AM_I_WIA_MASK                         = 0xFF         
		self.BM1422AGMV_STA1_DRDY_MASK                            = 0x40         # Data ready status
		self.BM1422AGMV_CNTL1_PC1_MASK                            = 0x80         # Power Control
		self.BM1422AGMV_CNTL1_OUT_BIT_MASK                        = 0x40         # Output data bit setting
		self.BM1422AGMV_CNTL1_RST_LV_MASK                         = 0x20         # Reset release (RST_LV=0 & RSTB_LV=1)
		self.BM1422AGMV_CNTL1_ODR_MASK                            = 0x18         
		self.BM1422AGMV_CNTL1_FS1_MASK                            = 0x02         # Measurement mode
		self.BM1422AGMV_CNTL2_DREN_MASK                           = 0x08         # DRDY enable setting. (0:Disable, 1:Enable)
		self.BM1422AGMV_CNTL2_DRP_MASK                            = 0x04         # DRDY active setting. (0:Low active, 1:High active)
		self.BM1422AGMV_CNTL3_FORCE_MASK                          = 0x40         # AD start measurement trigger at continuous mode and single mode. (Autocleared)
		self.BM1422AGMV_AVER_AVG_MASK                             = 0x1C         