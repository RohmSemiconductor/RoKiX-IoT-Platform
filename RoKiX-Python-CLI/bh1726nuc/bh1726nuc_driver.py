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
"""Driver for the ROHM BH1726NUC ambient light sensor."""
import struct

from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger

from . import imports  # pylint: disable=unused-import
from . import bh1726nuc_registers as registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

R = registers.registers()
B = registers.bits()
M = registers.masks()
E = registers.enums()


class BH1726NUCDriver(SensorDriver):
    _WAI = B.BH1726NUC_PART_ID_PART_ID_ID
    name = 'BH1726NUC'
    supported_parts = [name]
    I2C_SAD_LIST = [0x29, 0x39]
    INT_PINS = [1]

    def __init__(self):
        SensorDriver.__init__(self)
        self._registers = dict(R.__dict__)
        self._dump_range = (R.BH1726NUC_REGISTER_DUMP_START,
                            R.BH1726NUC_REGISTER_DUMP_END)
        self.supported_connectivity = [BUS1_I2C]

    def probe(self):
        """Check the component ID.

        Returns:
            int: 1 if ID matches this driver, otherwise 0
        """
        # This is necessary so that read_register won't fail because we're
        # not connected.
        self.connected = True

        resp = self.read_register(R.BH1726NUC_PART_ID)
        if resp[0] == self._WAI:
            return 1

        self.connected = False
        return 0

    def por(self):
        self.write_register(R.BH1726NUC_RESET, 0x00)

    def ic_test(self):
        pass

    def set_default_on(self):
        self.set_power_on()
        self.start_measurement()
        self.write_register(R.BH1726NUC_TIMING, 0xda)

    def read_data(self):
        data = self.read_register(R.BH1726NUC_DATA0_LSB, 4)
        return struct.unpack('hh', data)

    def read_drdy(self):
        return self.read_register(R.BH1726NUC_CONTROL)[0] & B.BH1726NUC_CONTROL_ADC_VALID != 0

    def set_power_on(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL, B.BH1726NUC_CONTROL_POWER_ENABLE,
                             M.BH1726NUC_CONTROL_POWER_MASK)

    def set_power_off(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL, B.BH1726NUC_CONTROL_POWER_DISABLE,
                             M.BH1726NUC_CONTROL_POWER_MASK)

    def start_measurement(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL, B.BH1726NUC_CONTROL_ADC_EN_ENABLE,
                             M.BH1726NUC_CONTROL_ADC_EN_MASK)

    def stop_measurement(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL, B.BH1726NUC_CONTROL_ADC_EN_DISABLE,
                             M.BH1726NUC_CONTROL_ADC_EN_MASK)

    def set_odr(self, valuex):
        self.write_register(R.BH1726NUC_TIMING, valuex)

    def set_gain0(self, valuex):
        self.set_bit_pattern(R.BH1726NUC_GAIN, valuex, M.BH1726NUC_GAIN_DATA0_GAIN_MASK)

    def set_gain1(self, valuex):
        self.set_bit_pattern(R.BH1726NUC_GAIN, valuex, M.BH1726NUC_GAIN_DATA1_GAIN_MASK)

    def clear_interrupt(self):
        self.write_register(R.BH1726NUC_INT_RESET, 0x00)

    def read_interrupt_thresholds(self):
        """
        :return: (uint16, uin16) raw data from (threshold_high, threshold_low)
        """
        data = self.read_register(R.BH1726NUC_TH_LOW_LSB, 2 * 2)
        threshold_high, threshold_low = struct.unpack('HH', data)
        return threshold_high, threshold_low

    def write_interrupt_thresholds(self, threshold_low, threshold_high):
        if not 0 <= threshold_high < 2**16:
            LOGGER.debug("threshold_high value out of bounds.")
            raise TypeError
        if not 0 <= threshold_low < 2**16:
            LOGGER.debug("threshold_low value out of bounds.")
            raise TypeError
        thl = (threshold_high & 0xff)
        thh = (threshold_high >> 8) & 0xff
        tll = (threshold_low & 0xff)
        tlh = (threshold_low >> 8) & 0xff
        self.write_register(R.BH1726NUC_TH_HIGH_LSB, thl)
        self.write_register(R.BH1726NUC_TH_HIGH_MSB, thh)
        self.write_register(R.BH1726NUC_TH_LOW_LSB, tll)
        self.write_register(R.BH1726NUC_TH_LOW_MSB, tlh)

    def get_interrupt_persistence(self):
        """
        :return: B.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function status
        """
        status = self.read_register(R.BH1726NUC_INTERRUPT) & M.BH1726NUC_INTERRUPT_PERSIST_MASK
        return status

    def set_interrupt_persistence(self, persistence):
        """
        :parameter: B.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function
        """
        assert persistence in [
            B.BH1726NUC_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,
            B.BH1726NUC_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,
            B.BH1726NUC_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,
            B.BH1726NUC_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME,
        ]
        self.set_bit_pattern(R.BH1726NUC_INTERRUPT, persistence,
                             M.BH1726NUC_INTERRUPT_PERSIST_MASK)

    def enable_int_pin(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL,
                             B.BH1726NUC_CONTROL_ADC_INTR_ACTIVE,
                             M.BH1726NUC_CONTROL_ADC_INTR_MASK)
        self.set_bit_pattern(R.BH1726NUC_INTERRUPT,
                             B.BH1726NUC_INTERRUPT_INT_EN_VALID,
                             M.BH1726NUC_INTERRUPT_INT_EN_MASK)

    def disable_int_pin(self):
        self.set_bit_pattern(R.BH1726NUC_CONTROL,
                             B.BH1726NUC_CONTROL_ADC_INTR_INACTIVE,
                             M.BH1726NUC_CONTROL_ADC_INTR_MASK)
