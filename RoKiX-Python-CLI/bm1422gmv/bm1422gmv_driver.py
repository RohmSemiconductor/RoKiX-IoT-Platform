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
import time
import struct

from . import imports  # pylint: disable=unused-import
from kx_lib.kx_sensor_base import SensorDriver
from . import bm1422gmv_registers as sensor

r = sensor.registers()
b = sensor.bits()
m = sensor.masks()
e = sensor.enums()


class bm1422gmv_driver(SensorDriver):
    _WAI = (b.BM1422GMV_WHO_AM_I_WIA_ID)
    _WAIREG = r.BM1422GMV_WHO_AM_I

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x0e, 0x0f]
        self.name="BM1422GMV"
        self.I2C_SUPPORT = True
        self.int_pins = [1,2]       #bm1422gmv has only one drdy, but it can be connected to either of aardvark gpio pins.
        self.connected = False

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BM1422GMV_REGISTER_DUMP_START, r.BM1422GMV_REGISTER_DUMP_END)
        return

    # Read component ID and compare it to expected value
    def probe(self):
        #return self.probe_glv()    ##fixme: remove this line when aglv component is available and in use
        self.connected = True
        resp = self.read_register(self._WAIREG)
        if resp[0] != self._WAI:
            self.connected = False
            return 0

        return 1

        # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
    def ic_test(self):
         # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BM1422GMV_CNTL1)[7]
        self.write_register(r.BM1422GMV_CNTL1, (datain1 ^ 0x80))  # toggle between standby and active
        datain2 = self.read_register(r.BM1422GMV_CNTL1)[7]
        self.write_register(r.BM1422GMV_CNTL1, datain1)
        if datain2 == (datain1 ^ 0x80):
            return True
        return False

    # setup sensor to be ready for multiple measurements
    def set_default_on(self):
        self.set_power_on()
        self.set_odr(b.BM1422GMV_CNTL1_ODR_20)
        self.set_averaging(b.BM1422GMV_AVER_AVG_1TIMES)
        self.disable_drdy_pin()
        self.start_continuous_measurement()
        return

    def read_data(self):
        return self.read_data_raw()
        # return self.read_temperature_pressure()        #Choose between these two outputs for default
        return

    def set_power_on(self):
        time.sleep(1e-4)  # wait >0.1ms
        #self.write_register(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_PC1_ON )
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_PC1_ON, m.BM1422GMV_CNTL1_PC1_MASK)
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_RST_LV_RELEASE, m.BM1422GMV_CNTL1_RST_LV_MASK)
        time.sleep(2e-3)  # wait >2ms
        self.write_register(r.BM1422GMV_CNTL4_LSB, 0x00)
        self.write_register(r.BM1422GMV_CNTL4_MSB, 0x00)
        return

    def set_power_off(self):
        #self.write_register(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_PC1_OFF)
        #self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_PC1_OFF, m.BM1422GMV_CNTL1_PC1_MASK)
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_FS1_SINGLE, m.BM1422GMV_CNTL1_FS1_MASK)
        return

    def shutdown(self):
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_PC1_OFF, m.BM1422GMV_CNTL1_PC1_MASK)
        return

    def por(self):
        """
        This sensor doesn't have soft_reset command so just cycle to power off state and back
        """
        self.write_register(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_RST_LV_RESET)
        # self.set_power_off()
        # self.set_power_on()
        return

    # set output data rate

    def set_odr(self, valuex):
        assert (valuex) in [b.BM1422GMV_CNTL1_ODR_20,
                            b.BM1422GMV_CNTL1_ODR_100,
                            b.BM1422GMV_CNTL1_ODR_10,
                            b.BM1422GMV_CNTL1_ODR_1000]
        self.set_bit_pattern(r.BM1422GMV_CNTL1, valuex, m.BM1422GMV_CNTL1_ODR_MASK)
        return

    def read_odr(self):
        odr_num = self.read_register(r.BM1422GMV_CNTL1) & m.BM1422GMV_CNTL1_ODR_MASK
        if (odr_num == b.BM1422GMV_CNTL1_ODR_20):
            odr = 20
        elif (odr_num == b.BM1422GMV_CNTL1_ODR_100):
            odr = 100
        elif (odr_num == b.BM1422GMV_CNTL1_ODR_10):
            odr = 10
        elif (odr_num == b.BM1422GMV_CNTL1_ODR_1000):
            odr = 1000
        else:
            odr = 0  # invalid averaging value
        return odr

    # input valuex is b.BM1422GMV_MODE_CONTROL_REG_AVE_NUM_*
    def set_averaging(self, valuex):
        assert (valuex) in [b.BM1422GMV_AVER_AVG_4TIMES,
                            b.BM1422GMV_AVER_AVG_2TIMES,
                            b.BM1422GMV_AVER_AVG_8TIMES,
                            b.BM1422GMV_AVER_AVG_16TIMES,
                            b.BM1422GMV_AVER_AVG_1TIMES]
        self.set_bit_pattern(r.BM1422GMV_AVER, valuex, m.BM1422GMV_AVER_AVG_MASK)
        return

    def enable_drdy_pin(self):
        self.set_bit_pattern(r.BM1422GMV_CNTL2, b.BM1422GMV_CNTL2_DREN_ENABLED, m.BM1422GMV_CNTL2_DREN_MASK)
        return

    def disable_drdy_pin(self):
        self.set_bit_pattern(r.BM1422GMV_CNTL2, b.BM1422GMV_CNTL2_DREN_DISABLED, m.BM1422GMV_CNTL2_DREN_MASK)
        return

    def set_drdy_low_active(self):
        self.set_bit_pattern(r.BM1422GMV_CNTL2, b.BM1422GMV_CNTL2_DRP_LOWACTIVE, m.BM1422GMV_CNTL2_DRP_MASK)
        return

    def set_drdy_high_active(self):
        self.set_bit_pattern(r.BM1422GMV_CNTL2, b.BM1422GMV_CNTL2_DRP_HIGHACTIVE, m.BM1422GMV_CNTL2_DRP_MASK)
        return

    def start_oneshot_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_FS1_SINGLE, m.BM1422GMV_CNTL1_FS1_MASK)
        self.set_bit_pattern(r.BM1422GMV_CNTL3, b.BM1422GMV_CNTL3_FORCE_START, m.BM1422GMV_CNTL3_FORCE_MASK)
        return

    def start_continuous_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_FS1_CONT, m.BM1422GMV_CNTL1_FS1_MASK)
        self.set_bit_pattern(r.BM1422GMV_CNTL3, b.BM1422GMV_CNTL3_FORCE_START, m.BM1422GMV_CNTL3_FORCE_MASK)
        return

    def stop_measurement(self):
        """
        Oneshot is interrupted if ongoing. Continuous is stopped if ongoing. No new measurement results after this command.
        """
        self.set_bit_pattern(r.BM1422GMV_CNTL1, b.BM1422GMV_CNTL1_FS1_SINGLE, m.BM1422GMV_CNTL1_FS1_MASK)
        return

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        """
        drdybit = self.read_register(r.BM1422GMV_STA1)[0] & m.BM1422GMV_STA1_DRDY_MASK
        drdy_status = (drdybit == b.BM1422GMV_STA1_DRDY_READY)
        return drdy_status  # True/False

    def reset_drdy_pin(self):
        self.read_drdy()
        return

    def read_magnetometer(self):
        data = self.read_register(r.BM1422GMV_DATAX, 6)
        dataout = struct.unpack('hhh', data)
        return dataout

    def read_data_raw(self):
        s_form = ()
        data = self.read_register(r.BM1422GMV_TEMP, 2)
        s_form = s_form + struct.unpack('h', data)
        data = self.read_register(r.BM1422GMV_DATAX, 6)
        s_form = s_form + struct.unpack('hhh', data)

        return s_form

    def read_temperature(self):
        data = self.read_register(r.BM1422GMV_TEMP, 2)
        temp_data = struct.unpack('h', data)
        return temp_data
