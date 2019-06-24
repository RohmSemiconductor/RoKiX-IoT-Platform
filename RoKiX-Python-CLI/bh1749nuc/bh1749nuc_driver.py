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
"""Driver for the ROHM BH1749NUC color sensor module."""
import struct
import time

from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger

from . import bh1749nuc_registers
from . import imports  # pylint: disable=unused-import

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

R = bh1749nuc_registers.registers()
B = bh1749nuc_registers.bits()
M = bh1749nuc_registers.masks()
E = bh1749nuc_registers.enums()


class BH1749NUCDriver(SensorDriver):
    _WAI = B.BH1749NUC_MANUFACTURER_ID_MANUFACTURER_ID_ID
    _WAIREG = R.BH1749NUC_MANUFACTURER_ID
    _WAI2 = B.BH1749NUC_SYSTEM_CONTROL_PART_ID_ID
    _WAIREG2 = R.BH1749NUC_SYSTEM_CONTROL
    _WAIREG2MASK = M.BH1749NUC_SYSTEM_CONTROL_PART_ID_MASK
    I2C_SAD_LIST = [0x38, 0x39]
    INT_PINS = [1]

    name = 'BH1749NUC'
    supported_parts = [name]

    def __init__(self):
        SensorDriver.__init__(self)
        # configurations to register_dump()
        self._registers = dict(R.__dict__)
        self._dump_range = (R.BH1749NUC_REGISTER_DUMP_START,
                            R.BH1749NUC_REGISTER_DUMP_END)
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
            resp = self.read_register(self._WAIREG2)
            if resp[0] == self._WAI2:
                return 1

        self.connected = False
        return 0

    def por(self):
        """Reset the chip."""
        self.set_bit_pattern(R.BH1749NUC_SYSTEM_CONTROL,
                             B.BH1749NUC_SYSTEM_CONTROL_SW_RESET_DONE,
                             M.BH1749NUC_SYSTEM_CONTROL_SW_RESET_MASK)

    def ic_test(self):
        """Run a basic register functionality test.

        Read a value, modify it, and write it back. Then read the value
        again and check that the earlier modification is visible.

        Returns:
            bool: Whether the test succeeded or not.
        """
        # ic should be powered on before trying this, otherwise it will fail.
        datain1 = self.read_register(R.BH1749NUC_MODE_CONTROL1)[0]
        self.write_register(R.BH1749NUC_MODE_CONTROL1, (datain1 ^ 0x10))
        datain2 = self.read_register(R.BH1749NUC_MODE_CONTROL1)[0]
        self.write_register(R.BH1749NUC_MODE_CONTROL1, datain1)
        return datain2 == datain1 ^ 0x10

    def set_default_on(self):
        """Setup sensor to be ready for multiple measurements."""
        self.set_measurement_time(B.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_8P333)
        self.set_rgb_gain(B.BH1749NUC_MODE_CONTROL1_RGB_GAIN_1X)
        self.set_ir_gain(B.BH1749NUC_MODE_CONTROL1_IR_GAIN_1X)
        self.disable_int_pin()
        self.start_measurement()
        # this function is used by hello_sensor, needs small delay here to get measurement done before reading
        time.sleep(0.2)

    def _read_data(self, channel=None):
        """Read sensor data.

        Args:
            channel: Unused. Do not set.

        Returns:
            tuple[int,int,int,int,int,int]: Raw data
                (R,G,B,IR,G2,status).
        """
        assert channel is None, 'channel selection is not supported'

        rgb_data_size = 3 * 2  # 16-bit R,G,B registers
        rgb_data = self.read_register(R.BH1749NUC_RED_DATA_LSB, rgb_data_size)
        # 16-bit IR,G2 registers and the 8-bit interrupt register.
        other_data_size = 2 * 2 + 1
        other_data = self.read_register(R.BH1749NUC_IR_DATA_LSB,
                                        other_data_size)
        return struct.unpack('<HHHHHB', rgb_data + other_data)

    def set_power_on(self, channel=None):
        """Powers on component by starting measurement."""
        assert channel is None, 'channel selection is not supported'
        self.start_measurement()

    def set_power_off(self, channel=None):
        """Powers down component by stopping measurement."""
        assert channel is None, 'channel selection is not supported'
        self.stop_measurement()
        self.disable_int_pin_active_state()

    def whoami(self):
        """Get manufacturer ID."""
        return self.read_register(R.BH1749NUC_MANUFACTURER_ID)[0]

    def is_interrupt_enabled(self):
        intr_reg = self.read_register(R.BH1749NUC_INTERRUPT)
        status = intr_reg[0] & M.BH1749NUC_INTERRUPT_INT_ENABLE_MASK
        return status == B.BH1749NUC_INTERRUPT_INT_ENABLE_ENABLE

    def disable_int_pin_active_state(self):
        """Set INT pin to high-impedance mode."""
        self.set_bit_pattern(R.BH1749NUC_SYSTEM_CONTROL,
                             B.BH1749NUC_SYSTEM_CONTROL_INT_RESET,
                             M.BH1749NUC_SYSTEM_CONTROL_INT_RESET_MASK)

    def enable_int_pin(self, intpin=1):
        """Enable interrupt."""
        assert intpin in self.INT_PINS
        self.set_bit_pattern(R.BH1749NUC_INTERRUPT, B.BH1749NUC_INTERRUPT_INT_ENABLE_ENABLE,
                             M.BH1749NUC_INTERRUPT_INT_ENABLE_MASK)

    def disable_int_pin(self, intpin=1):
        """Disable interrupt."""
        assert intpin in self.INT_PINS
        self.set_bit_pattern(R.BH1749NUC_INTERRUPT, B.BH1749NUC_INTERRUPT_INT_ENABLE_DISABLE,
                             M.BH1749NUC_INTERRUPT_INT_ENABLE_MASK)

    def get_measurement_time(self):
        """
        :return B.BH1749_MODE_CONTROL1_ODR_8P333 or B.BH1749_MODE_CONTROL1_ODR_4P167
        """
        con1_reg = self.read_register(R.BH1749NUC_MODE_CONTROL1)
        meas_time = con1_reg[0] & M.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_MASK
        return meas_time

    def set_measurement_time(self, meas_time):
        """
        :param time: Exposure time as in BH1747_MODE_CONTROL1_ODR_*
        """
        assert meas_time in [B.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_28P6,
                             B.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_8P333,
                             B.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_4P167]
        self.set_bit_pattern(R.BH1749NUC_MODE_CONTROL1, meas_time,
                             M.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE_MASK)

    def get_rgb_gain(self):
        reg = self.read_register(R.BH1749NUC_MODE_CONTROL1)[0]
        return reg & M.BH1749NUC_MODE_CONTROL1_RGB_GAIN_MASK

    def set_rgb_gain(self, gain):
        assert gain in [B.BH1749NUC_MODE_CONTROL1_RGB_GAIN_1X,
                        B.BH1749NUC_MODE_CONTROL1_RGB_GAIN_32X]
        self.set_bit_pattern(R.BH1749NUC_MODE_CONTROL1, gain,
                             M.BH1749NUC_MODE_CONTROL1_RGB_GAIN_MASK)

    def get_ir_gain(self):
        """Get the current IR gain.

        Returns:
            int: BH1749NUC_MODE_CONTROL1_IR_GAIN_*
        """
        reg = self.read_register(R.BH1749NUC_MODE_CONTROL1)[0]
        return reg & M.BH1749NUC_MODE_CONTROL1_IR_GAIN_MASK

    def set_ir_gain(self, gain):
        """Set the IR gain.

        Params:
            gain (int): BH1749NUC_MODE_CONTROL1_IR_GAIN_*
        """

        assert gain in [B.BH1749NUC_MODE_CONTROL1_IR_GAIN_1X,
                        B.BH1749NUC_MODE_CONTROL1_IR_GAIN_32X]
        self.set_bit_pattern(R.BH1749NUC_MODE_CONTROL1, gain,
                             M.BH1749NUC_MODE_CONTROL1_IR_GAIN_MASK)

    def read_interrupt_thresholds(self):
        """Read the interrupt thresholds.
        Returns:
            tuple[int, int]: (threshold_high, threshold_low)
        """
        data = self.read_register(R.BH1749NUC_TH_HIGH_LSB, 2 * 2)
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
        self.write_register(R.BH1749NUC_TH_HIGH_LSB, thl)
        self.write_register(R.BH1749NUC_TH_HIGH_MSB, thh)
        self.write_register(R.BH1749NUC_TH_LOW_LSB, tll)
        self.write_register(R.BH1749NUC_TH_LOW_MSB, tlh)

    def get_interrupt_persistence(self):
        reg = self.read_register(R.BH1749NUC_PERSISTENCE)[0]
        return reg & M.BH1749NUC_PERSISTENCE_PERSISTENCE_MASK

    def set_interrupt_persistence(self, psn):
        assert psn in [
            B.BH1749NUC_PERSISTENCE_PERSISTENCE_ACTIVE_AFTER_MEASUREMENT,
            B.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_MEASUREMENT,
            B.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_4_SAME,
            B.BH1749NUC_PERSISTENCE_PERSISTENCE_UPDATE_AFTER_8_SAME,
        ]
        self.set_bit_pattern(R.BH1749NUC_PERSISTENCE, psn,
                             M.BH1749NUC_PERSISTENCE_PERSISTENCE_MASK)

    def get_interrupt_source_channel(self):
        """
        :return: BH1749NUC_INTERRUPT_SOURCE_*
        """
        reg = self.read_register(R.BH1749NUC_INTERRUPT)[0]
        return reg & M.BH1749NUC_INTERRUPT_INT_SOURCE_MASK

    def set_interrupt_source_channel(self, channel):
        """
        :param channel: BH1749NUC_INTERRUPT_SOURCE_*
        """
        assert channel in [B.BH1749NUC_INTERRUPT_INT_SOURCE_RED,
                           B.BH1749NUC_INTERRUPT_INT_SOURCE_GREEN,
                           B.BH1749NUC_INTERRUPT_INT_SOURCE_BLUE]
        self.set_bit_pattern(R.BH1749NUC_INTERRUPT, channel,
                             M.BH1749NUC_INTERRUPT_INT_SOURCE_MASK)

    def start_measurement(self):
        """Write 1 to RGB_EN."""
        self.set_bit_pattern(R.BH1749NUC_MODE_CONTROL2,
                             B.BH1749NUC_MODE_CONTROL2_RGB_EN_ACTIVE,
                             M.BH1749NUC_MODE_CONTROL2_RGB_EN_MASK)

    def stop_measurement(self):
        """Write 0 to RGB_EN."""
        self.set_bit_pattern(R.BH1749NUC_MODE_CONTROL2,
                             B.BH1749NUC_MODE_CONTROL2_RGB_EN_INACTIVE,
                             M.BH1749NUC_MODE_CONTROL2_RGB_EN_MASK)
        self.release_interrupts()

    def read_drdy(self):
        """
        reads VALID-register to see if new data is available
        :return: True/False
        """
        reg = self.read_register(R.BH1749NUC_MODE_CONTROL2)[0]
        drdy = reg & M.BH1749NUC_MODE_CONTROL2_VALID_MASK
        return drdy == B.BH1749NUC_MODE_CONTROL2_VALID_YES

    def interrupt_status(self):
        """
        :return: R.BH1749NUC_INTERRUPT_STATUS_*
        """
        reg = self.read_register(R.BH1749NUC_INTERRUPT)[0]
        return reg & M.BH1749NUC_INTERRUPT_INT_STATUS_MASK

    def release_interrupts(self, intpin=1):
        """Clear interrupt status by reading interrupt status."""
        assert intpin in self.INT_PINS, 'invalid INT pin'
        self.interrupt_status()
