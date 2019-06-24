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
		self.BH1749NUC_REGISTER_DUMP_START                        = 0x40         
		self.BH1749NUC_SYSTEM_CONTROL                             = 0x40         # System control register
		self.BH1749NUC_MODE_CONTROL1                              = 0x41         # Control register 1
		self.BH1749NUC_MODE_CONTROL2                              = 0x42         # Control register 2
		self.BH1749NUC_RED_DATA_LSB                               = 0x50         # RED measurement result [7:0]
		self.BH1749NUC_RED_DATA_MSB                               = 0x51         # RED measurement result [15:8]
		self.BH1749NUC_GREEN_DATA_LSB                             = 0x52         # GREEN measurement result [7:0]
		self.BH1749NUC_GREEN_DATA_MSB                             = 0x53         # GREEN measurement result [15:8]
		self.BH1749NUC_BLUE_DATA_LSB                              = 0x54         # BLUE measurement result [7:0]
		self.BH1749NUC_BLUE_DATA_MSB                              = 0x55         # BLUE measurement result [15:8]
		self.BH1749NUC_IR_DATA_LSB                                = 0x58         # IR measurement result [7:0]
		self.BH1749NUC_IR_DATA_MSB                                = 0x59         # IR measurement result [15:8]
		self.BH1749NUC_GREEN2_DATA_LSB                            = 0x5A         # GREEN2 measurement result [7:0]
		self.BH1749NUC_GREEN2_DATA_MSB                            = 0x5B         # GREEN2 measurement result [15:8]
		self.BH1749NUC_INTERRUPT                                  = 0x60         # Interrupt control register
		self.BH1749NUC_PERSISTENCE                                = 0x61         # Interrupt persistence setting.
		self.BH1749NUC_TH_HIGH_LSB                                = 0x62         # Interrupt threshold upper level
		self.BH1749NUC_TH_HIGH_MSB                                = 0x63         # Interrupt threshold upper level [15:8]
		self.BH1749NUC_TH_LOW_LSB                                 = 0x64         # Interrupt threshold lower level
		self.BH1749NUC_TH_LOW_MSB                                 = 0x65         # Interrupt threshold lower level [15:8]
		self.BH1749NUC_MANUFACTURER_ID                            = 0x92         # Manufacturer ID
		self.BH1749NUC_REGISTER_DUMP_END                          = 0x92         
