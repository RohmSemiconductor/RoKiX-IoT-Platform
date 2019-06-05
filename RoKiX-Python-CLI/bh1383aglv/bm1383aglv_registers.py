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
		self.BM1383AGLV_PRESSURE_MIN                              = 0x12C        # [hPa]
		self.BM1383AGLV_PRESSURE_MAX                              = 0x44C        # [hPa]
		self.BM1383AGLV_REGISTER_DUMP_START                       = 0x0F         
		self.BM1383AGLV_ID1_REG                                   = 0x0F         
		self.BM1383AGLV_ID2_REG                                   = 0x10         
		self.BM1383AGLV_POWER_REG                                 = 0x12         
		self.BM1383AGLV_RESET_REG                                 = 0x13         
		self.BM1383AGLV_MODE_CONTROL_REG                          = 0x14         # This register can be accessed when power is up and measurement control block is not in reset.
		self.BM1383AGLV_STATUS_REG                                = 0x19         # Reading this REG resets DRDY pin
		self.BM1383AGLV_PRESSURE_OUT_MSB                          = 0x1A         # PRESS_OUT[15:5] integer part of pressure value
		self.BM1383AGLV_PRESSURE_OUT_LSB                          = 0x1B         # PRESS_OUT[4:0] PRESS_OUT_XL[7:2] decimal part of pressure value
		self.BM1383AGLV_PRESSURE_OUT_DECIMAL                      = 0x1C         # Pressurevalue[hPa] = { PRESS_OUT[15:8] PRESS_OUT[7:0] PRESS_OUT_XL[7:2] } / 2048
		self.BM1383AGLV_TEMPERATURE_OUT_MSB                       = 0x1D         # TEMP_OUT: [15] sign ; [14:5] integer ; [4:0] decimal (2's complement numbers)
		self.BM1383AGLV_TEMPERATURE_OUT_LSB                       = 0x1E         # Temperature value [C]= TEMP_OUT[15:0]/32
		self.BM1383AGLV_REGISTER_DUMP_END                         = 0x1E         
