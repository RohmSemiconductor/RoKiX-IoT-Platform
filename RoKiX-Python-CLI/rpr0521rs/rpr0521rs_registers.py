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
		self.RPR0521RS_REGISTER_DUMP_START                        = 0x40         
		self.RPR0521RS_SYSTEM_CONTROL                             = 0x40         # System control
		self.RPR0521RS_MODE_CONTROL                               = 0x41         # ALS, PS function setting
		self.RPR0521RS_ALS_PS_CONTROL                             = 0x42         # ALS Gain, PS LED Driver
		self.RPR0521RS_PS_CONTROL                                 = 0x43         # PS Gain, PS interrupt persistence
		self.RPR0521RS_PS_DATA_LSBS                               = 0x44         # PS data low byte
		self.RPR0521RS_PS_DATA_MSBS                               = 0x45         # PS data high byte
		self.RPR0521RS_ALS_DATA0_LSBS                             = 0x46         # ALS DATA0 low byte
		self.RPR0521RS_ALS_DATA0_MSBS                             = 0x47         # ALS DATA0 high byte
		self.RPR0521RS_ALS_DATA1_LSBS                             = 0x48         # ALS DATA1 low byte
		self.RPR0521RS_ALS_DATA1_MSBS                             = 0x49         # ALS DATA1 high byte
		self.RPR0521RS_INTERRUPT                                  = 0x4A         # Interrupt control
		self.RPR0521RS_PS_TH_LSBS                                 = 0x4B         # PS upper threshold low byte
		self.RPR0521RS_PS_TH_MSBS                                 = 0x4C         # PS upper threshold high byte
		self.RPR0521RS_PS_TL_LSBS                                 = 0x4D         # PS lower threshold low byte
		self.RPR0521RS_PS_TL_MSBS                                 = 0x4E         # PS lower threshold high byte
		self.RPR0521RS_ALS_DATA0_TH_LSBS                          = 0x4F         # ALS DATA0 upper threshold low byte
		self.RPR0521RS_ALS_DATA0_TH_MSBS                          = 0x50         # ALS DATA0 upper threshold high byte
		self.RPR0521RS_ALS_DATA0_TL_LSBS                          = 0x51         # ALS DATA0 lower threshold low byte
		self.RPR0521RS_ALS_DATA0_TL_MSBS                          = 0x52         # ALS DATA0 lower threshold high byte
		self.RPR0521RS_PS_OFFSET_LSBS                             = 0x53         # PS offset low byte
		self.RPR0521RS_PS_OFFSET_MSBS                             = 0x54         # PS offset high byte
		self.RPR0521RS_MANUFACT_ID                                = 0x92         # MANUFACT ID
		self.RPR0521RS_REGISTER_DUMP_END                          = 0x54         
