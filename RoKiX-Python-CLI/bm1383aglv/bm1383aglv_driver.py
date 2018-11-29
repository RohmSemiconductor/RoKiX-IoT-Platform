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
from kx_lib import kx_logger
from . import bm1383aglv_registers as sensor

LOGGER = kx_logger.get_logger(__name__)

r = sensor.registers()
b = sensor.bits()
m = sensor.masks()
e = sensor.enums()


class bm1383aglv_driver(SensorDriver):
    _WAI = (b.BM1383AGLV_ID1_REG_MANUFACTURER_ID1)
    _WAIREG = r.BM1383AGLV_ID1_REG
    _WAI2 = (b.BM1383AGLV_ID2_REG_MANUFACTURER_ID2)
    _WAIREG2 = r.BM1383AGLV_ID2_REG

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x5d]
        self.SPI_SUPPORT = False
        self.I2C_SUPPORT = True
        self.int_pins = [1, 2]  # bm1383aglv has only one drdy, but it can be connected to either of aardvark gpio pins.
        self.name = 'BM1383AGLV'
        self.connected = False

    # Read component ID and compare it to expected value
    def probe(self):
        self.connected = True
        resp = self.read_register(self._WAIREG)
        if resp[0] == self._WAI:
            resp = self.read_register(self._WAIREG2)
            if resp[0] == self._WAI2:
                # configurations to register_dump()
                self._registers = dict(r.__dict__)
                self._dump_range = (r.BM1383AGLV_REGISTER_DUMP_START, r.BM1383AGLV_REGISTER_DUMP_END)
                return 1

        self.connected = False
        return 0

    # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.

    def ic_test(self):
         # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BM1383AGLV_MODE_CONTROL_REG)[0]
        self.write_register(r.BM1383AGLV_MODE_CONTROL_REG, (datain1 ^ 0x01))  # toggle between standby and oneshot
        datain2 = self.read_register(r.BM1383AGLV_MODE_CONTROL_REG)[0]
        self.write_register(r.BM1383AGLV_MODE_CONTROL_REG, datain1)
        if datain2 == (datain1 ^ 0x01):
            return True
        return False

    # setup sensor to be ready for multiple measurements
    def set_default_on(self):
        self.set_power_on()
        self.set_averaging(b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS)
        self.enable_drdy_pin()
        self.start_continuous_measurement()
        return

    def read_data(self):
        return self.read_data_raw()
        # return self.read_temperature_pressure()        #Choose between these two outputs for default

    def set_power_on(self):
        time.sleep(1e-4)  # wait >0.1ms
        self.write_register(r.BM1383AGLV_POWER_REG, b.BM1383AGLV_POWER_REG_POWER_UP)
        time.sleep(2e-3)  # wait >2ms
        self.write_register(r.BM1383AGLV_RESET_REG, b.BM1383AGLV_RESET_REG_MODE_STANDBY)
        return

    def set_power_off(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_MODE_STANDBY,
            m.BM1383AGLV_MODE_CONTROL_REG_MODE_MASK)
        #self.write_register(r.BM1383AGLV_RESET_REG, b.BM1383AGLV_RESET_REG_MODE_RESET)
        #self.write_register(r.BM1383AGLV_POWER_REG, b.BM1383AGLV_POWER_REG_POWER_DOWN)
        return

    def set_shutdown(self):
        self.write_register(r.BM1383AGLV_RESET_REG, b.BM1383AGLV_RESET_REG_MODE_RESET)
        self.write_register(r.BM1383AGLV_POWER_REG, b.BM1383AGLV_POWER_REG_POWER_DOWN)
        return

    def por(self):
        """
        This sensor doesn't have soft_reset command so just cycle to power off state and back
        """
        self.set_shutdown()
        self.set_power_on()
        return

    # set output data rate

    def set_odr(self, valuex):
        LOGGER.debug('Odr is selected indirectly in BM1383AGLV. Indexes [0:4] give ODR 20, [5]:ODR 10, [6]:ODR 5')
        assert (valuex) in [b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS]
        self.set_bit_pattern(r.BM1383AGLV_MODE_CONTROL_REG, valuex, m.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_MASK)
        return

    # reads averaging value and deducts output data rate from that

    def read_odr(self):
        ave_num = self.read_register(r.BM1383AGLV_MODE_CONTROL_REG)[0] & m.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_MASK
        if (ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS or
            ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS or
            ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS or
            ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS or
                ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS):
            odr = 20  # 50ms rate = 20Hz
        elif (ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS):
            odr = 10  # 100ms rate = 10Hz
        elif (ave_num == b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS):
            odr = 5  # 200ms rate = 5Hz
        else:
            odr = 0  # invalid averaging value
        return odr

    # input valuex is b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_*
    def set_averaging(self, valuex):
        assert (valuex) in [b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_1_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_2_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_4_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_8_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_16_50MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_32_100MS,
                            b.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_AVG_64_200MS]
        self.set_bit_pattern(r.BM1383AGLV_MODE_CONTROL_REG, valuex, m.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM_MASK)
        return

    def enable_drdy_pin(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_DRDY_ENABLED,
            m.BM1383AGLV_MODE_CONTROL_REG_DRDY_MASK)
        return

    def disable_drdy_pin(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_DRDY_DISABLED,
            m.BM1383AGLV_MODE_CONTROL_REG_DRDY_MASK)
        return

    def start_oneshot_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_MODE_ONE_SHOT,
            m.BM1383AGLV_MODE_CONTROL_REG_MODE_MASK)
        return

    def start_continuous_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_MODE_CONTINUOUS,
            m.BM1383AGLV_MODE_CONTROL_REG_MODE_MASK)
        return

    def stop_measurement(self):
        """
        Oneshot is interrupted if ongoing. Continuous is stopped if ongoing. No new measurement results after this command.
        """
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL_REG,
            b.BM1383AGLV_MODE_CONTROL_REG_MODE_STANDBY,
            m.BM1383AGLV_MODE_CONTROL_REG_MODE_MASK)
        return

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        """
        drdybit = (self.read_register(r.BM1383AGLV_STATUS_REG))[0] & m.BM1383AGLV_STATUS_REG_DRDY_MASK
        drdy_status = (drdybit == b.BM1383AGLV_STATUS_REG_DRDY_READY)
        return drdy_status  # True/False

    def reset_drdy_pin(self):
        self.read_drdy()
        return

    def read_data_raw(self):
        data = self.read_register(r.BM1383AGLV_PRESSURE_OUT_MSB, 5)
        dataout = struct.unpack('>BBBh', data)
        return dataout

    def read_temperature_pressure(self):
        data = self.read_register(r.BM1383AGLV_PRESSURE_OUT_MSB, 5)
        (P_raw, P_raw_xlb, T_raw) = struct.unpack('>HBh', data)
        temperatureC = float(T_raw) / 32  # 'C
        P_all = (P_raw << 6) | ((P_raw_xlb & 0b11111100) >> 2)
        pressure_hPa = float(P_all) / 2048  # hPa
        return temperatureC, pressure_hPa  # Temp 'C, Pressure hPa   (10hPa = 1kPa)

    def read_temperature(self):
        data = self.read_register(r.BM1383AGLV_TEMPERATURE_OUT_MSB, 2)
        T_raw = struct.unpack('>h', data)
        temperatureC = float(T_raw) / 32  # 'C
        return temperatureC  # Temp 'C, Pressure hPa   (10hPa = 1kPa)

    def read_pressure(self):
        data = self.read_register(r.BM1383AGLV_PRESSURE_OUT_MSB, 3)
        (P_raw, P_raw_xlb) = struct.unpack('>HB', data)
        P_all = (P_raw << 6) | (P_raw_xlb & 0b00111111)
        pressure_hPa = float(P_all) / 2048  # hPa
        return pressure_hPa  # Temp 'C, Pressure hPa   (10hPa = 1kPa)
