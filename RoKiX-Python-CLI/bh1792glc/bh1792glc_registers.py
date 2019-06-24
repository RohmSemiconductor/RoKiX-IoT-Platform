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
		self.BH1792GLC_REGISTER_DUMP_START                        = 0x0F         
		self.BH1792GLC_MANUFACTURER_ID                            = 0x0F         # Manufacturer ID : 0xE0
		self.BH1792GLC_PART_ID                                    = 0x10         # Part ID : 0x0E
		self.BH1792GLC_RESET                                      = 0x40         # Soft reset
		self.BH1792GLC_MEAS_CONTROL1                              = 0x41         # System control setting
		self.BH1792GLC_MEAS_CONTROL2                              = 0x42         # LED 1 & 2 control register
		self.BH1792GLC_MEAS_CONTROL3                              = 0x43         # LED 3 control register
		self.BH1792GLC_MEAS_CONTROL4_LSB                          = 0x44         # IR Interrupt Threshold Value (LSB)
		self.BH1792GLC_MEAS_CONTROL4_MSB                          = 0x45         # IR Interrupt Threshold Value (MSB)
		self.BH1792GLC_MEAS_CONTROL5                              = 0x46         # INT pin interrupt factor control register
		self.BH1792GLC_MEAS_START                                 = 0x47         # Measurement start register
		self.BH1792GLC_MEAS_SYNC                                  = 0x48         # Input measurement synchronization signal register
		self.BH1792GLC_FIFO_LEV                                   = 0x4B         # GDATA FIFO
		self.BH1792GLC_FIFODATA0_LSB                              = 0x4C         # FIFO Output Data 0 [7:0]
		self.BH1792GLC_FIFODATA0_MSB                              = 0x4D         # FIFO Output Data 0 [15:8]
		self.BH1792GLC_FIFODATA1_LSB                              = 0x4E         # FIFO Output Data 1 [7:0]
		self.BH1792GLC_FIFODATA1_MSB                              = 0x4F         # FIFO Output Data 1 [15:8]
		self.BH1792GLC_IRDATA_LEDOFF_LSB                          = 0x50         # IR Data Count Value during no LED emission [7:0]
		self.BH1792GLC_IRDATA_LEDOFF_MSB                          = 0x51         # IR Data Count Value during no LED emission [15:8]
		self.BH1792GLC_IRDATA_LEDON_LSB                           = 0x52         # IR Data Count Value during LED emission - IR Data Count Value during no LED emission [7:0]
		self.BH1792GLC_IRDATA_LEDON_MSB                           = 0x53         # IR Data Count Value during LED emission - IR Data Count Value during no LED emission [15:8]
		self.BH1792GLC_GDATA_LEDOFF_LSB                           = 0x54         # Green Data Count Value during no LED emission [7:0]
		self.BH1792GLC_GDATA_LEDOFF_MSB                           = 0x55         # Green Data Count Value during no LED emission [15:8]
		self.BH1792GLC_GDATA_LEDON_LSB                            = 0x56         # Green Data Count Value during LED emission [7:0]
		self.BH1792GLC_GDATA_LEDON_MSB                            = 0x57         # Green Data Count Value during LED emission [15:8]
		self.BH1792GLC_INT_CLEAR                                  = 0x58         # IR threshold judgement and measurement completion interrupt is cleared when reading this register.
		self.BH1792GLC_REGISTER_DUMP_END                          = 0x58         
