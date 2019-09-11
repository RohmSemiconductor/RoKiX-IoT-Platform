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
import struct

from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver

from . import imports  # pylint: disable=unused-import
from . import rpr0521rs_registers as registers

R = registers.registers()
B = registers.bits()
M = registers.masks()
E = registers.enums()


class RPR0521RSDriver(SensorDriver):
    _WAIREG = R.RPR0521RS_SYSTEM_CONTROL
    _WAI = B.RPR0521RS_SYSTEM_CONTROL_PART_ID
    I2C_SAD_LIST = [0x38]
    INT_PINS = [1]
    name = "RPR-0521RS"
    supported_parts = [name]

    def __init__(self):
        SensorDriver.__init__(self)
        self._dump_range = (R.RPR0521RS_REGISTER_DUMP_START,
                            R.RPR0521RS_REGISTER_DUMP_END)
        self.supported_connectivity = [BUS1_I2C]

    def probe(self):
        """Check the component ID.

        Returns:
            int: 1 if ID matches this driver, otherwise 0
        """
        # This is necessary so that read_register won't fail because we're
        # not connected.
        self.connected = True

        resp = self.read_register(self._WAIREG)
        if resp[0] == self._WAI:
            return 1

        self.connected = False
        return 0

        # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
    def ic_test(self):
         # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(R.RPR0521RS_MODE_CONTROL)[0]
        # Toggle between RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF and
        # RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS
        self.write_register(R.RPR0521RS_MODE_CONTROL, (datain1 ^ 0x01))
        datain2 = self.read_register(R.RPR0521RS_MODE_CONTROL)[0]
        self.write_register(R.RPR0521RS_MODE_CONTROL, datain1)
        return datain2 == (datain1 ^ 0x01)

    # setup sensor to be ready for default measurements
    def set_default_on(self):
        self.set_als_data0_gain(B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1)
        self.set_als_data1_gain(B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1)
        self.set_ps_gain(B.RPR0521RS_PS_CONTROL_PS_GAIN_X1)
        self.set_measurement_time(B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS)
        self.set_ps_int_sensitivity(B.RPR0521RS_PS_CONTROL_PERSISTENCE_DRDY)
        self.enable_als_ps_measurement()

    def set_power_on(self):
        self.enable_als_ps_measurement()

    def set_power_off(self):
        self.disable_als_ps_measurement()
        self.write_register(R.RPR0521RS_SYSTEM_CONTROL, B.RPR0521RS_SYSTEM_CONTROL_INT_PIN_HI_Z)

    def read_data(self):
        data = self.read_data_raw()
        self.clear_interrupt()
        return data

    def por(self):
        self.soft_reset()

    def set_measurement_time(self, valuex):
        assert valuex in [
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_OFF,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_10MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_40MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_100MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_OFF_400MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_50MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_100MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_100MS_400MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_50MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_100MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_OFF,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_400MS_400MS,
            B.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_50MS_50MS,
        ]
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL, valuex,
                             M.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME_MASK)

    def set_ps_operating_mode(self, valuex):
        assert valuex in [
            B.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_DOUBLE_MEASUREMENT,
            B.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_NORMAL,
        ]
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL, valuex,
                             M.RPR0521RS_MODE_CONTROL_PS_OPERATING_MODE_MASK)

    def set_als_data0_gain(self, valuex):
        assert valuex in [
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X1,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X2,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X64,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_X128,
        ]
        self.set_bit_pattern(R.RPR0521RS_ALS_PS_CONTROL, valuex,
                             M.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK)

    def set_als_data1_gain(self, valuex):
        assert valuex in [
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X1,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X2,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X64,
            B.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_X128,
        ]
        self.set_bit_pattern(R.RPR0521RS_ALS_PS_CONTROL, valuex,
                             M.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK)

    def set_ps_gain(self, valuex):
        assert valuex in [
            B.RPR0521RS_PS_CONTROL_PS_GAIN_X1,
            B.RPR0521RS_PS_CONTROL_PS_GAIN_X2,
            B.RPR0521RS_PS_CONTROL_PS_GAIN_X4,
        ]
        self.set_bit_pattern(R.RPR0521RS_PS_CONTROL, valuex,
                             M.RPR0521RS_PS_CONTROL_PS_GAIN_MASK)

    def get_als_data0_gain(self):
        reg_tmp = self.read_register(R.RPR0521RS_ALS_PS_CONTROL, 1)
        als_gain = reg_tmp | M.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN_MASK
        return als_gain

    def get_als_data1_gain(self):
        reg_tmp = self.read_register(R.RPR0521RS_ALS_PS_CONTROL, 1)
        als_gain = reg_tmp | M.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN_MASK
        return als_gain

    def get_ps_gain(self):
        reg_tmp = self.read_register(R.RPR0521RS_PS_CONTROL, 1)
        ps_gain = reg_tmp | M.RPR0521RS_PS_CONTROL_PS_GAIN_MASK
        return ps_gain

    def enable_als_ps_measurement(self):
        mask = (M.RPR0521RS_MODE_CONTROL_ALS_EN_MASK
                | M.RPR0521RS_MODE_CONTROL_PS_EN_MASK)
        value = (B.RPR0521RS_MODE_CONTROL_ALS_EN_TRUE
                 | B.RPR0521RS_MODE_CONTROL_PS_EN_TRUE)
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL, value, mask)

    def enable_als_measurement(self):
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL,
                             B.RPR0521RS_MODE_CONTROL_ALS_EN_TRUE,
                             M.RPR0521RS_MODE_CONTROL_ALS_EN_MASK)

    def enable_ps_measurement(self):
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL,
                             B.RPR0521RS_MODE_CONTROL_PS_EN_TRUE,
                             M.RPR0521RS_MODE_CONTROL_PS_EN_MASK)

    def disable_als_ps_measurement(self):
        mask = (M.RPR0521RS_MODE_CONTROL_ALS_EN_MASK
                | M.RPR0521RS_MODE_CONTROL_PS_EN_MASK)
        value = (B.RPR0521RS_MODE_CONTROL_ALS_EN_FALSE
                 | B.RPR0521RS_MODE_CONTROL_PS_EN_FALSE)
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL, value, mask)

    def disable_als_measurement(self):
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL,
                             B.RPR0521RS_MODE_CONTROL_ALS_EN_FALSE,
                             M.RPR0521RS_MODE_CONTROL_ALS_EN_MASK)

    def disable_ps_measurement(self):
        self.set_bit_pattern(R.RPR0521RS_MODE_CONTROL,
                             B.RPR0521RS_MODE_CONTROL_PS_EN_FALSE,
                             M.RPR0521RS_MODE_CONTROL_PS_EN_MASK)

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        For this sensor return True if either of Proxy/ALS INT is True.
        """
        interrupt_reg = (self.read_register(R.RPR0521RS_INTERRUPT))[0]
        drdybit = interrupt_reg & (M.RPR0521RS_INTERRUPT_PS_INT_STATUS_MASK)
        drdy_status = (drdybit == B.RPR0521RS_INTERRUPT_PS_INT_STATUS_ACTIVE)
        if drdy_status:
            return drdy_status  # True
        drdybit = interrupt_reg & (M.RPR0521RS_INTERRUPT_ALS_INT_STATUS_MASK)
        drdy_status = (drdybit == B.RPR0521RS_INTERRUPT_ALS_INT_STATUS_ACTIVE)
        return drdy_status  # True/False

    def read_data_raw(self):
        data = self.read_register(R.RPR0521RS_PS_DATA_LSBS, 6)
        # little endian(LowHigh, LowHigh, LowHigh), 16bitPS, 16bitALS0, 16bitALS1
        dataout = struct.unpack('<HHH', data)
        return dataout

    def soft_reset(self):
        value = (B.RPR0521RS_SYSTEM_CONTROL_SW_RESET_START
                 | B.RPR0521RS_SYSTEM_CONTROL_INT_PIN_HI_Z)
        self.write_register(R.RPR0521RS_SYSTEM_CONTROL, value)

    def enable_interrupt_both(self):
        interrupt_reg_new = (B.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION |
                             B.RPR0521RS_INTERRUPT_INT_ASSERT_STABLE |
                             B.RPR0521RS_INTERRUPT_INT_LATCH_ENABLED |
                             B.RPR0521RS_INTERRUPT_INT_TRIG_BY_BOTH)
        self.write_register(R.RPR0521RS_INTERRUPT, interrupt_reg_new)

    def enable_interrupt_ps_only(self):
        interrupt_reg_new = (B.RPR0521RS_INTERRUPT_INT_MODE_PS_TH_OUTSIDE_DETECTION |
                             B.RPR0521RS_INTERRUPT_INT_ASSERT_STABLE |
                             B.RPR0521RS_INTERRUPT_INT_LATCH_ENABLED |
                             B.RPR0521RS_INTERRUPT_INT_TRIG_BY_PS)
        self.write_register(R.RPR0521RS_INTERRUPT, interrupt_reg_new)

    def enable_drdy_int(self):
        self.set_ps_int_sensitivity(B.RPR0521RS_PS_CONTROL_PERSISTENCE_DRDY)
        self.enable_interrupt_ps_only()

    def disable_drdy_int(self):
        self.write_register(R.RPR0521RS_INTERRUPT,
                            B.RPR0521RS_INTERRUPT_INT_TRIG_INACTIVE)

    def set_ps_int_sensitivity(self, valuex):
        """
        Set sensitivity of interrupt.

        intput valuex:  Interrupt is generated after N consecutive measurements if value is
                        outside of limits. N = 0-15. Using 0 will generate interrupt after
                        each measurement regardless of measurement value (~= DRDY).
        """
        assert valuex in [
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_DRDY,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_1,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_2,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_3,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_4,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_5,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_6,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_7,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_8,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_9,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_10,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_11,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_12,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_13,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_14,
            B.RPR0521RS_PS_CONTROL_PERSISTENCE_CONSECUTIVE_15,
        ]
        self.set_bit_pattern(R.RPR0521RS_PS_CONTROL, valuex,
                             M.RPR0521RS_PS_CONTROL_PERSISTENCE_MASK)

    def clear_interrupt(self):
        #self.write_register(R.RPR0521RS_SYSTEM_CONTROL, B.RPR0521RS_SYSTEM_CONTROL_INT_PIN_HI_Z)
        self.read_register(R.RPR0521RS_INTERRUPT)
