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
		self.BM1383AGLV_REGISTER_DUMP_START                       = 0x0F         
		self.BM1383AGLV_ID1                                       = 0x0F         # Identifier 1
		self.BM1383AGLV_ID2                                       = 0x10         # Identifier 2
		self.BM1383AGLV_POWER_DOWN                                = 0x12         # Power mode register
		self.BM1383AGLV_RESET                                     = 0x13         # Measurement control block reset register
		self.BM1383AGLV_MODE_CONTROL                              = 0x14         # This register can be accessed when power is up and measurement control block is not in reset.
		self.BM1383AGLV_STATUS                                    = 0x19         # Reading this REG resets DRDY pin
		self.BM1383AGLV_PRESSURE_MSB                              = 0x1A         # The upper part of pressure data
		self.BM1383AGLV_PRESSURE_LSB                              = 0x1B         # The lower part of pressure data
		self.BM1383AGLV_PRESSURE_LSB2                             = 0x1C         # Pressurevalue[hPa] = { PRESS_OUT[15:8] PRESS_OUT[7:0] PRESS_OUT_XL[7:2] } / 2048
		self.BM1383AGLV_TEMPERATURE_MSB                           = 0x1D         # TEMP_OUT: [15] sign ; [14:5] integer ; [4:0] decimal (2's complement numbers)
		self.BM1383AGLV_TEMPERATURE_LSB                           = 0x1E         # Temperature value [C]= TEMP_OUT[15:0]/32
		self.BM1383AGLV_REGISTER_DUMP_END                         = 0x1E         
