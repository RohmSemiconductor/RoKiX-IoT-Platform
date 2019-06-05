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
		self.BH1749_REGISTER_DUMP_START                           = 0x40         
		self.BH1749_SYSTEM_CONTROL                                = 0x40         
		self.BH1749_MODE_CONTROL1                                 = 0x41         
		self.BH1749_MODE_CONTROL2                                 = 0x42         
		self.BH1749_RED_DATA_LSBS                                 = 0x50         # Least significant byte of uint16 RED measurement value
		self.BH1749_RED_DATA_MSBS                                 = 0x51         # Most significant byte of uint16 RED measurement value
		self.BH1749_GREEN_DATA_LSBS                               = 0x52         # Least significant byte of uint16 GREEN measurement value
		self.BH1749_GREEN_DATA_MSBS                               = 0x53         # Most significant byte of uint16 GREEN measurement value
		self.BH1749_BLUE_DATA_LSBS                                = 0x54         # Least significant byte of uint16 BLUE measurement value
		self.BH1749_BLUE_DATA_MSBS                                = 0x55         # Most significant byte of uint16 BLUE measurement value
		self.BH1749_IR_DATA_LSBS                                  = 0x58         # Least significant byte of uint16 IR measurement value
		self.BH1749_IR_DATA_MSBS                                  = 0x59         # Most significant byte of uint16 IR measurement value
		self.BH1749_GREEN2_DATA_LSBS                              = 0x5A         # Least significant byte of uint16 GREEN2 measurement value
		self.BH1749_GREEN2_DATA_MSBS                              = 0x5B         # Most significant byte of uint16 GREEN2 measurement value
		self.BH1749_INTERRUPT                                     = 0x60         # Interrupt control register
		self.BH1749_PERSISTENCE                                   = 0x61         # Interrupt status update control register
		self.BH1749_TH_LSBS                                       = 0x62         # Least significant byte of interrupt threshold high level
		self.BH1749_TH_MSBS                                       = 0x63         # Most significant byte of interrupt threshold high level
		self.BH1749_TL_LSBS                                       = 0x64         # Least significant byte of interrupt threshold low level
		self.BH1749_TL_MSBS                                       = 0x65         # Most significant byte of interrupt threshold low level
		self.BH1749_ID_REG                                        = 0x92         
		self.BH1749_REGISTER_DUMP_END                             = 0x92         
