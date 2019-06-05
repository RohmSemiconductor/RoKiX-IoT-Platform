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
from . import imports  # pylint: disable=unused-import
from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger
from kx_lib.kx_util import delay_seconds
from kx_lib.kx_configuration_enum import CH_MAG, ACTIVE_LOW, ACTIVE_HIGH
from bm1422agmv import bm1422agmv_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

r = bm1422agmv_registers.registers()
b = bm1422agmv_registers.bits()
m = bm1422agmv_registers.masks()
e = bm1422agmv_registers.enums()


class BM1422AGMVDriver(SensorDriver):
    supported_parts = ['BM1422AGMV']
    _WAI = (b.BM1422AGMV_WHO_AM_I_WIA_ID)
    _WAIREG = r.BM1422AGMV_WHO_AM_I

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x0e, 0x0f]
        self.supported_connectivity = [BUS1_I2C]
        self.int_pins = [1, 2]  # bm1422agmv has only one drdy, but it can be connected to either of aardvark gpio pins.
        self.name = "BM1422AGMV"

    # Read component ID and compare it to expected value
    def probe(self):
        self.connected = True
        resp = self.read_register(self._WAIREG)
        if resp[0] != self._WAI:
            self.connected = False
            return 0

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BM1422AGMV_REGISTER_DUMP_START, r.BM1422AGMV_REGISTER_DUMP_END)
        return 1

        # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.
    def ic_test(self):
         # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BM1422AGMV_CNTL1)[7]
        self.write_register(r.BM1422AGMV_CNTL1, (datain1 ^ 0x80))  # toggle between standby and active
        datain2 = self.read_register(r.BM1422AGMV_CNTL1)[7]
        self.write_register(r.BM1422AGMV_CNTL1, datain1)
        if datain2 == (datain1 ^ 0x80):
            return True
        return False

    # setup sensor to be ready for multiple measurements
    def set_default_on(self):
        self.set_power_on()
        self.set_odr(b.BM1422AGMV_CNTL1_ODR_20)
        self.set_averaging(b.BM1422AGMV_AVER_AVG_1TIMES)
        self.disable_drdy_pin()
        self.start_continuous_measurement()

    def _read_data(self, channel=CH_MAG):
        return self.read_data_raw()
        # return self.read_temperature_pressure()        #Choose between these two outputs for default

    def set_power_on(self):
        delay_seconds(1e-4)  # wait >0.1ms
        #self.write_register(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_PC1_ON )
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_PC1_ON, m.BM1422AGMV_CNTL1_PC1_MASK)
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_RST_LV_RELEASE, m.BM1422AGMV_CNTL1_RST_LV_MASK)
        delay_seconds(2e-3)  # wait >2ms
        self.write_register(r.BM1422AGMV_CNTL4_LSB, 0x00)
        self.write_register(r.BM1422AGMV_CNTL4_MSB, 0x00)

    def set_power_off(self):
        #self.write_register(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_PC1_OFF)
        #self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_PC1_OFF, m.BM1422AGMV_CNTL1_PC1_MASK)
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_FS1_SINGLE, m.BM1422AGMV_CNTL1_FS1_MASK)

    def shutdown(self):
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_PC1_OFF, m.BM1422AGMV_CNTL1_PC1_MASK)

    def por(self):
        """
        This sensor doesn't have soft_reset command so just cycle to power off state and back
        """
        self.write_register(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_RST_LV_RESET)
        # self.set_power_off()
        # self.set_power_on()

    # set output data rate

    def set_odr(self, valuex):
        assert valuex in [b.BM1422AGMV_CNTL1_ODR_20,
                          b.BM1422AGMV_CNTL1_ODR_100,
                          b.BM1422AGMV_CNTL1_ODR_10,
                          b.BM1422AGMV_CNTL1_ODR_1000]
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, valuex, m.BM1422AGMV_CNTL1_ODR_MASK)

    def read_odr(self):
        odr_num = self.read_register(r.BM1422AGMV_CNTL1) & m.BM1422AGMV_CNTL1_ODR_MASK
        if odr_num == b.BM1422AGMV_CNTL1_ODR_20:
            odr = 20
        elif odr_num == b.BM1422AGMV_CNTL1_ODR_100:
            odr = 100
        elif odr_num == b.BM1422AGMV_CNTL1_ODR_10:
            odr = 10
        elif odr_num == b.BM1422AGMV_CNTL1_ODR_1000:
            odr = 1000
        else:
            odr = 0  # invalid averaging value
        return odr

    # input valuex is b.BM1422AGMV_MODE_CONTROL_REG_AVE_NUM_*
    def set_averaging(self, valuex):
        assert valuex in [b.BM1422AGMV_AVER_AVG_4TIMES,
                          b.BM1422AGMV_AVER_AVG_2TIMES,
                          b.BM1422AGMV_AVER_AVG_8TIMES,
                          b.BM1422AGMV_AVER_AVG_16TIMES,
                          b.BM1422AGMV_AVER_AVG_1TIMES]
        self.set_bit_pattern(r.BM1422AGMV_AVER, valuex, m.BM1422AGMV_AVER_AVG_MASK)

    def enable_drdy_pin(self):
        self.set_bit_pattern(r.BM1422AGMV_CNTL2, b.BM1422AGMV_CNTL2_DREN_ENABLED, m.BM1422AGMV_CNTL2_DREN_MASK)

    def disable_drdy_pin(self):
        self.set_bit_pattern(r.BM1422AGMV_CNTL2, b.BM1422AGMV_CNTL2_DREN_DISABLED, m.BM1422AGMV_CNTL2_DREN_MASK)

    def set_drdy_low_active(self):
        self.set_bit_pattern(r.BM1422AGMV_CNTL2, b.BM1422AGMV_CNTL2_DRP_LOWACTIVE, m.BM1422AGMV_CNTL2_DRP_MASK)

    def set_drdy_high_active(self):
        self.set_bit_pattern(r.BM1422AGMV_CNTL2, b.BM1422AGMV_CNTL2_DRP_HIGHACTIVE, m.BM1422AGMV_CNTL2_DRP_MASK)

    def set_interrupt_polarity(self, intpin=1, polarity=ACTIVE_LOW):
        assert intpin in self.int_pins
        assert polarity in [ACTIVE_LOW, ACTIVE_HIGH]

        if intpin == 1:
            if polarity == ACTIVE_HIGH:
                self.set_drdy_high_active()
            else:
                self.set_drdy_low_active()

    def start_oneshot_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_FS1_SINGLE, m.BM1422AGMV_CNTL1_FS1_MASK)
        self.set_bit_pattern(r.BM1422AGMV_CNTL3, b.BM1422AGMV_CNTL3_FORCE_START, m.BM1422AGMV_CNTL3_FORCE_MASK)

    def start_continuous_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_FS1_CONT, m.BM1422AGMV_CNTL1_FS1_MASK)
        self.set_bit_pattern(r.BM1422AGMV_CNTL3, b.BM1422AGMV_CNTL3_FORCE_START, m.BM1422AGMV_CNTL3_FORCE_MASK)

    def stop_measurement(self):
        """
        Oneshot is interrupted if ongoing. Continuous is stopped if ongoing. No new measurement results after this command.
        """
        self.set_bit_pattern(r.BM1422AGMV_CNTL1, b.BM1422AGMV_CNTL1_FS1_SINGLE, m.BM1422AGMV_CNTL1_FS1_MASK)

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        """
        drdybit = self.read_register(r.BM1422AGMV_STA1)[0] & m.BM1422AGMV_STA1_DRDY_MASK
        drdy_status = (drdybit == b.BM1422AGMV_STA1_DRDY_READY)
        return drdy_status  # True/False

    def reset_drdy_pin(self):
        self.read_drdy()

    def read_magnetometer(self):
        data = self.read_register(r.BM1422AGMV_DATAX, 6)
        dataout = struct.unpack('hhh', data)
        return dataout

    def read_data_raw(self):
        #
        # Data registers can have different positons.
        #
        #s_form = ()
        #data = self.read_register(r.BM1422AGMV_TEMP, 2)
        #s_form = s_form + struct.unpack('h', data)
        data = self.read_register(r.BM1422AGMV_DATAX, 6)
        #s_form = s_form + struct.unpack('hhh', data)
        # return list(s_form)
        return struct.unpack('hhh', data)

    def read_temperature(self):
        data = self.read_register(r.BM1422AGMV_TEMP, 2)
        temp_data = struct.unpack('h', data)
        return temp_data