class bits(register_base):
	def __init__(self):
		self.BH1749NUC_SYSTEM_CONTROL_SW_RESET_NOT_DONE           = (0x00 << 7)  # Software reset is not done
		self.BH1749NUC_SYSTEM_CONTROL_SW_RESET_DONE               = (0x01 << 7)  # Software reset is done
		self.BH1749NUC_SYSTEM_CONTROL_SW_RESET                    = (0x01 << 7)  # All registers are reset and this IC is in power down state by software reset
		self.BH1749NUC_SYSTEM_CONTROL_INT_RESET_NO_ACTION         = (0x00 << 6)  # INT pin status is not changed
		self.BH1749NUC_SYSTEM_CONTROL_INT_RESET_RESET             = (0x01 << 6)  # INT pin becomes inactive (high impedance)
		self.BH1749NUC_SYSTEM_CONTROL_INT_RESET                   = (0x01 << 6)  # INT-pin high-impedance control
		self.BH1749NUC_SYSTEM_CONTROL_PART_ID_ID                  = (0x0D << 0)  # Part ID 0x0D (read only)
		self.BH1749NUC_MODE_CONTROL1_IR_GAIN_FORBIDDEN            = (0x00 << 5)  # Forbidden to use
		self.BH1749NUC_MODE_CONTROL1_IR_GAIN_1X                   = (0x01 << 5)  # x1 gain mode
		self.BH1749NUC_MODE_CONTROL1_IR_GAIN_32X                  = (0x03 << 5)  # x32 gain mode
		self.BH1749NUC_MODE_CONTROL1_RGB_GAIN_FORBIDDEN           = (0x00 << 3)  # Forbidden to use
		self.BH1749NUC_MODE_CONTROL1_RGB_GAIN_1X                  = (0x01 << 3)  # x1 gain mode
		self.BH1749NUC_MODE_CONTROL1_RGB_GAIN_32X                 = (0x03 << 3)  # x32 gain mode
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_FORBIDDEN   = (0x00 << 0)  # Forbidden to use
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_8P333       = (0x02 << 0)  # 120 ms measurement time
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_4P167       = (0x03 << 0)  # 240 ms measurement time
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_28P6        = (0x05 << 0)  # 35 ms measurement time
		self.BH1749NUC_MODE_CONTROL2_VALID_NO                     = (0x00 << 7)  # Register setup changed or VALID has been read
		self.BH1749NUC_MODE_CONTROL2_VALID_YES                    = (0x01 << 7)  # Measurement data has been updated
		self.BH1749NUC_MODE_CONTROL2_VALID                        = (0x01 << 7)  # Measurement data update flag. Sets to 0 if MODE_CONTROL1/2 reg, MODE_CONTROL2, INTERRUPT, T(H/L)_(LSB/MSB) is written or MODE_CONTROL2 read.
		self.BH1749NUC_MODE_CONTROL2_RGB_EN_INACTIVE              = (0x00 << 4)  # Measurement is inactive and becomes power down.
		self.BH1749NUC_MODE_CONTROL2_RGB_EN_ACTIVE                = (0x01 << 4)  # Measurement is active.
		self.BH1749NUC_MODE_CONTROL2_RGB_EN                       = (0x01 << 4)  # Measurement enable
		self.BH1749NUC_INTERRUPT_INT_STATUS_INACTIVE              = (0x00 << 7)  # Interrupt signal is inactive
		self.BH1749NUC_INTERRUPT_INT_STATUS_ACTIVE                = (0x01 << 7)  # Interrupt signal is active
		self.BH1749NUC_INTERRUPT_INT_STATUS                       = (0x01 << 7)  # Interrupt status output. (Read only register)
		self.BH1749NUC_INTERRUPT_INT_SOURCE_RED                   = (0x00 << 2)  # Red channel
		self.BH1749NUC_INTERRUPT_INT_SOURCE_GREEN                 = (0x01 << 2)  # Green channel
		self.BH1749NUC_INTERRUPT_INT_SOURCE_BLUE                  = (0x02 << 2)  # Blue channel
		self.BH1749NUC_INTERRUPT_INT_ENABLE_DISABLE               = (0x00 << 0)  # The INT pin disable.
		self.BH1749NUC_INTERRUPT_INT_ENABLE_ENABLE                = (0x01 << 0)  # The INT pin enable.
		self.BH1749NUC_INTERRUPT_INT_ENABLE                       = (0x01 << 0)  # INT-pin enable
		self.BH1749NUC_PERSISTENCE_PERSISTENCE_ACTIVE_AFTER_MEASUREMENT = (0x00 << 0)  # Interrupt status becomes active at each measurement end.
		self.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_MEASUREMENT = (0x01 << 0)  # Interrupt status is updated at each measurement end.
		self.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_4_SAME = (0x02 << 0)  # Interrupt status is updated if 4 consecutive threshold judgements are the same
		self.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_8_SAME = (0x03 << 0)  # Interrupt status is updated if 8 consecutive threshold judgements are the same
		self.BH1749NUC_MANUFACTURER_ID_MANUFACTURER_ID_ID         = (0xE0 << 0)  # Manufacturer ID
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1749NUC_INTERRUPT_INT_STATUS={
			'ACTIVE':_b.BH1749NUC_INTERRUPT_INT_STATUS_ACTIVE,
			'INACTIVE':_b.BH1749NUC_INTERRUPT_INT_STATUS_INACTIVE,
		}
		self.BH1749NUC_INTERRUPT_INT_SOURCE={
			'BLUE':_b.BH1749NUC_INTERRUPT_INT_SOURCE_BLUE,
			'GREEN':_b.BH1749NUC_INTERRUPT_INT_SOURCE_GREEN,
			'RED':_b.BH1749NUC_INTERRUPT_INT_SOURCE_RED,
		}
		self.BH1749NUC_INTERRUPT_INT_ENABLE={
			'DISABLE':_b.BH1749NUC_INTERRUPT_INT_ENABLE_DISABLE,
			'ENABLE':_b.BH1749NUC_INTERRUPT_INT_ENABLE_ENABLE,
		}
		self.BH1749NUC_PERSISTENCE_PERSISTENCE={
			'UPDATE_AFTER_MEASUREMENT':_b.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_MEASUREMENT,
			'ACTIVE_AFTER_MEASUREMENT':_b.BH1749NUC_PERSISTENCE_PERSISTENCE_ACTIVE_AFTER_MEASUREMENT,
			'UPDATE_AFTER_4_SAME':_b.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_4_SAME,
			'UPDATE_AFTER_8_SAME':_b.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_8_SAME,
		}
		self.BH1749NUC_MODE_CONTROL2_RGB_EN={
			'ACTIVE':_b.BH1749NUC_MODE_CONTROL2_RGB_EN_ACTIVE,
			'INACTIVE':_b.BH1749NUC_MODE_CONTROL2_RGB_EN_INACTIVE,
		}
		self.BH1749NUC_MODE_CONTROL1_RGB_GAIN={
			'1X':_b.BH1749NUC_MODE_CONTROL1_RGB_GAIN_1X,
			'FORBIDDEN':_b.BH1749NUC_MODE_CONTROL1_RGB_GAIN_FORBIDDEN,
			'32X':_b.BH1749NUC_MODE_CONTROL1_RGB_GAIN_32X,
		}
		self.BH1749NUC_SYSTEM_CONTROL_SW_RESET={
			'DONE':_b.BH1749NUC_SYSTEM_CONTROL_SW_RESET_DONE,
			'NOT_DONE':_b.BH1749NUC_SYSTEM_CONTROL_SW_RESET_NOT_DONE,
		}
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE={
			'8P333':_b.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_8P333,
			'4P167':_b.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_4P167,
			'FORBIDDEN':_b.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_FORBIDDEN,
			'28P6':_b.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_28P6,
		}
		self.BH1749NUC_MODE_CONTROL2_VALID={
			'YES':_b.BH1749NUC_MODE_CONTROL2_VALID_YES,
			'NO':_b.BH1749NUC_MODE_CONTROL2_VALID_NO,
		}
		self.BH1749NUC_SYSTEM_CONTROL_INT_RESET={
			'RESET':_b.BH1749NUC_SYSTEM_CONTROL_INT_RESET_RESET,
			'NO_ACTION':_b.BH1749NUC_SYSTEM_CONTROL_INT_RESET_NO_ACTION,
		}
		self.BH1749NUC_MODE_CONTROL1_IR_GAIN={
			'1X':_b.BH1749NUC_MODE_CONTROL1_IR_GAIN_1X,
			'FORBIDDEN':_b.BH1749NUC_MODE_CONTROL1_IR_GAIN_FORBIDDEN,
			'32X':_b.BH1749NUC_MODE_CONTROL1_IR_GAIN_32X,
		}