class bits(register_base):
	def __init__(self):
		self.BM1383AGLV_ID1_ID1_ID1                               = (0xE0 << 0)  # Identifier 1
		self.BM1383AGLV_ID2_ID2_ID2                               = (0x32 << 0)  # Identifier 2
		self.BM1383AGLV_POWER_DOWN_PWR_DOWN_DOWN                  = (0x00 << 0)  # power down
		self.BM1383AGLV_POWER_DOWN_PWR_DOWN_UP                    = (0x01 << 0)  # active
		self.BM1383AGLV_POWER_DOWN_PWR_DOWN                       = (0x01 << 0)  # Power enable
		self.BM1383AGLV_RESET_RSTB_RESET                          = (0x00 << 0)  # Measurement control block is reset
		self.BM1383AGLV_RESET_RSTB_STANDBY                        = (0x01 << 0)  # Measurement control block is active
		self.BM1383AGLV_RESET_RSTB                                = (0x01 << 0)  # Measurement control block reset
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_1_60MS           = (0x00 << 5)  # single (meas. time max 6 [ms] ; max interval 60 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_2_60MS           = (0x01 << 5)  # average of 2 times (9 [ms] ; 60 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_4_60MS           = (0x02 << 5)  # average of 4 times (16 [ms] ; 60 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_8_60MS           = (0x03 << 5)  # average of 8 times (30 [ms] ; 60 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS          = (0x04 << 5)  # average of 16 times (60 [ms] ; 60 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_32_120MS         = (0x05 << 5)  # average of 32 times (120 [ms] ; 120 [ms])
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_64_240MS         = (0x06 << 5)  # average of 64 times (240 [ms] ; 240 [ms])
		self.BM1383AGLV_MODE_CONTROL_DREN_DISABLED                = (0x00 << 4)  # DRDY pin Disable
		self.BM1383AGLV_MODE_CONTROL_DREN_ENABLED                 = (0x01 << 4)  # DRDY pin Enable
		self.BM1383AGLV_MODE_CONTROL_DREN                         = (0x01 << 4)  # DRDY pin Enable
		self.BM1383AGLV_MODE_CONTROL_RESERVED3_WRITE_1            = (0x01 << 3)  # write 1
		self.BM1383AGLV_MODE_CONTROL_RESERVED3                    = (0x01 << 3)  # Reserved
		self.BM1383AGLV_MODE_CONTROL_RESERVED2_WRITE_0            = (0x00 << 2)  # write 0
		self.BM1383AGLV_MODE_CONTROL_RESERVED2                    = (0x01 << 2)  # Reserved; write 0
		self.BM1383AGLV_MODE_CONTROL_MODE_STANDBY                 = (0x00 << 0)  # Stand by
		self.BM1383AGLV_MODE_CONTROL_MODE_ONE_SHOT                = (0x01 << 0)  # One shot
		self.BM1383AGLV_MODE_CONTROL_MODE_CONTINUOUS              = (0x02 << 0)  # Continuous
		self.BM1383AGLV_MODE_CONTROL_MODE_PROHIBITED              = (0x03 << 0)  # Prohibition
		self.BM1383AGLV_STATUS_RD_DRDY_NOT_READY                  = (0x00 << 0)  # Data is not ready
		self.BM1383AGLV_STATUS_RD_DRDY_READY                      = (0x01 << 0)  # Data is ready
		self.BM1383AGLV_STATUS_RD_DRDY                            = (0x01 << 0)  # Pressure and temperature measurement data ready bit
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BM1383AGLV_POWER_DOWN_PWR_DOWN={
			'DOWN':_b.BM1383AGLV_POWER_DOWN_PWR_DOWN_DOWN,
			'UP':_b.BM1383AGLV_POWER_DOWN_PWR_DOWN_UP,
		}
		self.BM1383AGLV_RESET_RSTB={
			'RESET':_b.BM1383AGLV_RESET_RSTB_RESET,
			'STANDBY':_b.BM1383AGLV_RESET_RSTB_STANDBY,
		}
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM={
			'AVG_1_60MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_1_60MS,
			'AVG_2_60MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_2_60MS,
			'AVG_4_60MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_4_60MS,
			'AVG_8_60MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_8_60MS,
			'AVG_16_60MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS,
			'AVG_32_120MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_32_120MS,
			'AVG_64_240MS':_b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_64_240MS,
		}
		self.BM1383AGLV_MODE_CONTROL_DREN={
			'DISABLED':_b.BM1383AGLV_MODE_CONTROL_DREN_DISABLED,
			'ENABLED':_b.BM1383AGLV_MODE_CONTROL_DREN_ENABLED,
		}
		self.BM1383AGLV_MODE_CONTROL_MODE={
			'STANDBY':_b.BM1383AGLV_MODE_CONTROL_MODE_STANDBY,
			'ONE_SHOT':_b.BM1383AGLV_MODE_CONTROL_MODE_ONE_SHOT,
			'CONTINUOUS':_b.BM1383AGLV_MODE_CONTROL_MODE_CONTINUOUS,
			'PROHIBITED':_b.BM1383AGLV_MODE_CONTROL_MODE_PROHIBITED,
		}
		self.BM1383AGLV_STATUS_RD_DRDY={
			'NOT_READY':_b.BM1383AGLV_STATUS_RD_DRDY_NOT_READY,
			'READY':_b.BM1383AGLV_STATUS_RD_DRDY_READY,
		}
class masks(register_base):
	def __init__(self):
		self.BM1383AGLV_ID1_ID1_MASK                              = 0xFF         
		self.BM1383AGLV_ID2_ID2_MASK                              = 0xFF         
		self.BM1383AGLV_POWER_DOWN_PWR_DOWN_MASK                  = 0x01         # Power enable
		self.BM1383AGLV_RESET_RSTB_MASK                           = 0x01         # Measurement control block reset
		self.BM1383AGLV_MODE_CONTROL_AVE_NUM_MASK                 = 0xE0         # Set the average number of measurement data
		self.BM1383AGLV_MODE_CONTROL_DREN_MASK                    = 0x10         # DRDY pin Enable
		self.BM1383AGLV_MODE_CONTROL_RESERVED3_MASK               = 0x08         # Reserved
		self.BM1383AGLV_MODE_CONTROL_RESERVED2_MASK               = 0x04         # Reserved; write 0
		self.BM1383AGLV_MODE_CONTROL_MODE_MASK                    = 0x03         # Set measurement mode
		self.BM1383AGLV_STATUS_RD_DRDY_MASK                       = 0x01         # Pressure and temperature measurement data ready bit
		self.BM1383AGLV_PRESSURE_LSB_PRESS_OUT_MASK               = 0xFF         # The lower part of pressure data
		self.BM1383AGLV_PRESSURE_LSB2_PRESS_OUT_XL_MASK           = 0xFC         # Pressure data output (decimal extension 6bit)