class bits(register_base):
	def __init__(self):
		self.BM1383AGLV_ID1_REG_MANUFACTURER_ID1                  = (0xE0 << 0)  
		self.BM1383AGLV_ID2_REG_MANUFACTURER_ID2                  = (0x32 << 0)  
		self.BM1383AGLV_POWER_REG_RESERVED_WRITE0                 = (0x00 << 1)  # write 0
		self.BM1383AGLV_POWER_REG_POWER_DOWN                      = (0x00 << 0)  
		self.BM1383AGLV_POWER_REG_POWER_UP                        = (0x01 << 0)  
		self.BM1383AGLV_POWER_REG_POWER                           = (0x01 << 0)  # Named as PWR_DOWN in specification
		self.BM1383AGLV_RESET_REG_RESERVED_WRITE0                 = (0x00 << 1)  # write 0
		self.BM1383AGLV_RESET_REG_MODE_RESET                      = (0x00 << 0)  # Measurement control block is reset
		self.BM1383AGLV_RESET_REG_MODE_STANDBY                    = (0x01 << 0)  # Measurement control block is active
		self.BM1383AGLV_RESET_REG_MODE                            = (0x01 << 0)  # Named as RESET in specification
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS       = (0x00 << 5)  # Measurement time 3 [ms] ; interval 50 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS       = (0x01 << 5)  # 5 [ms] ; 50 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS       = (0x02 << 5)  # 10 [ms] ; 50 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS       = (0x03 << 5)  # 19 [ms] ; 50 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS      = (0x04 << 5)  # 37 [ms] ; 50 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS     = (0x05 << 5)  # 74 [ms] ; 100 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS     = (0x06 << 5)  # 147 [ms] ; 200 [ms]
		self.BM1383AGLV_MODE_CONTROL_REG_DRDY_DISABLED            = (0x00 << 4)  
		self.BM1383AGLV_MODE_CONTROL_REG_DRDY_ENABLED             = (0x01 << 4)  
		self.BM1383AGLV_MODE_CONTROL_REG_DRDY                     = (0x01 << 4)  # Named as DREN in specification
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED3_WRITE_1        = (0x01 << 3)  # write 1
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED3                = (0x01 << 3)  
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED2_WRITE_0        = (0x00 << 2)  # write 0
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED2                = (0x01 << 2)  
		self.BM1383AGLV_MODE_CONTROL_REG_MODE_STANDBY             = (0x00 << 0)  
		self.BM1383AGLV_MODE_CONTROL_REG_MODE_ONE_SHOT            = (0x01 << 0)  
		self.BM1383AGLV_MODE_CONTROL_REG_MODE_CONTINUOUS          = (0x02 << 0)  
		self.BM1383AGLV_MODE_CONTROL_REG_MODE_PROHIBITED          = (0x03 << 0)  
		self.BM1383AGLV_STATUS_REG_RESERVED_WRITE0                = (0x00 << 1)  # write 0
		self.BM1383AGLV_STATUS_REG_DRDY_NOT_READY                 = (0x00 << 0)  
		self.BM1383AGLV_STATUS_REG_DRDY_READY                     = (0x01 << 0)  
		self.BM1383AGLV_STATUS_REG_DRDY                           = (0x01 << 0)  # Named as RD_DRDY in specification
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BM1383AGLV_RESET_REG_MODE={
			'RESET':_b.BM1383AGLV_RESET_REG_MODE_RESET,
			'STANDBY':_b.BM1383AGLV_RESET_REG_MODE_STANDBY,
		}
		self.BM1383AGLV_MODE_CONTROL_REG_DRDY={
			'DISABLED':_b.BM1383AGLV_MODE_CONTROL_REG_DRDY_DISABLED,
			'ENABLED':_b.BM1383AGLV_MODE_CONTROL_REG_DRDY_ENABLED,
		}
		self.BM1383AGLV_STATUS_REG_DRDY={
			'READY':_b.BM1383AGLV_STATUS_REG_DRDY_READY,
			'NOT_READY':_b.BM1383AGLV_STATUS_REG_DRDY_NOT_READY,
		}
		self.BM1383AGLV_POWER_REG_POWER={
			'DOWN':_b.BM1383AGLV_POWER_REG_POWER_DOWN,
			'UP':_b.BM1383AGLV_POWER_REG_POWER_UP,
		}
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM={
			'AVG_8_50MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS,
			'AVG_64_200MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS,
			'AVG_16_50MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS,
			'AVG_2_50MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS,
			'AVG_32_100MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS,
			'AVG_4_50MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS,
			'AVG_1_50MS':_b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS,
		}
		self.BM1383AGLV_MODE_CONTROL_REG_MODE={
			'STANDBY':_b.BM1383AGLV_MODE_CONTROL_REG_MODE_STANDBY,
			'ONE_SHOT':_b.BM1383AGLV_MODE_CONTROL_REG_MODE_ONE_SHOT,
			'PROHIBITED':_b.BM1383AGLV_MODE_CONTROL_REG_MODE_PROHIBITED,
			'CONTINUOUS':_b.BM1383AGLV_MODE_CONTROL_REG_MODE_CONTINUOUS,
		}
class masks(register_base):
	def __init__(self):
		self.BM1383AGLV_ID1_REG_MANUFACTURER_MASK                 = 0xFF         
		self.BM1383AGLV_ID2_REG_MANUFACTURER_MASK                 = 0xFF         
		self.BM1383AGLV_POWER_REG_RESERVED_MASK                   = 0xFE         
		self.BM1383AGLV_POWER_REG_POWER_MASK                      = 0x01         # Named as PWR_DOWN in specification
		self.BM1383AGLV_RESET_REG_RESERVED_MASK                   = 0xFE         
		self.BM1383AGLV_RESET_REG_MODE_MASK                       = 0x01         # Named as RESET in specification
		self.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_MASK             = 0xE0         
		self.BM1383AGLV_MODE_CONTROL_REG_DRDY_MASK                = 0x10         # Named as DREN in specification
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED3_MASK           = 0x08         
		self.BM1383AGLV_MODE_CONTROL_REG_RESERVED2_MASK           = 0x04         
		self.BM1383AGLV_MODE_CONTROL_REG_MODE_MASK                = 0x03         
		self.BM1383AGLV_STATUS_REG_RESERVED_MASK                  = 0xFE         
		self.BM1383AGLV_STATUS_REG_DRDY_MASK                      = 0x01         # Named as RD_DRDY in specification