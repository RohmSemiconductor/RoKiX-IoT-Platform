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
		self.BH1792_REGISTER_DUMP_START                           = 0x0F         
		self.BH1792_MANUFACTURER_REG                              = 0x0F         
		self.BH1792_PARTID_REG                                    = 0x10         # WHO_AM_I -value
		self.BH1792_RESET                                         = 0x40         # Soft reset
		self.BH1792_MEAS_CONTROL1                                 = 0x41         # System control setting
		self.BH1792_MEAS_CONTROL2                                 = 0x42         # LED 1 & 2 control register
		self.BH1792_MEAS_CONTROL3                                 = 0x43         # LED 3 control register
		self.BH1792_MEAS_CONTROL4_L                               = 0x44         # IR Interrupt Threshold Value [7:0]
		self.BH1792_MEAS_CONTROL4_H                               = 0x45         # IR Interrupt Threshold Value [15:8]
		self.BH1792_MEAS_CONTROL5                                 = 0x46         # Interrupt function select
		self.BH1792_MEAS_START                                    = 0x47         # Flag of start measurement. MEAS_ST=1 after RDY=1 starts measurement. In single measurement mode MEAS_ST=1 restarts measurement.
		self.BH1792_MEAS_SYNC                                     = 0x48         # Used in synhcronized measurement mode. Write once per second.
		self.BH1792_FIFO_LEV                                      = 0x4B         # Number of stored samples in FIFO, 0=FIFO empty, 0x23=FIFO full
		self.BH1792_FIFO_DATA0_L                                  = 0x4C         # FIFO Output data 0 [7:0]
		self.BH1792_FIFO_DATA0_H                                  = 0x4D         # FIFO Output data 0 [15:8]
		self.BH1792_FIFO_DATA1_L                                  = 0x4E         # FIFO Output data 1 [7:0]
		self.BH1792_FIFO_DATA1_H                                  = 0x4F         # FIFO Output data 1 [15:8]
		self.BH1792_IRDATA_LEDOFF_L                               = 0x50         # IR Data Count Value during no LED emission [7:0]
		self.BH1792_IRDATA_LEDOFF_H                               = 0x51         # IR Data Count Value during no LED emission [15:8]
		self.BH1792_IRDATA_LEDON_L                                = 0x52         # IR Data Count Value during LED emission [7:0]
		self.BH1792_IRDATA_LEDON_H                                = 0x53         # IR Data Count Value during LED emission [15:8]
		self.BH1792_DATAOUT_LEDOFF_L                              = 0x54         # Green Data Count Value during no LED emission [7:0]
		self.BH1792_DATAOUT_LEDOFF_H                              = 0x55         # Green Data Count Value during no LED emission [15:8]
		self.BH1792_DATAOUT_LEDON_L                               = 0x56         # Green Data Count Value during LED emission [7:0]
		self.BH1792_DATAOUT_LEDON_H                               = 0x57         # Green Data Count Value during LED emission [15:8]
		self.BH1792_INT_CLEAR                                     = 0x58         # IR threshold judgement and measurement completion interrupt is cleared when reading this register.
		self.BH1792_REGISTER_DUMP_END                             = 0x58         
