# The MIT License (MIT)
#
# Copyright (c) 2018 Kionix Inc.
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
# Copyright (c) 2017 Kionix Inc.
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
		self.KMX64_WHO_AM_I                                       = 0x00         # This register can be used for supplier recognition, as it can be factory written to a known byte value.
		self.KMX64_INS1                                           = 0x01         # This Register tells which function caused an interrupt.
		self.KMX64_INS2                                           = 0x02         
		self.KMX64_INS3                                           = 0x03         
		self.KMX64_INL                                            = 0x05         
		self.KMX64_ACCEL_XOUT_L                                   = 0x0A         
		self.KMX64_ACCEL_XOUT_H                                   = 0x0B         
		self.KMX64_ACCEL_YOUT_L                                   = 0x0C         
		self.KMX64_ACCEL_YOUT_H                                   = 0x0D         
		self.KMX64_ACCEL_ZOUT_L                                   = 0x0E         
		self.KMX64_ACCEL_ZOUT_H                                   = 0x0F         
		self.KMX64_MAG_XOUT_L                                     = 0x10         
		self.KMX64_MAG_XOUT_H                                     = 0x11         
		self.KMX64_MAG_YOUT_L                                     = 0x12         
		self.KMX64_MAG_YOUT_H                                     = 0x13         
		self.KMX64_MAG_ZOUT_L                                     = 0x14         
		self.KMX64_MAG_ZOUT_H                                     = 0x15         
		self.KMX64_TEMP_OUT_L                                     = 0x16         
		self.KMX64_TEMP_OUT_H                                     = 0x17         
		self.KMX64_INC1                                           = 0x28         # This register controls routing of an interrupt reporting to physical interrupt pin GPIO1
		self.KMX64_INC2                                           = 0x29         # Interrupts reported on GPIO2.
		self.KMX64_INC3                                           = 0x2A         # Interrupt control 3 GPIO pin configuration.
		self.KMX64_INC4                                           = 0x2B         # This register controls which accelerometer axis and direction of detected motion can cause an interrupt.
		self.KMX64_INC5                                           = 0x2C         # This register controls which magnetometer axis and direction of detected motion can cause an interrupt.
		self.KMX64_AMI_CNTL1_L                                    = 0x2D         
		self.KMX64_AMI_CNTL1_H                                    = 0x2E         # threshold MSB
		self.KMX64_AMI_CNTL2                                      = 0x2F         # This register has control settings for the accelerometer motion interrupt function.
		self.KMX64_AMI_CNTL3                                      = 0x30         # Accelerometer Motion Control 3: This register has control settings for the accelerometer motion interrupt function.
		self.KMX64_MMI_CNTL1_L                                    = 0x31         
		self.KMX64_MMI_CNTL1_H                                    = 0x32         # threshold MSB
		self.KMX64_MMI_CNTL2                                      = 0x33         # Magnetometer Motion Control 2 This register has control settings for the magnetometer motion interrupt function.
		self.KMX64_MMI_CNTL3                                      = 0x34         # Magnetometer Motion Control 3 This register has control settings for the magnetometer motion interrupt function.
		self.KMX64_FFI_CNTL1                                      = 0x35         # This register has control settings for the free fall interrupt function
		self.KMX64_FFI_CNTL2                                      = 0x36         # This register has control settings for the free fall interrupt function
		self.KMX64_FFI_CNTL3                                      = 0x37         # This register has control settings for the free fall interrupt function
		self.KMX64_ODCNTL                                         = 0x38         # Output data control register
		self.KMX64_CNTL1                                          = 0x39         # Control register 1 Control register that controls the main feature set.
		self.KMX64_CNTL2                                          = 0x3A         # Control register 2 This is used to enable and disable the sensors.
		self.KMX64_COTR                                           = 0x3C         
		self.KMX64_BUF_CTRL_1                                     = 0x77         # These registers control the buffer sample buffer operation.
		self.KMX64_BUF_CTRL_2                                     = 0x78         # These registers control the buffer sample buffer operation.
		self.KMX64_BUF_CTRL_3                                     = 0x79         # These registers control the buffer sample buffer operation.
		self.KMX64_BUF_CLEAR                                      = 0x7A         # Latched buffer status information and the entire sample buffer are cleared when any data is written to this register.
		self.KMX64_BUF_STATUS_1                                   = 0x7B         # Sample Level; reports the number of data bytes that have been stored in the sample buffer.  If this register reads 0, no data has been stored in the buffer. If the buffer data is read past this level the part will return 32,767 (maximum value).
		self.KMX64_BUF_STATUS_2                                   = 0x7C         
		self.KMX64_BUF_STATUS_3                                   = 0x7D         # Sample over flow; reports the number of data bytes that have been missed since the sample buffer was filled.  If this register reads 0, the buffer has not over flowed. This is cleared for BUF_CLEAR command and when the data is read from BUF_READ
		self.KMX64_BUF_READ                                       = 0x7E         # Data in the buffer can be read according to the BUF_M settings in BUF_CTRL2 by executing this command.
		self.KMX64_DUMMY                                          = 0x7F         
