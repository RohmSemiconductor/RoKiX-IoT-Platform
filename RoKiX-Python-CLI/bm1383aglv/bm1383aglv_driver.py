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
from bm1383aglv import bm1383aglv_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

r = bm1383aglv_registers.registers()
b = bm1383aglv_registers.bits()
m = bm1383aglv_registers.masks()
e = bm1383aglv_registers.enums()


class BM1383AGLVDriver(SensorDriver):
    supported_parts = ['BM1383AGLV']
    _WAI = (b.BM1383AGLV_ID1_ID1_ID1)
    _WAIREG = r.BM1383AGLV_ID1
    _WAI2 = (b.BM1383AGLV_ID2_ID2_ID2)
    _WAIREG2 = r.BM1383AGLV_ID2

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x5d]
        self.supported_connectivity = [BUS1_I2C]
        self.int_pins = [1, 2]  # bm1383aglv has only one drdy, but it can be connected to either of aardvark gpio pins.
        self.name = 'BM1383AGLV'

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
        LOGGER.info("wrong BM1383AGLV MAN_ID received: 0x%02x" % resp[0])
        return 0

    # Read value, modify and write it back, read again. Make sure the value changed. Restore original value.

    def ic_test(self):
         # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(r.BM1383AGLV_MODE_CONTROL)[0]
        self.write_register(r.BM1383AGLV_MODE_CONTROL, (datain1 ^ 0x01))  # toggle between standby and oneshot
        datain2 = self.read_register(r.BM1383AGLV_MODE_CONTROL)[0]
        self.write_register(r.BM1383AGLV_MODE_CONTROL, datain1)
        if datain2 == (datain1 ^ 0x01):
            return True
        return False

    # setup sensor to be ready for multiple measurements
    def set_default_on(self):
        self.set_power_on()
        self.set_averaging(b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS)
        self.enable_drdy_pin()
        self.start_continuous_measurement()

    def _read_data(self, channel=None):
        # self.reset_drdy_pin()
        return self.read_data_raw()
        # return self.read_temperature_pressure()        #Choose between these two outputs for default

    def set_power_on(self):
        # time.sleep(1e-4)  # wait >0.1ms
        delay_seconds(1e-4)
        self.write_register(r.BM1383AGLV_POWER_DOWN, b.BM1383AGLV_POWER_DOWN_PWR_DOWN_UP)
        # time.sleep(2e-3)  # wait >2ms
        delay_seconds(1e-4)
        self.write_register(r.BM1383AGLV_RESET, b.BM1383AGLV_RESET_RSTB_STANDBY)

    def set_power_off(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_MODE_STANDBY,
            m.BM1383AGLV_MODE_CONTROL_MODE_MASK)
        #self.write_register(r.BM1383AGLV_RESET, b.BM1383AGLV_RESET_MODE_RESET)
        #self.write_register(r.BM1383AGLV_POWER_DOWN, b.BM1383AGLV_POWER_DOWN_POWER_DOWN)

    def set_shutdown(self):
        self.write_register(r.BM1383AGLV_RESET, b.BM1383AGLV_RESET_RSTB_RESET)
        self.write_register(r.BM1383AGLV_POWER_DOWN, b.BM1383AGLV_POWER_DOWN_PWR_DOWN_DOWN)

    def por(self):
        """
        This sensor doesn't have soft_reset command so just cycle to power off state and back
        """
        self.set_shutdown()
        self.set_power_on()

    # set output data rate

    def set_odr(self, valuex):
        LOGGER.debug('Odr is selected indirectly in BM1383AGLV. Indexes [0:4] give ODR 20, [5]:ODR 10, [6]:ODR 5')
        assert valuex in [b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_1_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_2_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_4_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_8_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_32_120MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_64_240MS]
        self.set_bit_pattern(r.BM1383AGLV_MODE_CONTROL, valuex, m.BM1383AGLV_MODE_CONTROL_AVE_NUM_MASK)

    # reads averaging value and deducts output data rate from that

    def read_odr(self):
        ave_num = self.read_register(r.BM1383AGLV_MODE_CONTROL)[0] & m.BM1383AGLV_MODE_CONTROL_AVE_NUM_MASK
        if ave_num in (b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_1_60MS,
                       b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_2_60MS,
                       b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_4_60MS,
                       b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_8_60MS,
                       b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS):
            odr = 20  # 50ms rate = 20Hz
        elif ave_num == b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_32_120MS:
            odr = 10  # 100ms rate = 10Hz
        elif ave_num == b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_64_240MS:
            odr = 5  # 200ms rate = 5Hz
        else:
            odr = 0  # invalid averaging value
        return odr

    # input valuex is b.BM1383AGLV_MODE_CONTROL_AVE_NUM_*
    def set_averaging(self, valuex):
        assert valuex in [b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_1_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_2_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_4_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_8_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_16_60MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_32_120MS,
                          b.BM1383AGLV_MODE_CONTROL_AVE_NUM_AVG_64_240MS]
        self.set_bit_pattern(r.BM1383AGLV_MODE_CONTROL, valuex, m.BM1383AGLV_MODE_CONTROL_AVE_NUM_MASK)

    def enable_drdy_pin(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_DREN_ENABLED,
            m.BM1383AGLV_MODE_CONTROL_DREN_MASK)

    def disable_drdy_pin(self):
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_DREN_DISABLED,
            m.BM1383AGLV_MODE_CONTROL_DREN_MASK)

    def start_oneshot_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_MODE_ONE_SHOT,
            m.BM1383AGLV_MODE_CONTROL_MODE_MASK)

    def start_continuous_measurement(self):
        # Assume: AVE_NUM and DREN are already setup
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_MODE_CONTINUOUS,
            m.BM1383AGLV_MODE_CONTROL_MODE_MASK)

    def stop_measurement(self):
        """
        Oneshot is interrupted if ongoing. Continuous is stopped if ongoing. No new measurement results after this command.
        """
        self.set_bit_pattern(
            r.BM1383AGLV_MODE_CONTROL,
            b.BM1383AGLV_MODE_CONTROL_MODE_STANDBY,
            m.BM1383AGLV_MODE_CONTROL_MODE_MASK)

    def read_drdy(self):
        return self.read_drdy_reg()

    def read_drdy_reg(self):
        """
        Used by framework for poll loop. "Poll data ready register via i2c, return register status True/False"
        """
        drdybit = (self.read_register(r.BM1383AGLV_STATUS))[0] & m.BM1383AGLV_STATUS_RD_DRDY_MASK
        drdy_status = (drdybit == b.BM1383AGLV_STATUS_RD_DRDY_READY)
        return drdy_status  # True/False

    def release_interrupts(self):
        self.read_drdy()

    def read_data_raw(self):
        data = self.read_register(r.BM1383AGLV_STATUS, 6)
        return struct.unpack('>BBBBh', data)

    def counts_to_temperature(self):
        data = self.read_register(r.BM1383AGLV_TEMPERATURE_MSB, 2)
        temp_raw = struct.unpack('>h', data)
        temp_celsius = float(temp_raw) / 32  # 'C
        return temp_celsius  # Temp 'C, Pressure hPa   (10hPa = 1kPa)

    def counts_to_pressure(self):
        data = self.read_register(r.BM1383AGLV_PRESSURE_MSB, 3)
        (press_raw, press_raw_xlb) = struct.unpack('>HB', data)
        press_all = (press_raw << 6) | (press_raw_xlb & 0b00111111)
        pressure_hpa = float(press_all) / 2048  # hPa
        return pressure_hpa  # Temp 'C, Pressure hPa   (10hPa = 1kPa)