class bits(register_base):
	def __init__(self):
		self.BH1749_SYSTEM_CONTROL_SW_RESET_NOT_DONE              = (0x00 << 7)  # Software reset is not done
		self.BH1749_SYSTEM_CONTROL_SW_RESET_DONE                  = (0x01 << 7)  # Software reset is done
		self.BH1749_SYSTEM_CONTROL_SW_RESET                       = (0x01 << 7)  # In specification named as SW_RESET
		self.BH1749_SYSTEM_CONTROL_INT_NO_ACTION                  = (0x00 << 6)  # INT pin status is not changed
		self.BH1749_SYSTEM_CONTROL_INT_RESET                      = (0x01 << 6)  # INT pin becomes inactive (high impedance)
		self.BH1749_SYSTEM_CONTROL_INT                            = (0x01 << 6)  
		self.BH1749_SYSTEM_CONTROL_PART_ID                        = (0x0D << 0)  
		self.BH1749_MODE_CONTROL1_RESERVED7_WRITE0                = (0x00 << 7)  
		self.BH1749_MODE_CONTROL1_RESERVED7                       = (0x01 << 7)  
		self.BH1749_MODE_CONTROL1_IR_GAIN_RESERVED0               = (0x00 << 5)  
		self.BH1749_MODE_CONTROL1_IR_GAIN_1X                      = (0x01 << 5)  
		self.BH1749_MODE_CONTROL1_IR_GAIN_RESERVED1               = (0x02 << 5)  
		self.BH1749_MODE_CONTROL1_IR_GAIN_32X                     = (0x03 << 5)  
		self.BH1749_MODE_CONTROL1_RGB_GAIN_RESERVED0              = (0x00 << 3)  
		self.BH1749_MODE_CONTROL1_RGB_GAIN_1X                     = (0x01 << 3)  
		self.BH1749_MODE_CONTROL1_RGB_GAIN_RESERVED1              = (0x02 << 3)  
		self.BH1749_MODE_CONTROL1_RGB_GAIN_32X                    = (0x03 << 3)  
		self.BH1749_MODE_CONTROL1_ODR_RESERVED0                   = (0x00 << 0)  # Reserved value
		self.BH1749_MODE_CONTROL1_ODR_RESERVED1                   = (0x01 << 0)  # Reserved value
		self.BH1749_MODE_CONTROL1_ODR_8P333                       = (0x02 << 0)  # 120ms measurement time
		self.BH1749_MODE_CONTROL1_ODR_4P167                       = (0x03 << 0)  # 240ms measurement time
		self.BH1749_MODE_CONTROL1_ODR_RESERVED2                   = (0x04 << 0)  # Reserved value
		self.BH1749_MODE_CONTROL1_ODR_28P6                        = (0x05 << 0)  # 35ms measurement time
		self.BH1749_MODE_CONTROL1_ODR_RESERVED3                   = (0x06 << 0)  # Reserved value
		self.BH1749_MODE_CONTROL1_ODR_RESERVED4                   = (0x07 << 0)  # Reserved value
		self.BH1749_MODE_CONTROL2_VALID_NO                        = (0x00 << 7)  
		self.BH1749_MODE_CONTROL2_VALID_YES                       = (0x01 << 7)  
		self.BH1749_MODE_CONTROL2_VALID                           = (0x01 << 7)  # Measurement data update flag. Sets to 0 if MODE_CONTROL1/2 reg, MODE_CONTROL2, INTERRUPT, T(H/L)_(LSB/MSB) is written or MODE_CONTROL2 read. In specification named as VALID.
		self.BH1749_MODE_CONTROL2_RESERVED65_WRITE00              = (0x00 << 5)  
		self.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_INACTIVE        = (0x00 << 4)  
		self.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_ACTIVE          = (0x01 << 4)  
		self.BH1749_MODE_CONTROL2_RGB_MEASUREMENT                 = (0x01 << 4)  # In specification named as RGBC_EN
		self.BH1749_MODE_CONTROL2_RESERVED30_WRITE0000            = (0x00 << 0)  
		self.BH1749_INTERRUPT_STATUS_INACTIVE                     = (0x00 << 7)  
		self.BH1749_INTERRUPT_STATUS_ACTIVE                       = (0x01 << 7)  
		self.BH1749_INTERRUPT_STATUS                              = (0x01 << 7)  # Interrupt status output (Read only value)
		self.BH1749_INTERRUPT_RESERVED64_WRITE000                 = (0x00 << 4)  
		self.BH1749_INTERRUPT_SOURCE_SELECT_RED                   = (0x00 << 2)  # red channel
		self.BH1749_INTERRUPT_SOURCE_SELECT_GREEN                 = (0x01 << 2)  # green channel
		self.BH1749_INTERRUPT_SOURCE_SELECT_BLUE                  = (0x02 << 2)  # blue channel
		self.BH1749_INTERRUPT_SOURCE_RESERVED0                    = (0x03 << 2)  # Reserved value
		self.BH1749_INTERRUPT_RESERVED1_WRITE0                    = (0x00 << 1)  
		self.BH1749_INTERRUPT_RESERVED1                           = (0x01 << 1)  # Write 0
		self.BH1749_INTERRUPT_EN_DISABLE                          = (0x00 << 0)  
		self.BH1749_INTERRUPT_EN_ENABLE                           = (0x01 << 0)  
		self.BH1749_INTERRUPT_EN                                  = (0x01 << 0)  # In specification named as INT ENABLE
		self.BH1749_PERSISTENCE_RESERVED72_WRITE000000            = (0x00 << 2)  
		self.BH1749_PERSISTENCE_MODE_STATUS_ACTIVE_AFTER_MEASUREMENT = (0x00 << 0)  # Interrupt status becomes active at each measurement end.
		self.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_MEASUREMENT = (0x01 << 0)  # Interrupt status is updated at each measurement end.
		self.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_4_SAME   = (0x02 << 0)  # Interrupt status is updated if 4 consecutive threshold judgements are the same
		self.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_8_SAME   = (0x03 << 0)  # Interrupt status is updated if 8 consecutive threshold judgements are the same
		self.BH1749_ID_REG_MANUFACTURER_ID                        = (0xE0 << 0)  # Manufacturer ID
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1749_INTERRUPT_EN={
			'DISABLE':_b.BH1749_INTERRUPT_EN_DISABLE,
			'ENABLE':_b.BH1749_INTERRUPT_EN_ENABLE,
		}
		self.BH1749_MODE_CONTROL1_ODR={
			'4P167':_b.BH1749_MODE_CONTROL1_ODR_4P167,
			'8P333':_b.BH1749_MODE_CONTROL1_ODR_8P333,
			'RESERVED1':_b.BH1749_MODE_CONTROL1_ODR_RESERVED1,
			'RESERVED4':_b.BH1749_MODE_CONTROL1_ODR_RESERVED4,
			'28P6':_b.BH1749_MODE_CONTROL1_ODR_28P6,
			'RESERVED0':_b.BH1749_MODE_CONTROL1_ODR_RESERVED0,
			'RESERVED3':_b.BH1749_MODE_CONTROL1_ODR_RESERVED3,
			'RESERVED2':_b.BH1749_MODE_CONTROL1_ODR_RESERVED2,
		}
		self.BH1749_INTERRUPT_SOURCE={
			'SELECT_GREEN':_b.BH1749_INTERRUPT_SOURCE_SELECT_GREEN,
			'SELECT_BLUE':_b.BH1749_INTERRUPT_SOURCE_SELECT_BLUE,
			'RESERVED0':_b.BH1749_INTERRUPT_SOURCE_RESERVED0,
			'SELECT_RED':_b.BH1749_INTERRUPT_SOURCE_SELECT_RED,
		}
		self.BH1749_PERSISTENCE_MODE={
			'STATUS_UPDATE_AFTER_4_SAME':_b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_4_SAME,
			'STATUS_UPDATE_AFTER_MEASUREMENT':_b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_MEASUREMENT,
			'STATUS_ACTIVE_AFTER_MEASUREMENT':_b.BH1749_PERSISTENCE_MODE_STATUS_ACTIVE_AFTER_MEASUREMENT,
			'STATUS_UPDATE_AFTER_8_SAME':_b.BH1749_PERSISTENCE_MODE_STATUS_UPDATE_AFTER_8_SAME,
		}
		self.BH1749_INTERRUPT_STATUS={
			'ACTIVE':_b.BH1749_INTERRUPT_STATUS_ACTIVE,
			'INACTIVE':_b.BH1749_INTERRUPT_STATUS_INACTIVE,
		}
		self.BH1749_SYSTEM_CONTROL_INT={
			'RESET':_b.BH1749_SYSTEM_CONTROL_INT_RESET,
			'NO_ACTION':_b.BH1749_SYSTEM_CONTROL_INT_NO_ACTION,
		}
		self.BH1749_MODE_CONTROL1_RGB_GAIN={
			'1X':_b.BH1749_MODE_CONTROL1_RGB_GAIN_1X,
			'32X':_b.BH1749_MODE_CONTROL1_RGB_GAIN_32X,
			'RESERVED1':_b.BH1749_MODE_CONTROL1_RGB_GAIN_RESERVED1,
			'RESERVED0':_b.BH1749_MODE_CONTROL1_RGB_GAIN_RESERVED0,
		}
		self.BH1749_SYSTEM_CONTROL_SW_RESET={
			'DONE':_b.BH1749_SYSTEM_CONTROL_SW_RESET_DONE,
			'NOT_DONE':_b.BH1749_SYSTEM_CONTROL_SW_RESET_NOT_DONE,
		}
		self.BH1749_MODE_CONTROL2_VALID={
			'YES':_b.BH1749_MODE_CONTROL2_VALID_YES,
			'NO':_b.BH1749_MODE_CONTROL2_VALID_NO,
		}
		self.BH1749_MODE_CONTROL2_RGB_MEASUREMENT={
			'ACTIVE':_b.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_ACTIVE,
			'INACTIVE':_b.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_INACTIVE,
		}
		self.BH1749_MODE_CONTROL1_IR_GAIN={
			'1X':_b.BH1749_MODE_CONTROL1_IR_GAIN_1X,
			'32X':_b.BH1749_MODE_CONTROL1_IR_GAIN_32X,
			'RESERVED1':_b.BH1749_MODE_CONTROL1_IR_GAIN_RESERVED1,
			'RESERVED0':_b.BH1749_MODE_CONTROL1_IR_GAIN_RESERVED0,
		}
