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
import struct
from . import imports  # pylint: disable=unused-import
from kx_lib.kx_configuration_enum import BUS1_I2C
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger
from kx_lib.kx_util import delay_seconds, bin2uint16
from kx_lib.kx_configuration_enum import CH_ACC, CH_MAG, CH_TEMP
from kx_lib.kx_exception import EvaluationKitException
from kmx64 import kmx64_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

r = kmx64_registers.registers()
b = kmx64_registers.bits()
m = kmx64_registers.masks()
e = kmx64_registers.enums()

# for acc power on delay calculation
hz = [12.5, 25.0, 50.0, 100.0, 200.0, 400.0, 800.0, 1600.0, 0.781, 1.563, 3.125, 6.25, 25600.0, 25600.0, 25600.0, 25600.0]


class KMX64Driver(SensorDriver):
    _WAIS_KMX64 = [0x41]

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x0E, 0x0F]
        self.supported_connectivity = [BUS1_I2C]
        self.int_pins = [1, 2]
        self.name = 'KMX64'

        # configurations to register_dump()
        self._registers = dict(r.__dict__)
        self._dump_range = (r.KMX64_INC1, r.KMX64_BUF_CTRL_3)

    def probe(self):
        """
        Read sensor ID register and make sure value is expected one. Return 1 if ID is correct.
        """
        self.connected = True
        resp = self.read_register(r.KMX64_WHO_AM_I)
        LOGGER.info('Who am I value received {}'.format(resp[0]))
        if resp[0] in self._WAIS_KMX64:
            self.WHOAMI = resp[0]
            LOGGER.info('KMX64 found')
            return 1
        elif resp[0] in self._WAIS_KMX64:
            self.WHOAMI = resp[0]
            LOGGER.info('KMX64 found')
            self.name = 'KMX64'
            return 1

        LOGGER.debug("wrong WHOAMI received for KMX64/65: 0x%02x" % resp[0])
        self.connected = False
        return 0

    def ic_test(self):
        """ Verify proper integrated circuit functionality. """
        cotr1 = self.read_register(r.KMX64_COTR)[0]

        self.write_register(r.KMX64_CNTL1, b.KMX64_CNTL1_COTC)

        cotr2 = self.read_register(r.KMX64_COTR)[0]
        if cotr1 == 0x55 and cotr2 == 0xaa:
            return True
        LOGGER.error('cotr1=0x%02x, cotr2=0x%02x' % (cotr1, cotr2))
        return False

    def por(self):
        """ Initiate software reset (reset without cutting voltage supply or ground wires). """
        self.write_register(r.KMX64_CNTL1, b.KMX64_CNTL1_SRST)
        delay_seconds(1)
        LOGGER.debug("POR done")

    def set_power_on(self, channel=CH_ACC):
        assert channel & (CH_ACC | CH_MAG | CH_TEMP) == channel
        if channel & CH_ACC > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_ACCEL_EN_OPERATING_MODE,
                                 m.KMX64_CNTL2_ACCEL_EN_MASK)

            # When setting power on; 0->1 then 1.5/ODR delay is needed for acc
            odr_t = 1 / (hz[self.read_register(r.KMX64_ODCNTL, 1)[0] & m.KMX64_ODCNTL_OSA_MASK])
            if odr_t < 0.1:
                odr_t = 0.1
            delay_seconds(odr_t)

        if channel & CH_MAG > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_MAG_EN_OPERATING_MODE,
                                 m.KMX64_CNTL2_MAG_EN_MASK)

        if channel & CH_TEMP > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_TEMP_EN_OPERATING_MODE,
                                 m.KMX64_CNTL2_TEMP_EN_MASK)

    def set_power_off(self, channel=CH_ACC | CH_MAG | CH_TEMP):
        assert channel & (CH_ACC | CH_MAG | CH_TEMP) == channel
        if channel & CH_ACC > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_ACCEL_EN_STANDBY_MODE,
                                 m.KMX64_CNTL2_ACCEL_EN_MASK)

        if channel & CH_MAG > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_MAG_EN_STANDBY_MODE,
                                 m.KMX64_CNTL2_MAG_EN_MASK)

        if channel & CH_TEMP > 0:
            self.set_bit_pattern(r.KMX64_CNTL2,
                                 b.KMX64_CNTL2_TEMP_EN_STANDBY_MODE,
                                 m.KMX64_CNTL2_TEMP_EN_MASK)

    def _read_data(self, channel=CH_ACC | CH_MAG):
        """ Read measurement results from registers. """
        assert channel & (CH_ACC | CH_MAG | CH_TEMP) == channel
        s_form = ()
        if channel & CH_ACC > 0:
            data = self.read_register(r.KMX64_ACCEL_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        if channel & CH_MAG > 0:
            data = self.read_register(r.KMX64_MAG_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        if channel & CH_TEMP > 0:
            data = self.read_register(r.KMX64_TEMP_OUT_L, 2)
            s_form = s_form + struct.unpack('h', data)
        return s_form

    def read_drdy(self, channel=CH_ACC):  # separately followed
        """ Read data ready register. """
        ins1 = self.read_register(r.KMX64_INS1)[0]
        if channel & CH_ACC > 0:
            return ins1 & b.KMX64_INS1_DRDY_A_AVAILABLE != 0
        if channel & CH_MAG > 0:
            return ins1 & b.KMX64_INS1_DRDY_M_AVAILABLE != 0
        raise EvaluationKitException('Invalid channel number %d' % channel)

    def set_default_on(self):
        """ ACC+MAG+temp: 2g, 25hz, high resolution,dataready to INT1 latched, active low """

        # ODR acc+mag
        self.set_odr(b.KMX64_ODCNTL_OSA_25, CH_ACC)
        self.set_odr(b.KMX64_ODCNTL_OSM_25, CH_MAG)

        # set g-range, enable acc+mag+temp
        self.set_range(b.KMX64_CNTL2_GSEL_2G, CH_ACC)

        # set mag -range
        self.set_range(b.KMX64_CNTL1_MFSSEL_1200UT, CH_MAG)

        # power mode, select high or low resolution setup
        self.set_average(b.KMX64_CNTL2_RES_MAX2)  # high res

        # interrupts and data ready settings
        self.write_register(r.KMX64_INC3,
                            b.KMX64_INC3_IEL1_LATCHED |
                            b.KMX64_INC3_IEA1_LOW)
        self.enable_drdy(1, CH_ACC)

        # enable acc+mag+temp
        self.set_power_on(CH_ACC | CH_MAG | CH_TEMP)

    def set_odr(self, ODR, channel=CH_ACC):           # set separately for acc or mag
        """ Setup output data rate. """
        assert channel in [CH_ACC, CH_MAG]
        if channel & CH_ACC:
            self.set_bit_pattern(r.KMX64_ODCNTL, ODR, m.KMX64_ODCNTL_OSA_MASK)
        elif channel & CH_MAG:
            self.set_bit_pattern(r.KMX64_ODCNTL, ODR, m.KMX64_ODCNTL_OSM_MASK)

    def set_range(self, range, channel=CH_ACC):
        assert channel in [CH_ACC, CH_MAG]
        if channel & CH_ACC > 0:
            assert range in [b.KMX64_CNTL2_GSEL_2G, b.KMX64_CNTL2_GSEL_4G, b.KMX64_CNTL2_GSEL_8G, b.KMX64_CNTL2_GSEL_16G]
            self.set_bit_pattern(r.KMX64_CNTL2, range, m.KMX64_CNTL2_GSEL_MASK)

        if channel & CH_MAG > 0:
            assert range in [b.KMX64_CNTL1_MFSSEL_1200UT, b.KMX64_CNTL1_MFSSEL_800UT]
            self.set_bit_pattern(r.KMX64_CNTL1, range, m.KMX64_CNTL1_MFSSEL_MASK)

    def set_average(self, average, channel=CH_ACC):
        assert channel == CH_ACC
        assert average in [b.KMX64_CNTL2_RES_MAX1, b.KMX64_CNTL2_RES_MAX2,
                           b.KMX64_CNTL2_RES_A4M2, b.KMX64_CNTL2_RES_A32M16]
        self.set_bit_pattern(r.KMX64_CNTL2, average, m.KMX64_CNTL2_RES_MASK)

    def enable_drdy(self, intpin=1, channel=CH_ACC):    # set separately for acc or mag
        assert channel in [CH_ACC, CH_MAG]
        assert intpin in self.int_pins
        if channel & CH_ACC > 0:
            if intpin == 1:
                self.set_bit(r.KMX64_INC1, b.KMX64_INC1_DRDY_A1)
            else:
                self.set_bit(r.KMX64_INC2, b.KMX64_INC2_DRDY_A2)
        if channel & CH_MAG > 0:
            if intpin == 1:
                self.set_bit(r.KMX64_INC1, b.KMX64_INC1_DRDY_M1)
            else:
                self.set_bit(r.KMX64_INC2, b.KMX64_INC2_DRDY_M2)

    def disable_drdy(self, intpin=1, channel=CH_ACC):   # set separately for acc or mag
        assert channel in [CH_ACC, CH_MAG]
        assert intpin in self.int_pins
        if channel & CH_ACC > 0:
            if intpin == 1:
                self.reset_bit(r.KMX64_INC1, b.KMX64_INC1_DRDY_A1)
            else:
                self.reset_bit(r.KMX64_INC2, b.KMX64_INC2_DRDY_A2)
        if channel & CH_MAG > 0:
            if intpin == 1:
                self.reset_bit(r.KMX64_INC1, b.KMX64_INC1_DRDY_M1)
            else:
                self.reset_bit(r.KMX64_INC2, b.KMX64_INC2_DRDY_M2)

    def release_interrupts(self):
        """ Clear interrupts. """
        self.read_register(r.KMX64_INL)

    def enable_fifo(self, mode=b.KMX64_BUF_CTRL_2_BUF_M_STREAM, res=None, axis_mask=0x7f):
        """ Enable fifo with mode and axis mask """
        assert mode in [b.KMX64_BUF_CTRL_2_BUF_M_STREAM,
                        b.KMX64_BUF_CTRL_2_BUF_M_FIFO,
                        b.KMX64_BUF_CTRL_2_BUF_M_TRIGGER,
                        b.KMX64_BUF_CTRL_2_BUF_M_FILO]
        assert res in [16, None], 'buffer storage resolution is 16b only'
        assert axis_mask < 0x80, 'axis mask for buffer storage is too big'
        self.set_bit_pattern(r.KMX64_BUF_CTRL_2,
                             mode,
                             m.KMX64_BUF_CTRL_2_BUF_M_MASK)         # mode
        self.write_register(r.KMX64_BUF_CTRL_3, axis_mask & 0x7f)   # axis masks
        self.clear_buffer()                                       # just in case

    def disable_fifo(self):
        self.write_register(r.KMX64_BUF_CTRL_3, 0x00)

    def set_fifo_watermark_level(self, level, axes=6):  # informed as samples in ODR
        """ set fifo watermark level in bytes """
        assert level < 512, 'Watermark level too high.'
        assert axes < 8
        lsb = level & 0xff
        msb = level >> 8
        self.write_register(r.KMX64_BUF_CTRL_1, lsb)
        self.set_bit_pattern(r.KMX64_BUF_CTRL_2,
                             msb,
                             b.KMX64_BUF_CTRL_2_SMT_TH8)

    def get_fifo_level(self):   # informs as data bytes !!!
        count = self.read_register(r.KMX64_BUF_STATUS_1, 2)
        count = bin2uint16(count)
        count = count & 0x03ff
        return count

    def clear_buffer(self):
        self.write_register(r.KMX64_BUF_CLEAR, 0)
