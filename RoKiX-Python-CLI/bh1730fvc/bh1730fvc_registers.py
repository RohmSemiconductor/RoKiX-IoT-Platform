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
		self.BH1730FVC_REGISTER_DUMP_START                        = 0x80         
		self.BH1730FVC_CONTROL                                    = 0x80         # Operation mode control
		self.BH1730FVC_TIMING                                     = 0x81         # Light integration time control (ITIME)
		self.BH1730FVC_INTERRUPT                                  = 0x82         # Interrupt function control
		self.BH1730FVC_THLLOW                                     = 0x83         # Low byte of low interrupt threshold setting
		self.BH1730FVC_THLHIGH                                    = 0x84         # High byte of low interrupt threshold setting
		self.BH1730FVC_THHLOW                                     = 0x85         # Low byte of high interrupt threshold setting
		self.BH1730FVC_THHHIGH                                    = 0x86         # High byte of high interrupt threshold setting
		self.BH1730FVC_GAIN                                       = 0x87         # Gain control
		self.BH1730FVC_ID                                         = 0x92         # Part number and Revision ID
		self.BH1730FVC_DATA0LOW                                   = 0x94         # ADC Type0 low byte data register
		self.BH1730FVC_DATA0HIGH                                  = 0x95         # ADC Type0 high byte data register
		self.BH1730FVC_DATA1LOW                                   = 0x96         # ADC Type1 low byte data register
		self.BH1730FVC_DATA1HIGH                                  = 0x97         # ADC Type1 high byte data register
		self.BH1730FVC_INT_RESET                                  = 0xE1         # Reset interrupt
		self.BH1730FVC_RESET                                      = 0xE4         # Software reset
		self.BH1730FVC_REGISTER_DUMP_END                          = 0x97         