class bits(register_base):
	def __init__(self):
		self.BH1792_MANUFACTURER_REG_MANUFACTURER_ID              = (0xE0 << 0)  
		self.BH1792_PARTID_REG_PART_ID                            = (0x0E << 0)  
		self.BH1792_RESET_SWRESET                                 = (0x01 << 7)  # 1 : Software reset is performed
		self.BH1792_MEAS_CONTROL1_RDY                             = (0x01 << 7)  # 1 : OSC block is active, 0: prohibited
		self.BH1792_MEAS_CONTROL1_SEL_ADC_GREEN                   = (0x00 << 4)  # Green mode, leds 1 & 2 active
		self.BH1792_MEAS_CONTROL1_SEL_ADC_IR                      = (0x01 << 4)  # IR mode, led 3 active. Can be used only in single and non synch modes.
		self.BH1792_MEAS_CONTROL1_SEL_ADC                         = (0x01 << 4)  # Select LED omitting frequency
		self.BH1792_MEAS_CONTROL1_MSR_32HZ                        = (0x00 << 0)  # 32 Hz synchronous mode
		self.BH1792_MEAS_CONTROL1_MSR_128HZ                       = (0x01 << 0)  # 128 Hz synchronous mode
		self.BH1792_MEAS_CONTROL1_MSR_64HZ                        = (0x02 << 0)  # 64 Hz synchronous mode
		self.BH1792_MEAS_CONTROL1_MSR_256HZ                       = (0x03 << 0)  # 256 Hz synchronous mode
		self.BH1792_MEAS_CONTROL1_MSR_PROHIBITED                  = (0x04 << 0)  
		self.BH1792_MEAS_CONTROL1_MSR_1024HZ                      = (0x05 << 0)  # 1024 Hz synchronous mode
		self.BH1792_MEAS_CONTROL1_MSR_NON_SYNCH_MODE              = (0x06 << 0)  # non synchronized measurement mode
		self.BH1792_MEAS_CONTROL1_MSR_SINGLE_MEAS_MODE            = (0x07 << 0)  # single measurement mode
		self.BH1792_MEAS_CONTROL3_LED_EN2                         = (0x01 << 7)  # LED driver mode, for usage see datasheet
		self.BH1792_MEAS_CONTROL5_INT_SEL_DISABLE                 = (0x00 << 0)  # No interrupt output.
		self.BH1792_MEAS_CONTROL5_INT_SEL_FIFO_WATERMARK          = (0x01 << 0)  # Watermark interrupt FIFO, fires when number of stored samples reaches 32. Cleared when number of samples falls below 32.
		self.BH1792_MEAS_CONTROL5_INT_SEL_IR_THRESHOLD            = (0x02 << 0)  # IR threshold judgement interrupt. Used in non synchroniozed mode.
		self.BH1792_MEAS_CONTROL5_INT_SEL_ON_COMPLETE             = (0x03 << 0)  # Measurement completion interrupt. In single mode.
		self.BH1792_MEAS_START_MEAS_ST                            = (0x01 << 0)  # Flag of start measurement. MEAS_ST=1 after RDY=1 starts measurement. In single measurement mode MEAS_ST=1 restarts measurement.
		self.BH1792_MEAS_SYNC_MEAS_SYNC                           = (0x01 << 0)  # Used in synhcronized measurement mode. Write once per second.
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1792_MEAS_CONTROL5_INT_SEL={
			'ON_COMPLETE':_b.BH1792_MEAS_CONTROL5_INT_SEL_ON_COMPLETE,
			'IR_THRESHOLD':_b.BH1792_MEAS_CONTROL5_INT_SEL_IR_THRESHOLD,
			'DISABLE':_b.BH1792_MEAS_CONTROL5_INT_SEL_DISABLE,
			'FIFO_WATERMARK':_b.BH1792_MEAS_CONTROL5_INT_SEL_FIFO_WATERMARK,
		}
		self.BH1792_MEAS_CONTROL1_MSR={
			'64HZ':_b.BH1792_MEAS_CONTROL1_MSR_64HZ,
			'256HZ':_b.BH1792_MEAS_CONTROL1_MSR_256HZ,
			'32HZ':_b.BH1792_MEAS_CONTROL1_MSR_32HZ,
			'NON_SYNCH_MODE':_b.BH1792_MEAS_CONTROL1_MSR_NON_SYNCH_MODE,
			'1024HZ':_b.BH1792_MEAS_CONTROL1_MSR_1024HZ,
			'128HZ':_b.BH1792_MEAS_CONTROL1_MSR_128HZ,
			'SINGLE_MEAS_MODE':_b.BH1792_MEAS_CONTROL1_MSR_SINGLE_MEAS_MODE,
			'PROHIBITED':_b.BH1792_MEAS_CONTROL1_MSR_PROHIBITED,
		}
		self.BH1792_MEAS_CONTROL1_SEL_ADC={
			'IR':_b.BH1792_MEAS_CONTROL1_SEL_ADC_IR,
			'GREEN':_b.BH1792_MEAS_CONTROL1_SEL_ADC_GREEN,
		}
class masks(register_base):
	def __init__(self):
		self.BH1792_MANUFACTURER_REG_MANUFACTURER_MASK            = 0xFF         
		self.BH1792_PARTID_REG_PART_MASK                          = 0xFF         
		self.BH1792_MEAS_CONTROL1_SEL_ADC_MASK                    = 0x10         # Select LED omitting frequency
		self.BH1792_MEAS_CONTROL1_MSR_MASK                        = 0x07         # Measurement mode
		self.BH1792_MEAS_CONTROL2_LED_EN1_MASK                    = 0xC0         # LED driver mode, for usage see datasheet
		self.BH1792_MEAS_CONTROL2_LED_CURRENT1_MASK               = 0x3F         # LED lighting current, 0 = stop, 1=1mA, , 0x3F = 63mA
		self.BH1792_MEAS_CONTROL3_LED_CURRENT2_MASK               = 0x3F         # LED lighting current, 0 = stop, 1=1mA, , 0x3F = 63mA
		self.BH1792_MEAS_CONTROL5_INT_SEL_MASK                    = 0x03         # Interrupt function select
		self.BH1792_FIFO_LEV_LEVEL_MASK                           = 0x3F         # Number of stored samples in FIFO, 0=FIFO empty, 0x23=FIFO full