class bits(register_base):
	def __init__(self):
		self.RPR0521RS_SYSTEM_CONTROL_SW_RESET_NOT_STARTED        = (0x00 << 7)  # Initial reset is not started
		self.RPR0521RS_SYSTEM_CONTROL_SW_RESET_START              = (0x01 << 7)  # Initial reset is started
		self.RPR0521RS_SYSTEM_CONTROL_SW_RESET                    = (0x01 << 7)  # Reset control
		self.RPR0521RS_SYSTEM_CONTROL_INT_PIN_NO_INIT             = (0x00 << 6)  # INT pin status is not initialized
		self.RPR0521RS_SYSTEM_CONTROL_INT_PIN_HI_Z                = (0x01 << 6)  # INT pin become inactive (high impedance)
		self.RPR0521RS_SYSTEM_CONTROL_INT_PIN                     = (0x01 << 6)  # INT pin control
		self.RPR0521RS_SYSTEM_CONTROL_PART_ID                     = (0x0A << 0)  # Part ID
		self.RPR0521RS_MODE_CONTROL_ALS_EN_FALSE                  = (0x00 << 7)  # ALS Standby
		self.RPR0521RS_MODE_CONTROL_ALS_EN_TRUE                   = (0x01 << 7)  # ALS Enable
		self.RPR0521RS_MODE_CONTROL_ALS_EN                        = (0x01 << 7)  # ALS enable
		self.RPR0521RS_MODE_CONTROL_PS_EN_FALSE                   = (0x00 << 6)  # PS Standby
		self.RPR0521RS_MODE_CONTROL_PS_EN_TRUE                    = (0x01 << 6)  # PS Enable
		self.RPR0521RS_MODE_CONTROL_PS_EN                         = (0x01 << 6)  # Proximity enable
		self.RPR0521RS_MODE_CONTROL_PS_PULSE_200US                = (0x00 << 5)  # PS LED pulse width is typ 200us
		self.RPR0521RS_MODE_CONTROL_PS_PULSE_330US                = (0x01 << 5)  # PS LED pulse width is typ 330us (PS sensor out is doubled)
		self.RPR0521RS_MODE_CONTROL_PS_PULSE                      = (0x01 << 5)  # Proximity pulse width control
		self.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_NORMAL      = (0x00 << 4)  # Normal mode
		self.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT = (0x01 << 4)  # Twice measurement mode
		self.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE             = (0x01 << 4)  # PS Operating mode
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF      = (0x00 << 0)  # ALS standby, PS standby
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS     = (0x01 << 0)  # ALS standby, PS 10ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS     = (0x02 << 0)  # ALS standby, PS 40ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS    = (0x03 << 0)  # ALS standby, PS 100ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS    = (0x04 << 0)  # ALS standby, PS 400ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS   = (0x05 << 0)  # ALS 100ms, PS 50ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS  = (0x06 << 0)  # ALS 100ms, PS 100ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS  = (0x07 << 0)  # ALS 100ms, PS 400ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS   = (0x08 << 0)  # ALS 100ms + 300ms sleep, PS 50ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS  = (0x09 << 0)  # ALS 100ms + 300ms sleep, PS 100ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF    = (0x0A << 0)  # ALS 400ms (high sensitivity), PS standby
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS  = (0x0B << 0)  # ALS 400ms (high sensitivity), PS 400ms
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS    = (0x0C << 0)  # ALS 50ms, PS 50ms (special mode, see datasheet for details)
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1           = (0x00 << 4)  # x1 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2           = (0x01 << 4)  # x2 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64          = (0x02 << 4)  # x64 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128         = (0x03 << 4)  # x128 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1           = (0x00 << 2)  # x1 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2           = (0x01 << 2)  # x2 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64          = (0x02 << 2)  # x64 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128         = (0x03 << 2)  # x128 Gain mode
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_25MA            = (0x00 << 0)  # 25mA
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_50MA            = (0x01 << 0)  # 50mA
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_100MA           = (0x02 << 0)  # 100mA
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_200MA           = (0x03 << 0)  # 200mA
		self.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_LOW             = (0x00 << 6)  # Ambient infrared level is low
		self.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_HIGH            = (0x01 << 6)  # Ambient infrared level is high
		self.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_TOO_HIGH        = (0x02 << 6)  # Ambient infrared level is too high
		self.RPR0521RS_PS_CONTROL_PS_GAIN_X1                      = (0x00 << 4)  # PS GAIN x1
		self.RPR0521RS_PS_CONTROL_PS_GAIN_X2                      = (0x01 << 4)  # PS GAIN x2
		self.RPR0521RS_PS_CONTROL_PS_GAIN_X4                      = (0x02 << 4)  # PS GAIN x4
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_DRDY                = (0x00 << 0)  # Interrupt becomes active at each measurement end
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1       = (0x01 << 0)  # Interrupt status is updated at each measurement end
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2       = (0x02 << 0)  # Interrupt status is updated if two consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3       = (0x03 << 0)  # Interrupt status is updated if three consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4       = (0x04 << 0)  # Interrupt status is updated if four consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5       = (0x05 << 0)  # Interrupt status is updated if five consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6       = (0x06 << 0)  # Interrupt status is updated if six consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7       = (0x07 << 0)  # Interrupt status is updated if seven consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8       = (0x08 << 0)  # Interrupt status is updated if eight consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9       = (0x09 << 0)  # Interrupt status is updated if nine consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10      = (0x0A << 0)  # Interrupt status is updated if ten consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11      = (0x0B << 0)  # Interrupt status is updated if eleven consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12      = (0x0C << 0)  # Interrupt status is updated if twelve consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13      = (0x0D << 0)  # Interrupt status is updated if thirteen consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14      = (0x0E << 0)  # Interrupt status is updated if fourteen consecutive threshold judgments are the same
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15      = (0x0F << 0)  # Interrupt status is updated if fifteen consecutive threshold judgments are the same
		self.RPR0521RS_INTERRUPT_PS_INT_STATUS_INACTIVE           = (0x00 << 7)  # PS interrupt signal inactive
		self.RPR0521RS_INTERRUPT_PS_INT_STATUS_ACTIVE             = (0x01 << 7)  # PS interrupt signal active
		self.RPR0521RS_INTERRUPT_PS_INT_STATUS                    = (0x01 << 7)  # PS interrupt status
		self.RPR0521RS_INTERRUPT_ALS_INT_STATUS_INACTIVE          = (0x00 << 6)  # ALS interrupt signal inactive
		self.RPR0521RS_INTERRUPT_ALS_INT_STATUS_ACTIVE            = (0x01 << 6)  # ALS interrupt signal active
		self.RPR0521RS_INTERRUPT_ALS_INT_STATUS                   = (0x01 << 6)  # ALS interrupt status
		self.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_H_ACTIVE          = (0x00 << 4)  # Only PS_TH_H is effective
		self.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_HYSTERESIS        = (0x01 << 4)  # PS_TH_H and PS_TH_L are effective as hysteresis
		self.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION = (0x02 << 4)  # PS_TH_H and PS_TH_L are effective as outside detection
		self.RPR0521RS_INTERRUPT_INT_ASSERT_STABLE                = (0x00 << 3)  # Interrupt output 'L' is stable if newer measurement result is also interrupt active
		self.RPR0521RS_INTERRUPT_INT_ASSERT_REINT                 = (0x01 << 3)  # Interrupt output 'L' is de-assert and re-assert if newer measurement result is also interrupt active
		self.RPR0521RS_INTERRUPT_INT_ASSERT                       = (0x01 << 3)  # Interrupt assert control
		self.RPR0521RS_INTERRUPT_INT_LATCH_ENABLED                = (0x00 << 2)  # INT pin is latched until INTERRUPT register is read or initialized
		self.RPR0521RS_INTERRUPT_INT_LATCH_DISABLED               = (0x01 << 2)  # INT pin is updated after each measurement
		self.RPR0521RS_INTERRUPT_INT_LATCH                        = (0x01 << 2)  # Interrupt latch control
		self.RPR0521RS_INTERRUPT_INT_TRIG_INACTIVE                = (0x00 << 0)  # INT pin is inactive
		self.RPR0521RS_INTERRUPT_INT_TRIG_BY_PS                   = (0x01 << 0)  # Triggered by only PS measurement
		self.RPR0521RS_INTERRUPT_INT_TRIG_BY_ALS                  = (0x02 << 0)  # Triggered by only ALS measurement
		self.RPR0521RS_INTERRUPT_INT_TRIG_BY_BOTH                 = (0x03 << 0)  # Triggered by PS and ALS measurement
		self.RPR0521RS_MANUFACT_ID_ID_E0H                         = (0xE0 << 0)  # MANUFACT ID
