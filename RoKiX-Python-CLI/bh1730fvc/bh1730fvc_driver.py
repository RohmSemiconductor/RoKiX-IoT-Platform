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
"""Driver for the ROHM BH1730FVC ambient light sensor."""
import struct

from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger

from . import imports  # pylint: disable=unused-import
from . import bh1730fvc_registers as registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

R = registers.registers()
B = registers.bits()
M = registers.masks()
E = registers.enums()


class BH1730FVCDriver(SensorDriver):
    _WAI = B.BH1730FVC_ID_PART_NUMBER_ID
    name = 'BH1730FVC'
    supported_parts = [name]
    I2C_SAD_LIST = [0x29]
    INT_PINS = [1]

    def __init__(self):
        SensorDriver.__init__(self)
        self._registers = dict(R.__dict__)
        self._dump_range = (R.BH1730FVC_CONTROL, R.BH1730FVC_DATA1HIGH)
        self.supported_connectivity = [BUS1_I2C]

    def probe(self):
        """Check the component ID.

        Returns:
            int: 1 if ID matches this driver, otherwise 0
        """
        # This is necessary so that read_register won't fail because we're
        # not connected.
        self.connected = True

        resp = self.read_register(R.BH1730FVC_ID)
        part_num = resp[0] & M.BH1730FVC_ID_PART_NUMBER_MASK
        if part_num == self._WAI:
            return 1

        self.connected = False
        return 0

    def por(self):
        self._write_command(R.BH1730FVC_RESET)

    def ic_test(self):
        pass

    def set_default_on(self):
        self.set_power_on()
        self.start_measurement()
        self.write_register(R.BH1730FVC_TIMING, 0xda)

    def read_data(self):
        data = self.read_register(R.BH1730FVC_DATA0LOW, 4)
        return struct.unpack('hh', data)

    def read_drdy(self):
        return self.read_register(R.BH1730FVC_CONTROL)[0] & B.BH1730FVC_CONTROL_ADC_VALID != 0

    def set_power_on(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL, B.BH1730FVC_CONTROL_POWER_ENABLE, M.BH1730FVC_CONTROL_POWER_MASK)

    def set_power_off(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL, B.BH1730FVC_CONTROL_POWER_DISABLE, M.BH1730FVC_CONTROL_POWER_MASK)

    def start_measurement(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL, B.BH1730FVC_CONTROL_ADC_EN_ENABLE, M.BH1730FVC_CONTROL_ADC_EN_MASK)

    def stop_measurement(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL, B.BH1730FVC_CONTROL_ADC_EN_DISABLE, M.BH1730FVC_CONTROL_ADC_EN_MASK)

    def set_odr(self, valuex):
        self.write_register(R.BH1730FVC_TIMING, valuex)

    def set_gain(self, valuex):
        self.write_register(R.BH1730FVC_GAIN, valuex)

    def clear_interrupt(self):
        self._write_command(R.BH1730FVC_INT_RESET)

    def read_interrupt_thresholds(self):
        """
        :return: (uint16, uin16) raw data from (threshold_high, threshold_low)
        """
        data = self.read_register(R.BH1730FVC_THLLOW, 2 * 2)
        threshold_high, threshold_low = struct.unpack('HH', data)
        return threshold_high, threshold_low

    def write_interrupt_thresholds(self, threshold_low, threshold_high):
        if not 0 <= threshold_high < 2**16:
            LOGGER.debug("threshold_high value out of bounds.")
            raise TypeError
        if not 0 <= threshold_low < 2**16:
            LOGGER.debug("threshold_low value out of bounds.")
            raise TypeError
        thl = threshold_high & 0xff
        thh = (threshold_high >> 8) & 0xff
        tll = threshold_low & 0xff
        tlh = (threshold_low >> 8) & 0xff
        self.write_register(R.BH1730FVC_THHLOW, thl)
        self.write_register(R.BH1730FVC_THHHIGH, thh)
        self.write_register(R.BH1730FVC_THLLOW, tll)
        self.write_register(R.BH1730FVC_THLHIGH, tlh)

    def get_interrupt_persistence(self):
        """
        :return: B.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function status
        """
        status = self.read_register(R.BH1730FVC_INTERRUPT) & M.BH1730FVC_INTERRUPT_PERSIST_MASK
        return status

    def set_interrupt_persistence(self, persistence):
        """
        :parameter: B.BH1745_PERSISTENCE_OF_INTERRUPT_STATUS_ Interrupt persistence function
        """
        assert persistence in [
            B.BH1730FVC_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT,
            B.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_MEASUREMENT,
            B.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_2_SAME,
            B.BH1730FVC_INTERRUPT_PERSIST_UPDATE_AFTER_3_SAME,
        ]
        self.set_bit_pattern(R.BH1730FVC_INTERRUPT, persistence,
                             M.BH1730FVC_INTERRUPT_PERSIST_MASK)

    def enable_int_pin(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL,
                             B.BH1730FVC_CONTROL_ADC_INTR_ACTIVE,
                             M.BH1730FVC_CONTROL_ADC_INTR_MASK)
        self.set_bit_pattern(R.BH1730FVC_CONTROL,
                             B.BH1730FVC_CONTROL_ONE_TIME_CONTINOUS,
                             M.BH1730FVC_CONTROL_ONE_TIME_MASK)
        self.set_bit_pattern(R.BH1730FVC_INTERRUPT,
                             B.BH1730FVC_INTERRUPT_INT_EN_VALID,
                             M.BH1730FVC_INTERRUPT_INT_EN_MASK)
        self.set_bit_pattern(R.BH1730FVC_INTERRUPT,
                             B.BH1730FVC_INTERRUPT_INT_STOP_CONTINUOUS,
                             M.BH1730FVC_INTERRUPT_INT_STOP_MASK)

    def disable_int_pin(self):
        self.set_bit_pattern(R.BH1730FVC_CONTROL,
                             B.BH1730FVC_CONTROL_ADC_INTR_INACTIVE,
                             M.BH1730FVC_CONTROL_ADC_INTR_MASK)

    def _write_command(self, command):
        # Commands use the same byte that register addresses normally use.
        # There is no data after the command byte.
        self.write_register(command, [])
