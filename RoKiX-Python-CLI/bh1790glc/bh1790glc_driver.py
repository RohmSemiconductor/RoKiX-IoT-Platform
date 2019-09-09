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
"""
    Driver for BH1790GLC Pulse Sensor
"""
import struct
import imports  # pylint: disable=unused-import
from kx_lib.kx_configuration_enum import BUS1_I2C, CH_ACC
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger
from bh1790glc import bh1790glc_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

r = bh1790glc_registers.registers()
b = bh1790glc_registers.bits()
m = bh1790glc_registers.masks()
e = bh1790glc_registers.enums()


class BH1790GLCDriver(SensorDriver):
    _WAI = b.BH1790_PART_ID_WIA_ID

    def __init__(self):
        SensorDriver.__init__(self)
        self.name = 'BH1790GLC'
        self.i2c_sad_list = [0x5B]
        self.supported_connectivity = [BUS1_I2C]
        self.int_pins = [1]
        self._registers = dict(r.__dict__)
        self._dump_range = (r.BH1790_MANUFACTURER_ID,
                            r.BH1790_DATAOUT_LEDON_H)

    def probe(self):
        self.connected = True
        resp = self.read_register(r.BH1790_PART_ID)
        if resp[0] == self._WAI:
            LOGGER.info('detected BH1790LC')
            return 1
        self.connected = False
        return 0

    def por(self):
        self.write_register(r.BH1790_RESET, b.BH1790_RESET_SWRESET)

    def ic_test(self):
        pass

    def set_default_on(self):
        self.set_power_on()
        self.set_led_freq_128hz()
        self.set_odr(b.BH1790_MEAS_CONTROL1_RCYCLE_64HZ)
        self.set_led_pulsed(1)
        self.set_led_pulsed(2)
        self.set_led_on_time_216us()
        self.set_led_current(b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA)
        self.start_measurement()

    def read_data(self):
        data = self.read_register(r.BH1790_DATAOUT_LEDOFF_L, 4)
        return struct.unpack('HH', data)

    def read_drdy(self):
        raise NotImplementedError("bh1790glc doesn't support reading DRDY")

    def set_power_on(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             b.BH1790_MEAS_CONTROL1_RDY_ENABLE,
                             m.BH1790_MEAS_CONTROL1_RDY_MASK)

    def set_power_off(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             b.BH1790_MEAS_CONTROL1_RDY_DISABLE,
                             m.BH1790_MEAS_CONTROL1_RDY_MASK)

    def start_measurement(self):
        self.set_bit_pattern(r.BH1790_MEAS_START,
                             b.BH1790_MEAS_START_MEAS_ST_START,
                             m.BH1790_MEAS_START_MEAS_ST_MASK)

    def stop_measurement(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             b.BH1790_MEAS_CONTROL1_RDY_DISABLE,
                             m.BH1790_MEAS_CONTROL1_RDY_MASK)

    def set_led_constant(self, led):
        assert led in [1, 2]
        if led == 1:
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                                 b.BH1790_MEAS_CONTROL2_LED1_EN_CONSTANT,
                                 m.BH1790_MEAS_CONTROL2_LED1_EN_MASK)
        elif led == 2:
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                                 b.BH1790_MEAS_CONTROL2_LED2_EN_CONSTANT,
                                 m.BH1790_MEAS_CONTROL2_LED2_EN_MASK)

    def set_led_pulsed(self, led):
        assert led in [1, 2]
        if led == 1:
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                                 b.BH1790_MEAS_CONTROL2_LED1_EN_PULSED,
                                 m.BH1790_MEAS_CONTROL2_LED1_EN_MASK)
        elif led == 2:
            self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                                 b.BH1790_MEAS_CONTROL2_LED2_EN_PULSED,
                                 m.BH1790_MEAS_CONTROL2_LED2_EN_MASK)

    def set_led_current(self, led_current):
        assert led_current in [b.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA,
                               b.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA]
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                             led_current,
                             m.BH1790_MEAS_CONTROL2_LED_CURRENT_MASK)

    def set_led_on_time_216us(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                             b.BH1790_MEAS_CONTROL2_LED_ON_TIME_216T_OSC,
                             m.BH1790_MEAS_CONTROL2_LED_ON_TIME_MASK)

    def set_led_on_time_432us(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL2,
                             b.BH1790_MEAS_CONTROL2_LED_ON_TIME_432T_OSC,
                             m.BH1790_MEAS_CONTROL2_LED_ON_TIME_MASK)

    def set_led_freq_64hz(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_64HZ,
                             m.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_MASK)

    def set_led_freq_128hz(self):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             b.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_128HZ,
                             m.BH1790_MEAS_CONTROL1_LED_LIGHTING_FREQ_MASK)

    def set_odr(self, odr):
        self.set_bit_pattern(r.BH1790_MEAS_CONTROL1,
                             odr,
                             m.BH1790_MEAS_CONTROL1_RCYCLE_MASK)