_b=bits()
class enums(register_base):
	def __init__(self):
		self.RPR0521RS_SYSTEM_CONTROL_SW_RESET={
			'NOT_STARTED':_b.RPR0521RS_SYSTEM_CONTROL_SW_RESET_NOT_STARTED,
			'START':_b.RPR0521RS_SYSTEM_CONTROL_SW_RESET_START,
		}
		self.RPR0521RS_SYSTEM_CONTROL_INT_PIN={
			'NO_INIT':_b.RPR0521RS_SYSTEM_CONTROL_INT_PIN_NO_INIT,
			'HI_Z':_b.RPR0521RS_SYSTEM_CONTROL_INT_PIN_HI_Z,
		}
		self.RPR0521RS_MODE_CONTROL_ALS_EN={
			'FALSE':_b.RPR0521RS_MODE_CONTROL_ALS_EN_FALSE,
			'TRUE':_b.RPR0521RS_MODE_CONTROL_ALS_EN_TRUE,
		}
		self.RPR0521RS_MODE_CONTROL_PS_EN={
			'FALSE':_b.RPR0521RS_MODE_CONTROL_PS_EN_FALSE,
			'TRUE':_b.RPR0521RS_MODE_CONTROL_PS_EN_TRUE,
		}
		self.RPR0521RS_MODE_CONTROL_PS_PULSE={
			'200US':_b.RPR0521RS_MODE_CONTROL_PS_PULSE_200US,
			'330US':_b.RPR0521RS_MODE_CONTROL_PS_PULSE_330US,
		}
		self.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE={
			'NORMAL':_b.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_NORMAL,
			'DOUBLE_MEASUREMENT':_b.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT,
		}
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME={
			'OFF_OFF':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF,
			'OFF_10MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS,
			'OFF_40MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS,
			'OFF_100MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS,
			'OFF_400MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS,
			'100MS_50MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS,
			'100MS_100MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS,
			'100MS_400MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS,
			'400MS_50MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS,
			'400MS_100MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS,
			'400MS_OFF':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF,
			'400MS_400MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS,
			'50MS_50MS':_b.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS,
		}
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN={
			'X1':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1,
			'X2':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2,
			'X64':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64,
			'X128':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128,
		}
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN={
			'X1':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1,
			'X2':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2,
			'X64':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64,
			'X128':_b.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128,
		}
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT={
			'25MA':_b.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_25MA,
			'50MA':_b.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_50MA,
			'100MA':_b.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_100MA,
			'200MA':_b.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_200MA,
		}
		self.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG={
			'LOW':_b.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_LOW,
			'HIGH':_b.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_HIGH,
			'TOO_HIGH':_b.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_TOO_HIGH,
		}
		self.RPR0521RS_PS_CONTROL_PS_GAIN={
			'X1':_b.RPR0521RS_PS_CONTROL_PS_GAIN_X1,
			'X2':_b.RPR0521RS_PS_CONTROL_PS_GAIN_X2,
			'X4':_b.RPR0521RS_PS_CONTROL_PS_GAIN_X4,
		}
		self.RPR0521RS_PS_CONTROL_PERSISTENCE={
			'DRDY':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_DRDY,
			'CONSECUTIVE_1':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1,
			'CONSECUTIVE_2':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2,
			'CONSECUTIVE_3':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3,
			'CONSECUTIVE_4':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4,
			'CONSECUTIVE_5':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5,
			'CONSECUTIVE_6':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6,
			'CONSECUTIVE_7':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7,
			'CONSECUTIVE_8':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8,
			'CONSECUTIVE_9':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9,
			'CONSECUTIVE_10':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10,
			'CONSECUTIVE_11':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11,
			'CONSECUTIVE_12':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12,
			'CONSECUTIVE_13':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13,
			'CONSECUTIVE_14':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14,
			'CONSECUTIVE_15':_b.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15,
		}
		self.RPR0521RS_INTERRUPT_PS_INT_STATUS={
			'INACTIVE':_b.RPR0521RS_INTERRUPT_PS_INT_STATUS_INACTIVE,
			'ACTIVE':_b.RPR0521RS_INTERRUPT_PS_INT_STATUS_ACTIVE,
		}
		self.RPR0521RS_INTERRUPT_ALS_INT_STATUS={
			'INACTIVE':_b.RPR0521RS_INTERRUPT_ALS_INT_STATUS_INACTIVE,
			'ACTIVE':_b.RPR0521RS_INTERRUPT_ALS_INT_STATUS_ACTIVE,
		}
		self.RPR0521RS_INTERRUPT_INT_MODE={
			'PS_TH_H_ACTIVE':_b.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_H_ACTIVE,
			'PS_TH_HYSTERESIS':_b.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_HYSTERESIS,
			'PS_TH_OUTSIDE_DETECTION':_b.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION,
		}
		self.RPR0521RS_INTERRUPT_INT_ASSERT={
			'STABLE':_b.RPR0521RS_INTERRUPT_INT_ASSERT_STABLE,
			'REINT':_b.RPR0521RS_INTERRUPT_INT_ASSERT_REINT,
		}
		self.RPR0521RS_INTERRUPT_INT_LATCH={
			'ENABLED':_b.RPR0521RS_INTERRUPT_INT_LATCH_ENABLED,
			'DISABLED':_b.RPR0521RS_INTERRUPT_INT_LATCH_DISABLED,
		}
		self.RPR0521RS_INTERRUPT_INT_TRIG={
			'INACTIVE':_b.RPR0521RS_INTERRUPT_INT_TRIG_INACTIVE,
			'BY_PS':_b.RPR0521RS_INTERRUPT_INT_TRIG_BY_PS,
			'BY_ALS':_b.RPR0521RS_INTERRUPT_INT_TRIG_BY_ALS,
			'BY_BOTH':_b.RPR0521RS_INTERRUPT_INT_TRIG_BY_BOTH,
		}