class masks(register_base):
	def __init__(self):
		self.BH1749NUC_SYSTEM_CONTROL_SW_RESET_MASK               = 0x80         # All registers are reset and this IC is in power down state by software reset
		self.BH1749NUC_SYSTEM_CONTROL_INT_RESET_MASK              = 0x40         # INT-pin high-impedance control
		self.BH1749NUC_SYSTEM_CONTROL_PART_ID_MASK                = 0x3F         # Part ID 0x0D (read only)
		self.BH1749NUC_MODE_CONTROL1_IR_GAIN_MASK                 = 0x60         # Gain setting for IR data
		self.BH1749NUC_MODE_CONTROL1_RGB_GAIN_MASK                = 0x18         # Gain setting for RGB data
		self.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_MASK        = 0x07         # Measurement mode
		self.BH1749NUC_MODE_CONTROL2_VALID_MASK                   = 0x80         # Measurement data update flag. Sets to 0 if MODE_CONTROL1/2 reg, MODE_CONTROL2, INTERRUPT, T(H/L)_(LSB/MSB) is written or MODE_CONTROL2 read.
		self.BH1749NUC_MODE_CONTROL2_RGB_EN_MASK                  = 0x10         # Measurement enable
		self.BH1749NUC_INTERRUPT_INT_STATUS_MASK                  = 0x80         # Interrupt status output. (Read only register)
		self.BH1749NUC_INTERRUPT_INT_SOURCE_MASK                  = 0x0C         # INT source select
		self.BH1749NUC_INTERRUPT_INT_ENABLE_MASK                  = 0x01         # INT-pin enable
		self.BH1749NUC_PERSISTENCE_PERSISTENCE_MASK               = 0x03         # Interrupt persistence setting.
		self.BH1749NUC_MANUFACTURER_ID_MANUFACTURER_ID_MASK       = 0xFF         # Manufacturer ID