class bits(register_base):
	def __init__(self):
		self.KMX64_WHO_AM_I_WAI_ID                                = (0x41 << 0)  # WHO_AM_I -value
		self.KMX64_INS1_INT_NO_INT                                = (0x00 << 7)  # no interrupt event
		self.KMX64_INS1_INT_INT                                   = (0x01 << 7)  # interrupt event has occurred
		self.KMX64_INS1_INT                                       = (0x01 << 7)  # reports the combined (OR) interrupt information of all enabled interrupt.
		self.KMX64_INS1_BFI_BUFF_NOT_FULL                         = (0x00 << 6)  # Buffer is not full
		self.KMX64_INS1_BFI_BUFF_FULL                             = (0x01 << 6)  # Buffer is full
		self.KMX64_INS1_BFI                                       = (0x01 << 6)  # indicates that the buffer is full.  This bit is cleared when the data is read until the buffer is not full.
		self.KMX64_INS1_WMI_MARK_NOT_REACHED                      = (0x00 << 5)  # Buffer watermark not reached
		self.KMX64_INS1_WMI_MARK_REACHED                          = (0x01 << 5)  # Buffer watermark reached
		self.KMX64_INS1_WMI                                       = (0x01 << 5)  # indicates that user-defined buffer watermark has been reached.  This bit is cleared when the data is read until the sample level in the buffer is smaller than the watermark threshold.
		self.KMX64_INS1_DRDY_A_NOT_AVAILABLE                      = (0x00 << 4)  # New acceleration data not available
		self.KMX64_INS1_DRDY_A_AVAILABLE                          = (0x01 << 4)  # New acceleration data available
		self.KMX64_INS1_DRDY_A                                    = (0x01 << 4)  # indicates that new acceleration data is available.  This bit is cleared when the data is read or the interrupt release register (INL Register) is read.
		self.KMX64_INS1_DRDY_M_NOT_AVAILABLE                      = (0x00 << 3)  # New magnetomter data not available
		self.KMX64_INS1_DRDY_M_AVAILABLE                          = (0x01 << 3)  # New magnetomter data available
		self.KMX64_INS1_DRDY_M                                    = (0x01 << 3)  # indicates that new magnetometer data is available.  This bit is cleared when the data is read or the interrupt release register (INL Register) is read.
		self.KMX64_INS1_FFI_NO_FFI                                = (0x00 << 2)  # No free fall
		self.KMX64_INS1_FFI_FFI                                   = (0x01 << 2)  # Free fall has activated the interrupt
		self.KMX64_INS1_FFI                                       = (0x01 << 2)  
		self.KMX64_INS1_AMI_NO_MOTION                             = (0x00 << 1)  # No motion
		self.KMX64_INS1_AMI_MOTION                                = (0x01 << 1)  # Motion has activated the interrupt
		self.KMX64_INS1_AMI                                       = (0x01 << 1)  
		self.KMX64_INS1_MMI_NO_MOTION                             = (0x00 << 0)  # No motion
		self.KMX64_INS1_MMI_MOTION                                = (0x01 << 0)  # Motion has activated the interrupt
		self.KMX64_INS1_MMI                                       = (0x01 << 0)  
		self.KMX64_INS2_AXNI                                      = (0x01 << 5)  # x negative (x-)
		self.KMX64_INS2_AXPI                                      = (0x01 << 4)  # x positive (x+)
		self.KMX64_INS2_AYNI                                      = (0x01 << 3)  # y negative (y-)
		self.KMX64_INS2_AYPI                                      = (0x01 << 2)  # y positive (y+)
		self.KMX64_INS2_AZNI                                      = (0x01 << 1)  # z negative (z-)
		self.KMX64_INS2_AZPI                                      = (0x01 << 0)  # z positive (z+)
		self.KMX64_INS3_MXNI                                      = (0x01 << 5)  # x negative (x-)
		self.KMX64_INS3_MXPI                                      = (0x01 << 4)  # x positive (x+)
		self.KMX64_INS3_MYNI                                      = (0x01 << 3)  # y negative (y-)
		self.KMX64_INS3_MYPI                                      = (0x01 << 2)  # y positive (y+)
		self.KMX64_INS3_MZNI                                      = (0x01 << 1)  # z negative (z-)
		self.KMX64_INS3_MZPI                                      = (0x01 << 0)  # z positive (z+)
		self.KMX64_INC1_SPI3E                                     = (0x01 << 7)  # 3 -wired SPI interface enable
		self.KMX64_INC1_BFI1                                      = (0x01 << 6)  # Buffer full interrupt reported on GPIO1
		self.KMX64_INC1_WMI1                                      = (0x01 << 5)  # Watermark interrupt reported on GPIO1
		self.KMX64_INC1_DRDY_A1                                   = (0x01 << 4)  # Accelerometer Data ready reported on GPIO1
		self.KMX64_INC1_DRDY_M1                                   = (0x01 << 3)  # Magnetometer Data ready reported on GPIO1
		self.KMX64_INC1_FFI1                                      = (0x01 << 2)  # Accelerometer Freefall interrupt reported on GPIO1
		self.KMX64_INC1_AMI1                                      = (0x01 << 1)  # Accelerometer motion interrupt reported on GPIO1
		self.KMX64_INC1_MMI1                                      = (0x01 << 0)  # Magnetometer motion interrupt reported on GPIO1
		self.KMX64_INC2_BFI2                                      = (0x01 << 6)  # Buffer full interrupt reported on GPIO2
		self.KMX64_INC2_WMI2                                      = (0x01 << 5)  # Watermark interrupt reported on GPIO2
		self.KMX64_INC2_DRDY_A2                                   = (0x01 << 4)  # Accelerometer Data ready reported on GPIO2
		self.KMX64_INC2_DRDY_M2                                   = (0x01 << 3)  # Magnetometer Data ready reported on GPIO2
		self.KMX64_INC2_FFI2                                      = (0x01 << 2)  # Accelerometer Freefall interrupt reported on GPIO2
		self.KMX64_INC2_AMI2                                      = (0x01 << 1)  # Accelerometer motion interrupt reported on GPIO2
		self.KMX64_INC2_MMI2                                      = (0x01 << 0)  # Magnetometer motion interrupt reported on GPIO2
		self.KMX64_INC3_IED2_PUSHPULL                             = (0x00 << 7)  # push-pull
		self.KMX64_INC3_IED2_OPENDRAIN                            = (0x01 << 7)  # open-drain
		self.KMX64_INC3_IED2                                      = (0x01 << 7)  # Interrupt pin drive options for GPIO2
		self.KMX64_INC3_IEA2_LOW                                  = (0x00 << 6)  # active low
		self.KMX64_INC3_IEA2_HIGH                                 = (0x01 << 6)  # active high
		self.KMX64_INC3_IEA2                                      = (0x01 << 6)  # Interrupt active level control for interrupt GPIO2
		self.KMX64_INC3_IEL2_LATCHED                              = (0x00 << 4)  # latched/unlatched. Unlatched feature is available for FFI,MME and AMI. AND DRDY
		self.KMX64_INC3_IEL2_PULSED                               = (0x01 << 4)  # pulsed.  In pulse mode the pulse width is 50us for normal mode and 10us for debug mode (high ODR rates).
		self.KMX64_INC3_IEL2_FIFO_TRIG                            = (0x02 << 4)  # trigger input for FIFO
		self.KMX64_INC3_IEL2_FIFO_TRIG_2                          = (0x03 << 4)  # trigger input for FIFO
		self.KMX64_INC3_IED1_PUSHPULL                             = (0x00 << 3)  # push-pull
		self.KMX64_INC3_IED1_OPENDRAIN                            = (0x01 << 3)  # open-drain
		self.KMX64_INC3_IED1                                      = (0x01 << 3)  # Interrupt pin drive options for GPIO1
		self.KMX64_INC3_IEA1_LOW                                  = (0x00 << 2)  # active low
		self.KMX64_INC3_IEA1_HIGH                                 = (0x01 << 2)  # active high
		self.KMX64_INC3_IEA1                                      = (0x01 << 2)  # Interrupt active level control for interrupt GPIO1
		self.KMX64_INC3_IEL1_LATCHED                              = (0x00 << 0)  # latched/unlatched. Unlatched feature is available for FFI,MME and AMI.
		self.KMX64_INC3_IEL1_PULSED                               = (0x01 << 0)  # pulsed.  In pulse mode the pulse width is 50us for normal mode and 10us for debug mode (high ODR rates).
		self.KMX64_INC3_IEL1_FIFO_TRIG                            = (0x02 << 0)  # trigger input for FIFO
		self.KMX64_INC3_IEL1_FIFO_TRIG_2                          = (0x03 << 0)  # trigger input for FIFO
		self.KMX64_INC4_AXNIE                                     = (0x01 << 5)  # x negative (x-) enable/disable
		self.KMX64_INC4_AXPIE                                     = (0x01 << 4)  # x positive (x+) enable/disable
		self.KMX64_INC4_AYNIE                                     = (0x01 << 3)  # y negative (y-) enable/disable
		self.KMX64_INC4_AYPIE                                     = (0x01 << 2)  # y positive (y+) enable/disable
		self.KMX64_INC4_AZNIE                                     = (0x01 << 1)  # z negative (z-) enable/disable
		self.KMX64_INC4_AZPIE                                     = (0x01 << 0)  # z positive (z+) enable/disable
		self.KMX64_INC5_MXNIE                                     = (0x01 << 5)  # x negative (x-) enable/disable
		self.KMX64_INC5_MXPIE                                     = (0x01 << 4)  # x positive (x+) enable/disable
		self.KMX64_INC5_MYNIE                                     = (0x01 << 3)  # y negative (y-) enable/disable
		self.KMX64_INC5_MYPIE                                     = (0x01 << 2)  # y positive (y+) enable/disable
		self.KMX64_INC5_MZNIE                                     = (0x01 << 1)  # z negative (z-) enable/disable
		self.KMX64_INC5_MZPIE                                     = (0x01 << 0)  # z positive (z+) enable/disable
		self.KMX64_AMI_CNTL3_AMI_EN_DISABLED                      = (0x00 << 7)  
		self.KMX64_AMI_CNTL3_AMI_EN_ENABLED                       = (0x01 << 7)  
		self.KMX64_AMI_CNTL3_AMI_EN                               = (0x01 << 7)  
		self.KMX64_AMI_CNTL3_AMIUL                                = (0x01 << 6)  
		self.KMX64_AMI_CNTL3_OAMI_0P781                           = (0x00 << 0)  # 0.781Hz
		self.KMX64_AMI_CNTL3_OAMI_1P563                           = (0x01 << 0)  # 1.563Hz
		self.KMX64_AMI_CNTL3_OAMI_3P125                           = (0x02 << 0)  # 3.125Hz
		self.KMX64_AMI_CNTL3_OAMI_6P25                            = (0x03 << 0)  # 6.25Hz
		self.KMX64_AMI_CNTL3_OAMI_12P5                            = (0x04 << 0)  # 12.5Hz
		self.KMX64_AMI_CNTL3_OAMI_25                              = (0x05 << 0)  # 25Hz
		self.KMX64_AMI_CNTL3_OAMI_50                              = (0x06 << 0)  # 50Hz
		self.KMX64_AMI_CNTL3_OAMI_100                             = (0x07 << 0)  # 100Hz
		self.KMX64_MMI_CNTL3_MMI_EN_DISABLED                      = (0x00 << 7)  
		self.KMX64_MMI_CNTL3_MMI_EN_ENABLED                       = (0x01 << 7)  
		self.KMX64_MMI_CNTL3_MMI_EN                               = (0x01 << 7)  
		self.KMX64_MMI_CNTL3_MMIUL                                = (0x01 << 6)  
		self.KMX64_MMI_CNTL3_OMMI_0P781                           = (0x00 << 0)  # 0.781Hz
		self.KMX64_MMI_CNTL3_OMMI_1P563                           = (0x01 << 0)  # 1.563Hz
		self.KMX64_MMI_CNTL3_OMMI_3P125                           = (0x02 << 0)  # 3.125Hz
		self.KMX64_MMI_CNTL3_OMMI_6P25                            = (0x03 << 0)  # 6.25Hz
		self.KMX64_MMI_CNTL3_OMMI_12P5                            = (0x04 << 0)  # 12.5Hz
		self.KMX64_MMI_CNTL3_OMMI_25                              = (0x05 << 0)  # 25Hz
		self.KMX64_MMI_CNTL3_OMMI_50                              = (0x06 << 0)  # 50Hz
		self.KMX64_MMI_CNTL3_OMMI_100                             = (0x07 << 0)  # 100Hz
		self.KMX64_FFI_CNTL3_FFI_EN_DISABLED                      = (0x00 << 7)  
		self.KMX64_FFI_CNTL3_FFI_EN_ENABLED                       = (0x01 << 7)  
		self.KMX64_FFI_CNTL3_FFI_EN                               = (0x01 << 7)  
		self.KMX64_FFI_CNTL3_FFIUL                                = (0x01 << 6)  
		self.KMX64_FFI_CNTL3_DCRM                                 = (0x01 << 3)  
		self.KMX64_FFI_CNTL3_OFFI_12P5                            = (0x00 << 0)  # 12.5Hz
		self.KMX64_FFI_CNTL3_OFFI_25                              = (0x01 << 0)  # 25Hz
		self.KMX64_FFI_CNTL3_OFFI_50                              = (0x02 << 0)  # 50Hz
		self.KMX64_FFI_CNTL3_OFFI_100                             = (0x03 << 0)  # 100Hz
		self.KMX64_FFI_CNTL3_OFFI_200                             = (0x04 << 0)  # 200Hz
		self.KMX64_FFI_CNTL3_OFFI_400                             = (0x05 << 0)  # 400Hz
		self.KMX64_FFI_CNTL3_OFFI_800                             = (0x06 << 0)  # 800Hz
		self.KMX64_FFI_CNTL3_OFFI_1600                            = (0x07 << 0)  # 1600Hz
		self.KMX64_ODCNTL_OSM_12P5                                = (0x00 << 4)  # 12.5Hz
		self.KMX64_ODCNTL_OSM_25                                  = (0x01 << 4)  # 25Hz
		self.KMX64_ODCNTL_OSM_50                                  = (0x02 << 4)  # 50Hz
		self.KMX64_ODCNTL_OSM_100                                 = (0x03 << 4)  # 100Hz
		self.KMX64_ODCNTL_OSM_200                                 = (0x04 << 4)  # 200Hz
		self.KMX64_ODCNTL_OSM_400                                 = (0x05 << 4)  # 400Hz
		self.KMX64_ODCNTL_OSM_800                                 = (0x06 << 4)  # 800Hz
		self.KMX64_ODCNTL_OSM_1600                                = (0x07 << 4)  # 1600Hz
		self.KMX64_ODCNTL_OSM_0P781                               = (0x08 << 4)  # 0.781Hz
		self.KMX64_ODCNTL_OSM_1P563                               = (0x09 << 4)  # 1.563Hz
		self.KMX64_ODCNTL_OSM_3P125                               = (0x0A << 4)  # 3.125Hz
		self.KMX64_ODCNTL_OSM_6P25                                = (0x0B << 4)  # 6.25Hz
		self.KMX64_ODCNTL_OSM_12800                               = (0x0F << 4)  # 12.8kHz
		self.KMX64_ODCNTL_OSA_12P5                                = (0x00 << 0)  # 12.5Hz
		self.KMX64_ODCNTL_OSA_25                                  = (0x01 << 0)  # 25Hz
		self.KMX64_ODCNTL_OSA_50                                  = (0x02 << 0)  # 50Hz
		self.KMX64_ODCNTL_OSA_100                                 = (0x03 << 0)  # 100Hz
		self.KMX64_ODCNTL_OSA_200                                 = (0x04 << 0)  # 200Hz
		self.KMX64_ODCNTL_OSA_400                                 = (0x05 << 0)  # 400Hz
		self.KMX64_ODCNTL_OSA_800                                 = (0x06 << 0)  # 800Hz
		self.KMX64_ODCNTL_OSA_1600                                = (0x07 << 0)  # 1600Hz
		self.KMX64_ODCNTL_OSA_0P781                               = (0x08 << 0)  # 0.781Hz
		self.KMX64_ODCNTL_OSA_1P563                               = (0x09 << 0)  # 1.563Hz
		self.KMX64_ODCNTL_OSA_3P125                               = (0x0A << 0)  # 3.125Hz
		self.KMX64_ODCNTL_OSA_6P25                                = (0x0B << 0)  # 6.25Hz
		self.KMX64_ODCNTL_OSA_25600                               = (0x0F << 0)  # 25.6kHz
		self.KMX64_CNTL1_SRST                                     = (0x01 << 7)  # Start POR routine
		self.KMX64_CNTL1_STEN_DISABLED                            = (0x00 << 6)  
		self.KMX64_CNTL1_STEN_ENABLED                             = (0x01 << 6)  
		self.KMX64_CNTL1_STEN                                     = (0x01 << 6)  # This bit enables the self-test mode that will produce a change in both the accelerometer and magnetometer transducers and can be measured in the output registers
		self.KMX64_CNTL1_STPOL                                    = (0x01 << 5)  # Accelerometer and Magnetometer ST polarity.
		self.KMX64_CNTL1_COTC                                     = (0x01 << 3)  # enables the command test function
		self.KMX64_CNTL1_MFSSEL_800UT                             = (0x02 << 0)  # 800uT
		self.KMX64_CNTL1_MFSSEL_1200UT                            = (0x03 << 0)  # 1200uT
		self.KMX64_CNTL2_TEMP_EN_STANDBY_MODE                     = (0x00 << 6)  # standby mode
		self.KMX64_CNTL2_TEMP_EN_OPERATING_MODE                   = (0x01 << 6)  # operating mode, magnetometer and temperature output registers are updated at the selected output data rate
		self.KMX64_CNTL2_TEMP_EN                                  = (0x01 << 6)  # controls the operating mode of the ASIC_AOs temperature sensors. MAG_EN must also be enabled for temperature data to be converted. Output data rate is locked to the magnetometers OSM.
		self.KMX64_CNTL2_GSEL_2G                                  = (0x00 << 4)  
		self.KMX64_CNTL2_GSEL_4G                                  = (0x01 << 4)  
		self.KMX64_CNTL2_GSEL_8G                                  = (0x02 << 4)  
		self.KMX64_CNTL2_GSEL_16G                                 = (0x03 << 4)  
		self.KMX64_CNTL2_RES_A4M2                                 = (0x00 << 2)  
		self.KMX64_CNTL2_RES_A32M16                               = (0x01 << 2)  
		self.KMX64_CNTL2_RES_MAX1                                 = (0x02 << 2)  
		self.KMX64_CNTL2_RES_MAX2                                 = (0x03 << 2)  
		self.KMX64_CNTL2_MAG_EN_STANDBY_MODE                      = (0x00 << 1)  
		self.KMX64_CNTL2_MAG_EN_OPERATING_MODE                    = (0x01 << 1)  
		self.KMX64_CNTL2_MAG_EN                                   = (0x01 << 1)  # controls the operating mode of the magnetometer sensor
		self.KMX64_CNTL2_ACCEL_EN_STANDBY_MODE                    = (0x00 << 0)  # controls the operating mode of the accelerometer sensor
		self.KMX64_CNTL2_ACCEL_EN_OPERATING_MODE                  = (0x01 << 0)  
		self.KMX64_CNTL2_ACCEL_EN                                 = (0x01 << 0)  
		self.KMX64_COTR_TEST_RESP_DEFAULT                         = (0x55 << 0)  
		self.KMX64_COTR_TEST_RESP_TEST                            = (0xAA << 0)  
		self.KMX64_BUF_CTRL_2_BUF_M_FIFO                          = (0x00 << 1)  # The buffer collects 384 bytes of data until full, collecting new data only when the buffer is not full.
		self.KMX64_BUF_CTRL_2_BUF_M_STREAM                        = (0x01 << 1)  # The buffer holds the last 384 bytes of data.  Once the buffer is full, the oldest data is discarded to make room for newer data.
		self.KMX64_BUF_CTRL_2_BUF_M_TRIGGER                       = (0x02 << 1)  # When a trigger event occurs (logic high input on TRIG pin), the buffer holds the last data set of SMP[6:0] samples before the trigger event and then continues to collect data until full.  New data is collected only when the buffer is not full.
		self.KMX64_BUF_CTRL_2_BUF_M_FILO                          = (0x03 << 1)  # The buffer holds the last 384 bytes of data.  Once the buffer is full, the oldest data is discarded to make room for newer data.  Reading from the buffer in this mode will return the most recent data first.
		self.KMX64_BUF_CTRL_2_SMT_TH8                             = (0x01 << 0)  # 8th bit of smt_th data
		self.KMX64_BUF_CTRL_3_BFI_EN_DISABLED                     = (0x00 << 7)  
		self.KMX64_BUF_CTRL_3_BFI_EN_ENABLED                      = (0x01 << 7)  
		self.KMX64_BUF_CTRL_3_BFI_EN                              = (0x01 << 7)  # controls the buffer full interrupt
		self.KMX64_BUF_CTRL_3_BUF_AX_DISABLED                     = (0x00 << 6)  
		self.KMX64_BUF_CTRL_3_BUF_AX_ENABLED                      = (0x01 << 6)  
		self.KMX64_BUF_CTRL_3_BUF_AX                              = (0x01 << 6)  # ax to be buffered
		self.KMX64_BUF_CTRL_3_BUF_AY_DISABLED                     = (0x00 << 5)  
		self.KMX64_BUF_CTRL_3_BUF_AY_ENABLED                      = (0x01 << 5)  
		self.KMX64_BUF_CTRL_3_BUF_AY                              = (0x01 << 5)  # ay to be buffered
		self.KMX64_BUF_CTRL_3_BUF_AZ_DISABLED                     = (0x00 << 4)  
		self.KMX64_BUF_CTRL_3_BUF_AZ_ENABLED                      = (0x01 << 4)  
		self.KMX64_BUF_CTRL_3_BUF_AZ                              = (0x01 << 4)  # az to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MX_DISABLED                     = (0x00 << 3)  
		self.KMX64_BUF_CTRL_3_BUF_MX_ENABLED                      = (0x01 << 3)  
		self.KMX64_BUF_CTRL_3_BUF_MX                              = (0x01 << 3)  # mx to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MY_DISABLED                     = (0x00 << 2)  
		self.KMX64_BUF_CTRL_3_BUF_MY_ENABLED                      = (0x01 << 2)  
		self.KMX64_BUF_CTRL_3_BUF_MY                              = (0x01 << 2)  # my to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MZ_DISABLED                     = (0x00 << 1)  
		self.KMX64_BUF_CTRL_3_BUF_MZ_ENABLED                      = (0x01 << 1)  
		self.KMX64_BUF_CTRL_3_BUF_MZ                              = (0x01 << 1)  # mz to be buffered
		self.KMX64_BUF_CTRL_3_BUF_TEMP_DISABLED                   = (0x00 << 0)  
		self.KMX64_BUF_CTRL_3_BUF_TEMP_ENABLED                    = (0x01 << 0)  
		self.KMX64_BUF_CTRL_3_BUF_TEMP                            = (0x01 << 0)  # temperature to be buffered
		self.KMX64_BUF_STATUS_2_BUF_TRIG                          = (0x01 << 2)  # reports the status of the buffers trigger function if this mode has been selected.  When using trigger mode, a buffer read should only be performed after a trigger event.