class bits(register_base):
	def __init__(self):
		self.BH1792GLC_MANUFACTURER_ID_MANUFACTURER_ID_ID         = (0xE0 << 0)  # Manufacturer ID : 0xE0
		self.BH1792GLC_PART_ID_PART_ID_ID                         = (0x0E << 0)  # Part ID : 0x0E
		self.BH1792GLC_RESET_SWRESET                              = (0x01 << 7)  # 1 : Software reset is performed
		self.BH1792GLC_MEAS_CONTROL1_RDY                          = (0x01 << 7)  # 1 : OSC block is active, 0: prohibited
		self.BH1792GLC_MEAS_CONTROL1_SEL_ADC_GREEN                = (0x00 << 4)  # GREEN Measurement Mode. LED1 and LED2 drivers are active.
		self.BH1792GLC_MEAS_CONTROL1_SEL_ADC_IR                   = (0x01 << 4)  # IR Measurement Mode. LED3 driver is active. Only works in Non-Synchronized and Single Measurement modes.
		self.BH1792GLC_MEAS_CONTROL1_SEL_ADC                      = (0x01 << 4)  # Select LED omitting frequency
		self.BH1792GLC_MEAS_CONTROL1_MSR_32HZ                     = (0x00 << 0)  # 32 Hz synchronous mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_128HZ                    = (0x01 << 0)  # 128 Hz synchronous mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_64HZ                     = (0x02 << 0)  # 64 Hz synchronous mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_256HZ                    = (0x03 << 0)  # 256 Hz synchronous mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_PROHIBITED               = (0x04 << 0)  # Prohibited
		self.BH1792GLC_MEAS_CONTROL1_MSR_1024HZ                   = (0x05 << 0)  # 1024 Hz synchronous mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_NON_SYNCH_MODE           = (0x06 << 0)  # Non Synchronized Measurement Mode
		self.BH1792GLC_MEAS_CONTROL1_MSR_SINGLE_MEAS_MODE         = (0x07 << 0)  # Single Measurement Mode
		self.BH1792GLC_MEAS_CONTROL3_LED_EN2                      = (0x01 << 7)  # LED driver mode, for usage see datasheet
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL_DISABLE              = (0x00 << 0)  # No interrupt output.
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL_FIFO_WATERMARK       = (0x01 << 0)  # Watermark interrupt FIFO, fires when number of stored samples reaches 32. Cleared when number of samples falls below 32.
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL_IR_THRESHOLD         = (0x02 << 0)  # IR threshold judgement interrupt. Used only in Non Synchronized mode.
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL_ON_COMPLETE          = (0x03 << 0)  # Measurement completion interrupt. Used only in Single Measurement mode.
		self.BH1792GLC_MEAS_START_MEAS_ST                         = (0x01 << 0)  # Flag of start measurement. MEAS_ST=1 after RDY=1 starts measurement. In single measurement mode MEAS_ST=1 restarts measurement.
		self.BH1792GLC_MEAS_SYNC_MEAS_SYNC                        = (0x01 << 0)  # Input measurement synchronization signal. Write to 1 once every second.
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1792GLC_MEAS_CONTROL1_SEL_ADC={
			'IR':_b.BH1792GLC_MEAS_CONTROL1_SEL_ADC_IR,
			'GREEN':_b.BH1792GLC_MEAS_CONTROL1_SEL_ADC_GREEN,
		}
		self.BH1792GLC_MEAS_CONTROL1_MSR={
			'64HZ':_b.BH1792GLC_MEAS_CONTROL1_MSR_64HZ,
			'256HZ':_b.BH1792GLC_MEAS_CONTROL1_MSR_256HZ,
			'32HZ':_b.BH1792GLC_MEAS_CONTROL1_MSR_32HZ,
			'NON_SYNCH_MODE':_b.BH1792GLC_MEAS_CONTROL1_MSR_NON_SYNCH_MODE,
			'1024HZ':_b.BH1792GLC_MEAS_CONTROL1_MSR_1024HZ,
			'128HZ':_b.BH1792GLC_MEAS_CONTROL1_MSR_128HZ,
			'SINGLE_MEAS_MODE':_b.BH1792GLC_MEAS_CONTROL1_MSR_SINGLE_MEAS_MODE,
			'PROHIBITED':_b.BH1792GLC_MEAS_CONTROL1_MSR_PROHIBITED,
		}
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL={
			'ON_COMPLETE':_b.BH1792GLC_MEAS_CONTROL5_INT_SEL_ON_COMPLETE,
			'IR_THRESHOLD':_b.BH1792GLC_MEAS_CONTROL5_INT_SEL_IR_THRESHOLD,
			'DISABLE':_b.BH1792GLC_MEAS_CONTROL5_INT_SEL_DISABLE,
			'FIFO_WATERMARK':_b.BH1792GLC_MEAS_CONTROL5_INT_SEL_FIFO_WATERMARK,
		}
class masks(register_base):
	def __init__(self):
		self.BH1792GLC_MANUFACTURER_ID_MANUFACTURER_ID_MASK       = 0xFF         
		self.BH1792GLC_PART_ID_PART_ID_MASK                       = 0xFF         
		self.BH1792GLC_MEAS_CONTROL1_SEL_ADC_MASK                 = 0x10         # Select LED omitting frequency
		self.BH1792GLC_MEAS_CONTROL1_MSR_MASK                     = 0x07         # Select Measurement Mode
		self.BH1792GLC_MEAS_CONTROL2_LED_EN1_MASK                 = 0xC0         # LED driver mode, for usage see datasheet
		self.BH1792GLC_MEAS_CONTROL2_LED_CURRENT1_MASK            = 0x3F         # LED lighting current, 0 = stop, 1=1mA, , 0x3F = 63mA
		self.BH1792GLC_MEAS_CONTROL3_LED_CURRENT2_MASK            = 0x3F         # LED lighting current, 0 = stop, 1=1mA, , 0x3F = 63mA
		self.BH1792GLC_MEAS_CONTROL4_MSB_TH_IR_MASK               = 0xFF         # IR Interrupt Threshold Value [15:8]
		self.BH1792GLC_MEAS_CONTROL5_INT_SEL_MASK                 = 0x03         # Interrupt function select
		self.BH1792GLC_FIFO_LEV_FIFO_LEV_MASK                     = 0x3F         # Number of stored samples in FIFO; 0x00=FIFO empty, 0x23=FIFO full