class bits(register_base):
	def __init__(self):
		self.BH1730FVC_CONTROL_ADC_INTR_INACTIVE                  = (0x00 << 5)  # Interrupt is inactive
		self.BH1730FVC_CONTROL_ADC_INTR_ACTIVE                    = (0x01 << 5)  # Interrupt is active
		self.BH1730FVC_CONTROL_ADC_INTR                           = (0x01 << 5)  # ADC interrupt status
		self.BH1730FVC_CONTROL_ADC_VALID                          = (0x01 << 4)  # ADC data updated flag
		self.BH1730FVC_CONTROL_ONE_TIME_CONTINOUS                 = (0x00 << 3)  # ADC measurement is continuous
		self.BH1730FVC_CONTROL_ONE_TIME_ONETIME                   = (0x01 << 3)  # ADC measurement is one time
		self.BH1730FVC_CONTROL_ONE_TIME                           = (0x01 << 3)  # ADC measurement mode
		self.BH1730FVC_CONTROL_DATA_SEL_TYPE0_AND_1               = (0x00 << 2)  # ADC measurement Type0 and Type1
		self.BH1730FVC_CONTROL_DATA_SEL_TYPE0                     = (0x01 << 2)  # ADC measurement Type0 only
		self.BH1730FVC_CONTROL_DATA_SEL                           = (0x01 << 2)  # ADC channel select
		self.BH1730FVC_CONTROL_ADC_EN_DISABLE                     = (0x00 << 1)  # ADC measurement stops
		self.BH1730FVC_CONTROL_ADC_EN_ENABLE                      = (0x01 << 1)  # ADC measurement starts
		self.BH1730FVC_CONTROL_ADC_EN                             = (0x01 << 1)  # ADC measurement enable
		self.BH1730FVC_CONTROL_POWER_DISABLE                      = (0x00 << 0)  # ADC power down
		self.BH1730FVC_CONTROL_POWER_ENABLE                       = (0x01 << 0)  # ADC power on
		self.BH1730FVC_CONTROL_POWER                              = (0x01 << 0)  # ADC power control
		self.BH1730FVC_INTERRUPT_INT_STOP_CONTINUOUS              = (0x00 << 6)  # ADC measurement does not stop
		self.BH1730FVC_INTERRUPT_INT_STOP_STOPPED                 = (0x01 << 6)  # ADC measurement stops when interrupt becomes active
		self.BH1730FVC_INTERRUPT_INT_STOP                         = (0x01 << 6)  # ADC stop on interrupt control
		self.BH1730FVC_INTERRUPT_INT_EN_INVALID                   = (0x00 << 4)  # Disable interrupt function
		self.BH1730FVC_INTERRUPT_INT_EN_VALID                     = (0x01 << 4)  # Enable interrupt function
		self.BH1730FVC_INTERRUPT_INT_EN                           = (0x01 << 4)  # Interrupt enable
		self.BH1730FVC_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT = (0x00 << 0)  # Interrupt becomes active at each measurement end
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT = (0x01 << 0)  # Interrrupt status is updated at each measurement end
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME      = (0x02 << 0)  # Interrupt status is updated if 2 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME      = (0x03 << 0)  # Interrupt status is updated if 3 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_4_SAME      = (0x04 << 0)  # Interrupt status is updated if 4 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_5_SAME      = (0x05 << 0)  # Interrupt status is updated if 5 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_6_SAME      = (0x06 << 0)  # Interrupt status is updated if 6 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_7_SAME      = (0x07 << 0)  # Interrupt status is updated if 7 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_8_SAME      = (0x08 << 0)  # Interrupt status is updated if 8 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_9_SAME      = (0x09 << 0)  # Interrupt status is updated if 9 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_10_SAME     = (0x0A << 0)  # Interrupt status is updated if 10 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_11_SAME     = (0x0B << 0)  # Interrupt status is updated if 11 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_12_SAME     = (0x0C << 0)  # Interrupt status is updated if 12 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_13_SAME     = (0x0D << 0)  # Interrupt status is updated if 13 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_14_SAME     = (0x0E << 0)  # Interrupt status is updated if 14 consecutive threshold judgments are the same
		self.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_15_SAME     = (0x0F << 0)  # Interrupt status is updated if 15 consecutive threshold judgments are the same
		self.BH1730FVC_GAIN_GAIN_X1_GAIN                          = (0x00 << 0)  # x1 gain mode
		self.BH1730FVC_GAIN_GAIN_X2_GAIN                          = (0x01 << 0)  # x2 gain mode
		self.BH1730FVC_GAIN_GAIN_X64_GAIN                         = (0x02 << 0)  # x64 gain mode
		self.BH1730FVC_GAIN_GAIN_X128_GAIN                        = (0x03 << 0)  # x128 gain mode
		self.BH1730FVC_ID_PART_NUMBER_ID                          = (0x07 << 4)  # Part number
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1730FVC_CONTROL_ADC_INTR={
			'INACTIVE':_b.BH1730FVC_CONTROL_ADC_INTR_INACTIVE,
			'ACTIVE':_b.BH1730FVC_CONTROL_ADC_INTR_ACTIVE,
		}
		self.BH1730FVC_CONTROL_ONE_TIME={
			'CONTINOUS':_b.BH1730FVC_CONTROL_ONE_TIME_CONTINOUS,
			'ONETIME':_b.BH1730FVC_CONTROL_ONE_TIME_ONETIME,
		}
		self.BH1730FVC_CONTROL_DATA_SEL={
			'TYPE0_AND_1':_b.BH1730FVC_CONTROL_DATA_SEL_TYPE0_AND_1,
			'TYPE0':_b.BH1730FVC_CONTROL_DATA_SEL_TYPE0,
		}
		self.BH1730FVC_CONTROL_ADC_EN={
			'DISABLE':_b.BH1730FVC_CONTROL_ADC_EN_DISABLE,
			'ENABLE':_b.BH1730FVC_CONTROL_ADC_EN_ENABLE,
		}
		self.BH1730FVC_CONTROL_POWER={
			'DISABLE':_b.BH1730FVC_CONTROL_POWER_DISABLE,
			'ENABLE':_b.BH1730FVC_CONTROL_POWER_ENABLE,
		}
		self.BH1730FVC_INTERRUPT_INT_STOP={
			'CONTINUOUS':_b.BH1730FVC_INTERRUPT_INT_STOP_CONTINUOUS,
			'STOPPED':_b.BH1730FVC_INTERRUPT_INT_STOP_STOPPED,
		}
		self.BH1730FVC_INTERRUPT_INT_EN={
			'INVALID':_b.BH1730FVC_INTERRUPT_INT_EN_INVALID,
			'VALID':_b.BH1730FVC_INTERRUPT_INT_EN_VALID,
		}
		self.BH1730FVC_INTERRUPT_PERSIST={
			'TOGGLE_AFTER_MEASUREMENT':_b.BH1730FVC_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,
			'UPDATE_AFTER_MEASUREMENT':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,
			'UPDATE_AFTER_2_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,
			'UPDATE_AFTER_3_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME,
			'UPDATE_AFTER_4_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_4_SAME,
			'UPDATE_AFTER_5_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_5_SAME,
			'UPDATE_AFTER_6_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_6_SAME,
			'UPDATE_AFTER_7_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_7_SAME,
			'UPDATE_AFTER_8_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_8_SAME,
			'UPDATE_AFTER_9_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_9_SAME,
			'UPDATE_AFTER_10_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_10_SAME,
			'UPDATE_AFTER_11_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_11_SAME,
			'UPDATE_AFTER_12_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_12_SAME,
			'UPDATE_AFTER_13_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_13_SAME,
			'UPDATE_AFTER_14_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_14_SAME,
			'UPDATE_AFTER_15_SAME':_b.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_15_SAME,
		}
		self.BH1730FVC_GAIN_GAIN={
			'X1_GAIN':_b.BH1730FVC_GAIN_GAIN_X1_GAIN,
			'X2_GAIN':_b.BH1730FVC_GAIN_GAIN_X2_GAIN,
			'X64_GAIN':_b.BH1730FVC_GAIN_GAIN_X64_GAIN,
			'X128_GAIN':_b.BH1730FVC_GAIN_GAIN_X128_GAIN,
		}
class masks(register_base):
	def __init__(self):
		self.BH1730FVC_CONTROL_ADC_INTR_MASK                      = 0x20         # ADC interrupt status
		self.BH1730FVC_CONTROL_ONE_TIME_MASK                      = 0x08         # ADC measurement mode
		self.BH1730FVC_CONTROL_DATA_SEL_MASK                      = 0x04         # ADC channel select
		self.BH1730FVC_CONTROL_ADC_EN_MASK                        = 0x02         # ADC measurement enable
		self.BH1730FVC_CONTROL_POWER_MASK                         = 0x01         # ADC power control
		self.BH1730FVC_INTERRUPT_INT_STOP_MASK                    = 0x40         # ADC stop on interrupt control
		self.BH1730FVC_INTERRUPT_INT_EN_MASK                      = 0x10         # Interrupt enable
		self.BH1730FVC_INTERRUPT_PERSIST_MASK                     = 0x0F         # Interrupt persistence function
		self.BH1730FVC_GAIN_GAIN_MASK                             = 0x07         # ADC resolution setting
		self.BH1730FVC_ID_PART_NUMBER_MASK                        = 0xF0         # Part number