_b=bits()
class enums(register_base):
	def __init__(self):
		self.KMX64_INS1_INT={
			'NO_INT':_b.KMX64_INS1_INT_NO_INT,
			'INT':_b.KMX64_INS1_INT_INT,
		}
		self.KMX64_INS1_BFI={
			'BUFF_NOT_FULL':_b.KMX64_INS1_BFI_BUFF_NOT_FULL,
			'BUFF_FULL':_b.KMX64_INS1_BFI_BUFF_FULL,
		}
		self.KMX64_INS1_WMI={
			'MARK_NOT_REACHED':_b.KMX64_INS1_WMI_MARK_NOT_REACHED,
			'MARK_REACHED':_b.KMX64_INS1_WMI_MARK_REACHED,
		}
		self.KMX64_INS1_DRDY_A={
			'NOT_AVAILABLE':_b.KMX64_INS1_DRDY_A_NOT_AVAILABLE,
			'AVAILABLE':_b.KMX64_INS1_DRDY_A_AVAILABLE,
		}
		self.KMX64_INS1_DRDY_M={
			'NOT_AVAILABLE':_b.KMX64_INS1_DRDY_M_NOT_AVAILABLE,
			'AVAILABLE':_b.KMX64_INS1_DRDY_M_AVAILABLE,
		}
		self.KMX64_INS1_FFI={
			'NO_FFI':_b.KMX64_INS1_FFI_NO_FFI,
			'FFI':_b.KMX64_INS1_FFI_FFI,
		}
		self.KMX64_INS1_AMI={
			'NO_MOTION':_b.KMX64_INS1_AMI_NO_MOTION,
			'MOTION':_b.KMX64_INS1_AMI_MOTION,
		}
		self.KMX64_INS1_MMI={
			'NO_MOTION':_b.KMX64_INS1_MMI_NO_MOTION,
			'MOTION':_b.KMX64_INS1_MMI_MOTION,
		}
		self.KMX64_INC3_IED2={
			'PUSHPULL':_b.KMX64_INC3_IED2_PUSHPULL,
			'OPENDRAIN':_b.KMX64_INC3_IED2_OPENDRAIN,
		}
		self.KMX64_INC3_IEA2={
			'LOW':_b.KMX64_INC3_IEA2_LOW,
			'HIGH':_b.KMX64_INC3_IEA2_HIGH,
		}
		self.KMX64_INC3_IEL2={
			'LATCHED':_b.KMX64_INC3_IEL2_LATCHED,
			'PULSED':_b.KMX64_INC3_IEL2_PULSED,
			'FIFO_TRIG':_b.KMX64_INC3_IEL2_FIFO_TRIG,
			'FIFO_TRIG_2':_b.KMX64_INC3_IEL2_FIFO_TRIG_2,
		}
		self.KMX64_INC3_IED1={
			'PUSHPULL':_b.KMX64_INC3_IED1_PUSHPULL,
			'OPENDRAIN':_b.KMX64_INC3_IED1_OPENDRAIN,
		}
		self.KMX64_INC3_IEA1={
			'LOW':_b.KMX64_INC3_IEA1_LOW,
			'HIGH':_b.KMX64_INC3_IEA1_HIGH,
		}
		self.KMX64_INC3_IEL1={
			'LATCHED':_b.KMX64_INC3_IEL1_LATCHED,
			'PULSED':_b.KMX64_INC3_IEL1_PULSED,
			'FIFO_TRIG':_b.KMX64_INC3_IEL1_FIFO_TRIG,
			'FIFO_TRIG_2':_b.KMX64_INC3_IEL1_FIFO_TRIG_2,
		}
		self.KMX64_AMI_CNTL3_AMI_EN={
			'DISABLED':_b.KMX64_AMI_CNTL3_AMI_EN_DISABLED,
			'ENABLED':_b.KMX64_AMI_CNTL3_AMI_EN_ENABLED,
		}
		self.KMX64_AMI_CNTL3_OAMI={
			'0P781':_b.KMX64_AMI_CNTL3_OAMI_0P781,
			'1P563':_b.KMX64_AMI_CNTL3_OAMI_1P563,
			'3P125':_b.KMX64_AMI_CNTL3_OAMI_3P125,
			'6P25':_b.KMX64_AMI_CNTL3_OAMI_6P25,
			'12P5':_b.KMX64_AMI_CNTL3_OAMI_12P5,
			'25':_b.KMX64_AMI_CNTL3_OAMI_25,
			'50':_b.KMX64_AMI_CNTL3_OAMI_50,
			'100':_b.KMX64_AMI_CNTL3_OAMI_100,
		}
		self.KMX64_MMI_CNTL3_MMI_EN={
			'DISABLED':_b.KMX64_MMI_CNTL3_MMI_EN_DISABLED,
			'ENABLED':_b.KMX64_MMI_CNTL3_MMI_EN_ENABLED,
		}
		self.KMX64_MMI_CNTL3_OMMI={
			'0P781':_b.KMX64_MMI_CNTL3_OMMI_0P781,
			'1P563':_b.KMX64_MMI_CNTL3_OMMI_1P563,
			'3P125':_b.KMX64_MMI_CNTL3_OMMI_3P125,
			'6P25':_b.KMX64_MMI_CNTL3_OMMI_6P25,
			'12P5':_b.KMX64_MMI_CNTL3_OMMI_12P5,
			'25':_b.KMX64_MMI_CNTL3_OMMI_25,
			'50':_b.KMX64_MMI_CNTL3_OMMI_50,
			'100':_b.KMX64_MMI_CNTL3_OMMI_100,
		}
		self.KMX64_FFI_CNTL3_FFI_EN={
			'DISABLED':_b.KMX64_FFI_CNTL3_FFI_EN_DISABLED,
			'ENABLED':_b.KMX64_FFI_CNTL3_FFI_EN_ENABLED,
		}
		self.KMX64_FFI_CNTL3_OFFI={
			'12P5':_b.KMX64_FFI_CNTL3_OFFI_12P5,
			'25':_b.KMX64_FFI_CNTL3_OFFI_25,
			'50':_b.KMX64_FFI_CNTL3_OFFI_50,
			'100':_b.KMX64_FFI_CNTL3_OFFI_100,
			'200':_b.KMX64_FFI_CNTL3_OFFI_200,
			'400':_b.KMX64_FFI_CNTL3_OFFI_400,
			'800':_b.KMX64_FFI_CNTL3_OFFI_800,
			'1600':_b.KMX64_FFI_CNTL3_OFFI_1600,
		}
		self.KMX64_ODCNTL_OSM={
			'12P5':_b.KMX64_ODCNTL_OSM_12P5,
			'25':_b.KMX64_ODCNTL_OSM_25,
			'50':_b.KMX64_ODCNTL_OSM_50,
			'100':_b.KMX64_ODCNTL_OSM_100,
			'200':_b.KMX64_ODCNTL_OSM_200,
			'400':_b.KMX64_ODCNTL_OSM_400,
			'800':_b.KMX64_ODCNTL_OSM_800,
			'1600':_b.KMX64_ODCNTL_OSM_1600,
			'0P781':_b.KMX64_ODCNTL_OSM_0P781,
			'1P563':_b.KMX64_ODCNTL_OSM_1P563,
			'3P125':_b.KMX64_ODCNTL_OSM_3P125,
			'6P25':_b.KMX64_ODCNTL_OSM_6P25,
			'12800':_b.KMX64_ODCNTL_OSM_12800,
		}
		self.KMX64_ODCNTL_OSA={
			'12P5':_b.KMX64_ODCNTL_OSA_12P5,
			'25':_b.KMX64_ODCNTL_OSA_25,
			'50':_b.KMX64_ODCNTL_OSA_50,
			'100':_b.KMX64_ODCNTL_OSA_100,
			'200':_b.KMX64_ODCNTL_OSA_200,
			'400':_b.KMX64_ODCNTL_OSA_400,
			'800':_b.KMX64_ODCNTL_OSA_800,
			'1600':_b.KMX64_ODCNTL_OSA_1600,
			'0P781':_b.KMX64_ODCNTL_OSA_0P781,
			'1P563':_b.KMX64_ODCNTL_OSA_1P563,
			'3P125':_b.KMX64_ODCNTL_OSA_3P125,
			'6P25':_b.KMX64_ODCNTL_OSA_6P25,
			'25600':_b.KMX64_ODCNTL_OSA_25600,
		}
		self.KMX64_CNTL1_STEN={
			'DISABLED':_b.KMX64_CNTL1_STEN_DISABLED,
			'ENABLED':_b.KMX64_CNTL1_STEN_ENABLED,
		}
		self.KMX64_CNTL1_MFSSEL={
			'800UT':_b.KMX64_CNTL1_MFSSEL_800UT,
			'1200UT':_b.KMX64_CNTL1_MFSSEL_1200UT,
		}
		self.KMX64_CNTL2_TEMP_EN={
			'STANDBY_MODE':_b.KMX64_CNTL2_TEMP_EN_STANDBY_MODE,
			'OPERATING_MODE':_b.KMX64_CNTL2_TEMP_EN_OPERATING_MODE,
		}
		self.KMX64_CNTL2_GSEL={
			'2G':_b.KMX64_CNTL2_GSEL_2G,
			'4G':_b.KMX64_CNTL2_GSEL_4G,
			'8G':_b.KMX64_CNTL2_GSEL_8G,
			'16G':_b.KMX64_CNTL2_GSEL_16G,
		}
		self.KMX64_CNTL2_RES={
			'A4M2':_b.KMX64_CNTL2_RES_A4M2,
			'A32M16':_b.KMX64_CNTL2_RES_A32M16,
			'MAX1':_b.KMX64_CNTL2_RES_MAX1,
			'MAX2':_b.KMX64_CNTL2_RES_MAX2,
		}
		self.KMX64_CNTL2_MAG_EN={
			'STANDBY_MODE':_b.KMX64_CNTL2_MAG_EN_STANDBY_MODE,
			'OPERATING_MODE':_b.KMX64_CNTL2_MAG_EN_OPERATING_MODE,
		}
		self.KMX64_CNTL2_ACCEL_EN={
			'STANDBY_MODE':_b.KMX64_CNTL2_ACCEL_EN_STANDBY_MODE,
			'OPERATING_MODE':_b.KMX64_CNTL2_ACCEL_EN_OPERATING_MODE,
		}
		self.KMX64_COTR_TEST_RESP={
			'DEFAULT':_b.KMX64_COTR_TEST_RESP_DEFAULT,
			'TEST':_b.KMX64_COTR_TEST_RESP_TEST,
		}
		self.KMX64_BUF_CTRL_2_BUF_M={
			'FIFO':_b.KMX64_BUF_CTRL_2_BUF_M_FIFO,
			'STREAM':_b.KMX64_BUF_CTRL_2_BUF_M_STREAM,
			'TRIGGER':_b.KMX64_BUF_CTRL_2_BUF_M_TRIGGER,
			'FILO':_b.KMX64_BUF_CTRL_2_BUF_M_FILO,
		}
		self.KMX64_BUF_CTRL_3_BFI_EN={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BFI_EN_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BFI_EN_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_AX={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_AX_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_AX_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_AY={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_AY_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_AY_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_AZ={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_AZ_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_AZ_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_MX={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_MX_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_MX_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_MY={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_MY_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_MY_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_MZ={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_MZ_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_MZ_ENABLED,
		}
		self.KMX64_BUF_CTRL_3_BUF_TEMP={
			'DISABLED':_b.KMX64_BUF_CTRL_3_BUF_TEMP_DISABLED,
			'ENABLED':_b.KMX64_BUF_CTRL_3_BUF_TEMP_ENABLED,
		}
class masks(register_base):
	def __init__(self):
		self.KMX64_WHO_AM_I_WAI_MASK                              = 0xFF         
		self.KMX64_INS1_INT_MASK                                  = 0x80         # reports the combined (OR) interrupt information of all enabled interrupt.
		self.KMX64_INS1_BFI_MASK                                  = 0x40         # indicates that the buffer is full.  This bit is cleared when the data is read until the buffer is not full.
		self.KMX64_INS1_WMI_MASK                                  = 0x20         # indicates that user-defined buffer watermark has been reached.  This bit is cleared when the data is read until the sample level in the buffer is smaller than the watermark threshold.
		self.KMX64_INS1_DRDY_A_MASK                               = 0x10         # indicates that new acceleration data is available.  This bit is cleared when the data is read or the interrupt release register (INL Register) is read.
		self.KMX64_INS1_DRDY_M_MASK                               = 0x08         # indicates that new magnetometer data is available.  This bit is cleared when the data is read or the interrupt release register (INL Register) is read.
		self.KMX64_INS1_FFI_MASK                                  = 0x04         
		self.KMX64_INS1_AMI_MASK                                  = 0x02         
		self.KMX64_INS1_MMI_MASK                                  = 0x01         
		self.KMX64_INC3_IED2_MASK                                 = 0x80         # Interrupt pin drive options for GPIO2
		self.KMX64_INC3_IEA2_MASK                                 = 0x40         # Interrupt active level control for interrupt GPIO2
		self.KMX64_INC3_IEL2_MASK                                 = 0x30         # Interrupt latch control for interrupt GPIO2
		self.KMX64_INC3_IED1_MASK                                 = 0x08         # Interrupt pin drive options for GPIO1
		self.KMX64_INC3_IEA1_MASK                                 = 0x04         # Interrupt active level control for interrupt GPIO1
		self.KMX64_INC3_IEL1_MASK                                 = 0x03         # Interrupt latch control for interrupt GPIO1
		self.KMX64_AMI_CNTL1_H_AMITH_H_MASK                       = 0xFF         # threshold MSB
		self.KMX64_AMI_CNTL3_AMI_EN_MASK                          = 0x80         
		self.KMX64_AMI_CNTL3_OAMI_MASK                            = 0x07         
		self.KMX64_MMI_CNTL1_H_MMITH_H_MASK                       = 0xFF         # threshold MSB
		self.KMX64_MMI_CNTL3_MMI_EN_MASK                          = 0x80         
		self.KMX64_MMI_CNTL3_OMMI_MASK                            = 0x07         
		self.KMX64_FFI_CNTL3_FFI_EN_MASK                          = 0x80         
		self.KMX64_FFI_CNTL3_OFFI_MASK                            = 0x07         
		self.KMX64_ODCNTL_OSM_MASK                                = 0xF0         
		self.KMX64_ODCNTL_OSA_MASK                                = 0x0F         
		self.KMX64_CNTL1_STEN_MASK                                = 0x40         # This bit enables the self-test mode that will produce a change in both the accelerometer and magnetometer transducers and can be measured in the output registers
		self.KMX64_CNTL1_MFSSEL_MASK                              = 0x03         # Selects the magnetometer full scale range
		self.KMX64_CNTL2_TEMP_EN_MASK                             = 0x40         # controls the operating mode of the ASIC_AOs temperature sensors. MAG_EN must also be enabled for temperature data to be converted. Output data rate is locked to the magnetometers OSM.
		self.KMX64_CNTL2_GSEL_MASK                                = 0x30         # selects the acceleration range of the accelerometer outputs
		self.KMX64_CNTL2_RES_MASK                                 = 0x0C         # selects the resolution of both sensors.
		self.KMX64_CNTL2_MAG_EN_MASK                              = 0x02         # controls the operating mode of the magnetometer sensor
		self.KMX64_CNTL2_ACCEL_EN_MASK                            = 0x01         
		self.KMX64_COTR_TEST_RESP_MASK                            = 0xFF         
		self.KMX64_BUF_CTRL_2_BUF_M_MASK                          = 0x06         
		self.KMX64_BUF_CTRL_3_BFI_EN_MASK                         = 0x80         # controls the buffer full interrupt
		self.KMX64_BUF_CTRL_3_BUF_AX_MASK                         = 0x40         # ax to be buffered
		self.KMX64_BUF_CTRL_3_BUF_AY_MASK                         = 0x20         # ay to be buffered
		self.KMX64_BUF_CTRL_3_BUF_AZ_MASK                         = 0x10         # az to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MX_MASK                         = 0x08         # mx to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MY_MASK                         = 0x04         # my to be buffered
		self.KMX64_BUF_CTRL_3_BUF_MZ_MASK                         = 0x02         # mz to be buffered
		self.KMX64_BUF_CTRL_3_BUF_TEMP_MASK                       = 0x01         # temperature to be buffered
		self.KMX64_BUF_STATUS_2_SMP_LEV_H_MASK                    = 0x03         
		self.KMX64_BUF_STATUS_3_SMP_PAST_H_MASK                   = 0xFF         # Sample over flow; reports the number of data bytes that have been missed since the sample buffer was filled.  If this register reads 0, the buffer has not over flowed. This is cleared for BUF_CLEAR command and when the data is read from BUF_READ