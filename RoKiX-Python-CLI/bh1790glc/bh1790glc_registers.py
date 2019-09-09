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
		self.BH1790_REGISTER_DUMP_START                           = 0x0F         
		self.BH1790_MANUFACTURER_ID                               = 0x0F         
		self.BH1790_PART_ID                                       = 0x10         
		self.BH1790_RESET                                         = 0x40         # Soft reset
		self.BH1790_MEAS_CONTROL1                                 = 0x41         # System control setting
		self.BH1790_MEAS_CONTROL2                                 = 0x42         # Measurement control setting
		self.BH1790_MEAS_START                                    = 0x43         # Measurement start
		self.BH1790_DATAOUT_LEDOFF_L                              = 0x54         
		self.BH1790_DATAOUT_LEDOFF_H                              = 0x55         
		self.BH1790_DATAOUT_LEDON_L                               = 0x56         
		self.BH1790_DATAOUT_LEDON_H                               = 0x57         # Restarts measurement.
		self.BH1790_REGISTER_DUMP_END                             = 0x57         
class bits(register_base):
	def __init__(self):
		self.BH1790_PART_ID_WIA_ID                                = (0x0D << 0)  # WHO_AM_I -value
		self.BH1790_RESET_SWRESET                                 = (0x01 << 7)  # 1 : Software reset is performed
		self.BH1790_MEAS_CONTROL1_RDY_DISABLE                     = (0x00 << 7)  # OSC block is inactive
		self.BH1790_MEAS_CONTROL1_RDY_ENABLE                      = (0x01 << 7)  # OSC block is active
		self.BH1790_MEAS_CONTROL1_RDY                             = (0x01 << 7)  # 1 : OSC block is active
		self.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_128HZ         = (0x00 << 2)  
		self.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_64HZ          = (0x01 << 2)  
		self.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ               = (0x01 << 2)  # Select LED omitting frequency
		self.BH1790_MEAS_CONTROL1_RCYCLE_PROHIBITED1              = (0x00 << 0)  
		self.BH1790_MEAS_CONTROL1_RCYCLE_64HZ                     = (0x01 << 0)  
		self.BH1790_MEAS_CONTROL1_RCYCLE_32HZ                     = (0x02 << 0)  
		self.BH1790_MEAS_CONTROL1_RCYCLE_PROHIBITED2              = (0x03 << 0)  
		self.BH1790_MEAS_CONTROL2_LED2_EN_PULSED                  = (0x00 << 7)  
		self.BH1790_MEAS_CONTROL2_LED2_EN_CONSTANT                = (0x01 << 7)  
		self.BH1790_MEAS_CONTROL2_LED2_EN                         = (0x01 << 7)  # LED driver mode
		self.BH1790_MEAS_CONTROL2_LED1_EN_PULSED                  = (0x00 << 6)  
		self.BH1790_MEAS_CONTROL2_LED1_EN_CONSTANT                = (0x01 << 6)  
		self.BH1790_MEAS_CONTROL2_LED1_EN                         = (0x01 << 6)  # LED driver mode
		self.BH1790_MEAS_CONTROL2_LED_ON_TIME_216T_OSC            = (0x00 << 5)  # us
		self.BH1790_MEAS_CONTROL2_LED_ON_TIME_432T_OSC            = (0x01 << 5)  # us
		self.BH1790_MEAS_CONTROL2_LED_ON_TIME                     = (0x01 << 5)  # LED emitting time
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA                 = (0x00 << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA                 = (0x08 << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA                 = (0x09 << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA                 = (0x0A << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA                 = (0x0B << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA                = (0x0C << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA                = (0x0D << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA                = (0x0E << 0)  
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA                = (0x0F << 0)  
		self.BH1790_MEAS_START_MEAS_ST_STOP                       = (0x00 << 0)  
		self.BH1790_MEAS_START_MEAS_ST_START                      = (0x01 << 0)  
		self.BH1790_MEAS_START_MEAS_ST                            = (0x01 << 0)  # Flag of start measurement. (Write RDY=1 before this to start measurement)
_b=bits()
class enums(register_base):
	def __init__(self):
		self.BH1790_MEAS_CONTROL2_LED1_EN={
			'PULSED':_b.BH1790_MEAS_CONTROL2_LED1_EN_PULSED,
			'CONSTANT':_b.BH1790_MEAS_CONTROL2_LED1_EN_CONSTANT,
		}
		self.BH1790_MEAS_CONTROL2_LED_CURRENT={
			'30MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA,
			'10MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA,
			'6MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA,
			'1MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA,
			'2MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA,
			'60MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA,
			'0MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA,
			'20MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA,
			'3MA':_b.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA,
		}
		self.BH1790_MEAS_CONTROL1_RCYCLE={
			'PROHIBITED1':_b.BH1790_MEAS_CONTROL1_RCYCLE_PROHIBITED1,
			'64HZ':_b.BH1790_MEAS_CONTROL1_RCYCLE_64HZ,
			'PROHIBITED2':_b.BH1790_MEAS_CONTROL1_RCYCLE_PROHIBITED2,
			'32HZ':_b.BH1790_MEAS_CONTROL1_RCYCLE_32HZ,
		}
		self.BH1790_MEAS_CONTROL2_LED2_EN={
			'PULSED':_b.BH1790_MEAS_CONTROL2_LED2_EN_PULSED,
			'CONSTANT':_b.BH1790_MEAS_CONTROL2_LED2_EN_CONSTANT,
		}
		self.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ={
			'64HZ':_b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_64HZ,
			'128HZ':_b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_128HZ,
		}
		self.BH1790_MEAS_START_MEAS_ST={
			'START':_b.BH1790_MEAS_START_MEAS_ST_START,
			'STOP':_b.BH1790_MEAS_START_MEAS_ST_STOP,
		}
		self.BH1790_MEAS_CONTROL2_LED_ON_TIME={
			'216T_OSC':_b.BH1790_MEAS_CONTROL2_LED_ON_TIME_216T_OSC,
			'432T_OSC':_b.BH1790_MEAS_CONTROL2_LED_ON_TIME_432T_OSC,
		}
		self.BH1790_MEAS_CONTROL1_RDY={
			'DISABLE':_b.BH1790_MEAS_CONTROL1_RDY_DISABLE,
			'ENABLE':_b.BH1790_MEAS_CONTROL1_RDY_ENABLE,
		}
class masks(register_base):
	def __init__(self):
		self.BH1790_PART_ID_WIA_MASK                              = 0xFF         
		self.BH1790_MEAS_CONTROL1_RDY_MASK                        = 0x80         # 1 : OSC block is active
		self.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_MASK          = 0x04         # Select LED omitting frequency
		self.BH1790_MEAS_CONTROL1_RCYCLE_MASK                     = 0x03         # Select Data reading frequency
		self.BH1790_MEAS_CONTROL2_LED2_EN_MASK                    = 0x80         # LED driver mode
		self.BH1790_MEAS_CONTROL2_LED1_EN_MASK                    = 0x40         # LED driver mode
		self.BH1790_MEAS_CONTROL2_LED_ON_TIME_MASK                = 0x20         # LED emitting time
		self.BH1790_MEAS_CONTROL2_LED_CURRENT_MASK                = 0x0F         # LED lighting current
		self.BH1790_MEAS_START_MEAS_ST_MASK                       = 0x01         # Flag of start measurement. (Write RDY=1 before this to start measurement)