class masks(register_base):
	def __init__(self):
		self.RPR0521RS_SYSTEM_CONTROL_SW_RESET_MASK               = 0x80         # Reset control
		self.RPR0521RS_SYSTEM_CONTROL_INT_PIN_MASK                = 0x40         # INT pin control
		self.RPR0521RS_SYSTEM_CONTROL_PART_MASK                   = 0x3F         # Part ID
		self.RPR0521RS_MODE_CONTROL_ALS_EN_MASK                   = 0x80         # ALS enable
		self.RPR0521RS_MODE_CONTROL_PS_EN_MASK                    = 0x40         # Proximity enable
		self.RPR0521RS_MODE_CONTROL_PS_PULSE_MASK                 = 0x20         # Proximity pulse width control
		self.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_MASK        = 0x10         # PS Operating mode
		self.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_MASK         = 0x0F         # Measurement time
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK         = 0x30         # Gain control of ALS DATA 0
		self.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK         = 0x0C         # Gain control of ALS DATA 1
		self.RPR0521RS_ALS_PS_CONTROL_LED_CURRENT_MASK            = 0x03         # LED current
		self.RPR0521RS_PS_CONTROL_AMBIENT_IR_FLAG_MASK            = 0xC0         # Ambient infrared level flag
		self.RPR0521RS_PS_CONTROL_PS_GAIN_MASK                    = 0x30         # Proximity gain
		self.RPR0521RS_PS_CONTROL_PERSISTENCE_MASK                = 0x0F         # PS interrupt persistence setting
		self.RPR0521RS_INTERRUPT_PS_INT_STATUS_MASK               = 0x80         # PS interrupt status
		self.RPR0521RS_INTERRUPT_ALS_INT_STATUS_MASK              = 0x40         # ALS interrupt status
		self.RPR0521RS_INTERRUPT_INT_MODE_MASK                    = 0x30         # Interrupt mode
		self.RPR0521RS_INTERRUPT_INT_ASSERT_MASK                  = 0x08         # Interrupt assert control
		self.RPR0521RS_INTERRUPT_INT_LATCH_MASK                   = 0x04         # Interrupt latch control
		self.RPR0521RS_INTERRUPT_INT_TRIG_MASK                    = 0x03         # Interrupt trigger control
		self.RPR0521RS_MANUFACT_ID_ID_MASK                        = 0xFF         