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
# pylint: disable=bad-whitespace
import imports  # pylint: disable=unused-import
from kx126.kx126_driver import r, e


class Pedometer_parameters_odr_50:
### Pedometer algorithm settings, configuration ODR_50, ODR = 50 Hz.
### Obtained so far with the sensor in the wrist setting.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_10']
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['50'] # b.KX126_PED_CNTL2_PED_ODR_50
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x0E)
    M_H         =   (0x0B)
    M_L         =   (0x02)
    T_L         =   (0x03)
    T_M         =   (0x0D)
    T_P         =   (0x10)

class Pedometer_parameters_odr_100:
### Pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.
### These are the same as the RND7 set.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_12'] #b.KX126_PED_CNTL1_STP_TH_STEP_12
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100'] # b.KX126_PED_CNTL2_PED_ODR_100
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x24)
    M_H         =   (0x13)
    M_L         =   (0x0B)
    T_L         =   (0x08)
    T_M         =   (0x19)
    T_P         =   (0x1C)

class Pedometer_parameters_rnd5:
### Pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_8']
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100']
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x03 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x1E)
    M_H         =   (0x13)
    M_L         =   (0x0C)
    T_L         =   (0x07)
    T_M         =   (0x19)
    T_P         =   (0x1E)

class Pedometer_parameters_pocket:
### Pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.
### For the general or pocket use case.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_8']
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100']
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x5A)
    M_H         =   (0x14)
    M_L         =   (0x06)
    T_L         =   (0x05)
    T_M         =   (0x16)
    T_P         =   (0x13)

class Pedometer_parameters_wrist:
### Pedometer algorithm settings, configuration ODR_100, ODR = 100 Hz.
### For the wrist use case.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_8']
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100']
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x03 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x2D)
    M_H         =   (0x14)
    M_L         =   (0x06)
    T_L         =   (0x0C)
    T_M         =   (0x16)
    T_P         =   (0x13)

class Pedometer_parameters_robot_odr_100:
### Pedometer algorithm settings for a toy robot, configuration ODR_100, ODR = 100 Hz.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['NO_STEP'] #b.KX126_PED_CNTL1_STP_TH_STEP_12
    MAG_SCALE   =   (0x03 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100'] # b.KX126_PED_CNTL2_PED_ODR_100
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x00 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x1D)
    M_H         =   (0x27)
    M_L         =   (0x0C)
    T_L         =   (0x15)
    T_M         =   (0x27)
    T_P         =   (0x1D)

class Pedometer_parameters_vibra_odr_100:
### Pedometer algorithm settings when vibration is used in some device, configuration ODR_100, ODR = 100 Hz.
    STP_TH      =   e.KX126_PED_CNTL1_STP_TH['STEP_12'] #b.KX126_PED_CNTL1_STP_TH_STEP_12
    MAG_SCALE   =   (0x06 << 0)
    HPS         =   (0x02 << 4)
    LP_LEN      =   e.KX126_PED_CNTL2_PED_ODR['100'] # b.KX126_PED_CNTL2_PED_ODR_100
    FCB         =   (0x02 << 3)
    FCA         =   (0x07 << 0)
    B_CNT       =   (0x01 << 4)
    A_H         =   (0x0F << 0)
    A_L         =   (0x1E)
    M_H         =   (0x0A)
    M_L         =   (0x0D)
    T_L         =   (0x00)
    T_M         =   (0x2D)
    T_P         =   (0x03)