class masks(register_base):
	def __init__(self):
		self.BH1749_SYSTEM_CONTROL_SW_RESET_MASK                  = 0x80         # In specification named as SW_RESET
		self.BH1749_SYSTEM_CONTROL_INT_MASK                       = 0x40         
		self.BH1749_SYSTEM_CONTROL_PART_MASK                      = 0x3F         
		self.BH1749_MODE_CONTROL1_RESERVED7_MASK                  = 0x80         
		self.BH1749_MODE_CONTROL1_IR_GAIN_MASK                    = 0x60         
		self.BH1749_MODE_CONTROL1_RGB_GAIN_MASK                   = 0x18         
		self.BH1749_MODE_CONTROL1_ODR_MASK                        = 0x07         # In specification named as MEASUREMENT MODE
		self.BH1749_MODE_CONTROL2_VALID_MASK                      = 0x80         # Measurement data update flag. Sets to 0 if MODE_CONTROL1/2 reg, MODE_CONTROL2, INTERRUPT, T(H/L)_(LSB/MSB) is written or MODE_CONTROL2 read. In specification named as VALID.
		self.BH1749_MODE_CONTROL2_RESERVED65_MASK                 = 0x60         # write 00
		self.BH1749_MODE_CONTROL2_RGB_MEASUREMENT_MASK            = 0x10         # In specification named as RGBC_EN
		self.BH1749_MODE_CONTROL2_RESERVED30_MASK                 = 0x0F         # write 0000
		self.BH1749_INTERRUPT_STATUS_MASK                         = 0x80         # Interrupt status output (Read only value)
		self.BH1749_INTERRUPT_RESERVED64_MASK                     = 0x70         
		self.BH1749_INTERRUPT_SOURCE_MASK                         = 0x0C         
		self.BH1749_INTERRUPT_RESERVED1_MASK                      = 0x02         # Write 0
		self.BH1749_INTERRUPT_EN_MASK                             = 0x01         # In specification named as INT ENABLE
		self.BH1749_PERSISTENCE_RESERVED72_MASK                   = 0xFC         
		self.BH1749_PERSISTENCE_MODE_MASK                         = 0x03         # In specification named as PERSISTENCE
		self.BH1749_ID_REG_MANUFACTURER_MASK                      = 0xFF         