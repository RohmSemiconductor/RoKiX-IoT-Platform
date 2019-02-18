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
from kx_lib.kx_configuration_enum import BUS1_I2C, BUS1_SPI
from kx_lib.kx_sensor_base import SensorDriver, AxisMapper
from kx_lib import kx_logger
from kx_lib.kx_util import delay_seconds, bin2uint16, bin2uint8
from kx_lib.kx_configuration_enum import CH_ACC, CH_TEMP, ACTIVE_LOW, ACTIVE_HIGH
from kx132 import kx132_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)
r = kx132_registers.registers()
b = kx132_registers.bits()
m = kx132_registers.masks()
e = kx132_registers.enums()

# activity modes
SLEEP, WAKE = range(2)

filter1_values = { # FIXME to upper case
    'LP_ODR_4': (22, 0, 1439258, 1, 1),
    'LP_ODR_8': (72, 3954428, 2796203, 2, 0),
    'LP_ODR_16': (117, 6099540, 4815580, 4, 0),
    'LP_ODR_32': (10, 7230041, 6354764, 5, 0),
    'LP_ODR_64': (20, 7807115, 7301172, 7, 0),
    'LP_ODR_128': (25, 8097550, 7826024, 9, 0),
    'LP_ODR_256': (27, 8243038, 8102435, 11, 0),
    'LP_ODR_512': (29, 8315818, 8244280, 13, 0),
    'LP_ODR_1024': (29, 8352212, 8316131, 15, 0),
    'LP_ODR_2048': (30, 8370410, 8352291, 17, 0),
    'LP_ODR_2560': (74, 8374050, 8359542, 18, 0)
}
filter2_values = { # FIXME to upper case
    'LP_ODR_4': (0, 0, 0, 1),
    'LP_ODR_8': (22, 13573, 0, 0),
    'LP_ODR_16': (42, 21895, 1, 0),
    'LP_ODR_32': (56, 26892, 2, 0),
    'LP_ODR_64': (64, 29699, 3, 0),
    'LP_ODR_128': (68, 31198, 4, 0),
    'LP_ODR_256': (71, 31973, 5, 0),
    'LP_ODR_512': (72, 32368, 6, 0),
    'LP_ODR_1024': (72, 32568, 7, 0),
    'LP_ODR_2048': (73, 32668, 8, 0),
    'LP_ODR_2560': (33, 32688, 8, 0),
    'HP_ODR_4': (0, 0, 1, 1),
    'HP_ODR_8': (53, 13573, 2, 2),
    'HP_ODR_16': (86, 21895, 3, 3),
    'HP_ODR_32': (105, 26892, 4, 4),
    'HP_ODR_64': (116, 29699, 5, 5),
    'HP_ODR_128': (122, 31198, 6, 6),
    'HP_ODR_256': (125, 31973, 7, 7),
    'HP_ODR_512': (126, 32368, 8, 8),
    'HP_ODR_1024': (127, 32568, 9, 9),
    'HP_ODR_2048': (128, 32668, 9, 9),
    'HP_ODR_2560': (128, 32668, 10, 10)
}
## wuf and bts_directions


wufbts_direction = { # FIXME to upper case
    b.KX132_INS3_ZNWU: "FACE_UP",
    b.KX132_INS3_ZPWU: "FACE_DOWN",
    b.KX132_INS3_XNWU: "UP",
    b.KX132_INS3_XPWU: "DOWN",
    b.KX132_INS3_YPWU: "RIGHT",
    b.KX132_INS3_YNWU: "LEFT"}
# for PC1 start delay (acc) calculation

# FIXME to upper case
hz = [12.5, 25.0, 50.0, 100.0,
      200.0, 400.0, 800.0, 1600.0,
      0.781, 1.563, 3.125, 6.25,
      3200.0, 6400.0, 12800.0, 25600.0]


class KX132Driver(SensorDriver):
    _WAIS = [b.KX132_WHO_AM_I_WAI_ID, 61]

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x1F, 0x1E, 0x1D, 0x1C]
        self.supported_connectivity = [BUS1_I2C, BUS1_SPI]
        self.int_pins = [1, 2]
        self.name = 'KX132'
        self.axis_mapper = AxisMapper()

    def probe(self):
        """Read sensor ID register and make sure value is expected one. Return 1 if ID is correct."""
        self.connected = True
        resp = self.read_register(r.KX132_WHO_AM_I)
        if resp[0] in self._WAIS:
            self.WHOAMI = resp[0]
            self._registers = dict(r.__dict__)
            self._dump_range = (r.KX132_CNTL1, r.KX132_ADP_CNTL19)
            return 1
        LOGGER.debug("wrong KX132 WHOAMI received: 0x%02x" % resp[0])
        self.connected = False
        return 0

    def ic_test(self):  # communication self test
        """verify proper integrated circuit functionality"""
        ctl2 = self.read_register(r.KX132_CNTL2)[0]

        cotr1 = self.read_register(r.KX132_COTR)[0]
        self.write_register(r.KX132_CNTL2, ctl2 | b.KX132_CNTL2_COTC)

        cotr2 = self.read_register(r.KX132_COTR)[0]
        self.write_register(r.KX132_CNTL2, ctl2 & ~b.KX132_CNTL2_COTC)

        if cotr1 == b.KX132_COTR_DCSTR_BEFORE and cotr2 == b.KX132_COTR_DCSTR_AFTER:
            return True
        return False

    def por(self):
        self.write_register(r.KX132_CNTL2, b.KX132_CNTL2_SRST)
        delay_seconds(1)
        LOGGER.debug("POR done")

    def set_power_on(self, channel=CH_ACC | CH_TEMP):
        """
        Set operating mode to "operating mode".
        """

        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        self.set_bit(r.KX132_CNTL1, b.KX132_CNTL1_PC1)

        if channel & CH_ACC:
            # When changing PC1 0->1 then 1.5/ODR delay is needed
            odr_t = 1 / (hz[self.read_register(r.KX132_ODCNTL, 1)
                            [0] & m.KX132_ODCNTL_OSA_MASK]) * 1.5
            if odr_t < 0.1:
                odr_t = 0.1
            delay_seconds(odr_t)

        if channel & CH_TEMP:
            self.set_bit(r.KX132_CNTL5, b.KX132_CNTL5_TSE)

    def set_power_off(self, channel=CH_ACC | CH_TEMP):
        """
        Set operating mode to "stand-by".
        """
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'

        self.reset_bit(r.KX132_CNTL1, b.KX132_CNTL1_PC1)

        if channel & CH_ACC:
            # When changing PC1 1->0 then 1.5/ODR delay is needed
            odr_t = 1 / \
                hz[self.read_register(r.KX132_ODCNTL, 1)[
                    0] & m.KX132_ODCNTL_OSA_MASK] * 1.5

            delay_seconds(max(odr_t, 0.1))  # wait at least 0.1 seconds
        if channel & CH_TEMP:
            self.reset_bit(r.KX132_CNTL5, b.KX132_CNTL5_TSE)

    def _read_data(self, channel=CH_ACC | CH_TEMP):    # normal data
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        s_form = ()
        if channel & CH_ACC:
            data = self.read_register(r.KX132_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)
        if channel & CH_TEMP:
            data = self.read_register(r.KX132_TEMP_OUT_L, 2)
            s_form = s_form + struct.unpack('h', data)
        return s_form

    def enable_adp(self):
        self.set_bit(r.KX132_CNTL5, b.KX132_CNTL5_ADPE)

    def disable_adp(self):
        self.reset_bit(r.KX132_CNTL5, b.KX132_CNTL5_ADPE)

    def read_adp_data(self, channel=CH_ACC | CH_TEMP):    # adp filtered data
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        s_form = ()
        data = self.read_register(r.KX132_XADP_L, 6)
        s_form = s_form + struct.unpack('hhh', data)
        return s_form

    # accelerometer data + adp filtered data
    def read_combined_adp_data(self, channel=CH_ACC | CH_TEMP):
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        s_form = ()

        data = self.read_register(r.KX132_XOUT_L, 6)
        data2 = self.read_register(r.KX132_XADP_L, 6)
        data3 = self.read_register(r.KX132_TEMP_OUT_L, 2)
        s_form = s_form + struct.unpack('hhh', data)
        s_form = s_form + struct.unpack('hhh', data2)
        s_form = s_form + struct.unpack('h', data3)
        return s_form

    def read_drdy(self, intpin=1, channel=CH_ACC | CH_TEMP):
        assert intpin in self.int_pins
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        return self.read_register(r.KX132_INS2)[0] & b.KX132_INS2_DRDY != 0

    def read_step_count(self):
        data = self.read_register(r.KX132_PED_STP_L, 2)
        return data[0] | data[1] << 8

    def reset_step_count(self):
        # reading step count will reset the register value
        self.read_step_count()

    def set_default_on(self):
        """
        2g, 25Hz ODR, high resolution mode, dataready to INT1 latched active low
        """
        self.set_power_off()

        # select ODR
        self.set_odr(b.KX132_ODCNTL_OSA_25)  # default for basic applications

        # select g-range
        self.set_range(b.KX132_CNTL1_GSEL_2G)

        # high resolution mode
        self.set_bit(r.KX132_CNTL1, b.KX132_CNTL1_RES)

        # interrupt settings
        self.enable_drdy(intpin=1)                      # drdy to INT1
        self.reset_bit(r.KX132_CNTL1, b.KX132_INC1_IEL1)  # latched interrupt
        self.reset_bit(r.KX132_INC1, b.KX132_INC1_IEA1)  # active low
        self.set_bit(r.KX132_INC1, b.KX132_INC1_IEN1)   # interrupt 1 set

        # power on sensor
        self.set_power_on()
        self.release_interrupts()                       # clear all interrupts

    def enable_drdy(self, intpin=1, channel=CH_ACC | CH_TEMP):
        """enables and routes dataready, but not enable physical interrupt"""
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        assert intpin in self.int_pins
        self.set_bit(r.KX132_CNTL1, b.KX132_CNTL1_DRDYE)
        if intpin == 1:

            # data ready to int1
            self.set_bit(r.KX132_INC4, b.KX132_INC4_DRDYI1)
        else:

            # data ready to int2
            self.set_bit(r.KX132_INC6, b.KX132_INC6_DRDYI2)

    def disable_drdy(self, intpin=1, channel=CH_ACC):
        """disables and routes dataready, but not enable physical interrupt"""
        assert channel > 0 and channel & (CH_ACC) == channel, 'only accelerometer and temperature supported'
        assert intpin in self.int_pins
        self.reset_bit(r.KX132_CNTL1, b.KX132_CNTL1_DRDYE)
        if intpin == 1:

            # remove drdy to int1 routing
            self.reset_bit(r.KX132_INC4, b.KX132_INC4_DRDYI1)
        else:

            # remove drdy to int2 routing
            self.reset_bit(r.KX132_INC6, b.KX132_INC6_DRDYI2)

    def set_odr(self, ODCNTL_OSA, channel=CH_ACC):
        assert channel > 0 and channel & (CH_ACC) == channel, 'only accelerometersupported'
        self.set_bit_pattern(r.KX132_ODCNTL, ODCNTL_OSA,
                             m.KX132_ODCNTL_OSA_MASK)

    def set_adp_odr(self, ADP_OADP, channel=CH_ACC): # FIXME use set_odr(channel=CH_ADP)
        assert channel > 0 and channel & (CH_ACC) == channel, 'only accelerometersupported'
        self.set_bit_pattern(r.KX132_ADP_CNTL1, ADP_OADP,
                             m.KX132_ADP_CNTL1_OADP_MASK)

    def set_rms_average(self, average=None, channel=CH_ACC):
        assert channel > 0 and channel & (CH_ACC) == channel, 'only accelerometersupported'
        assert average in list(e.KX132_ADP_CNTL1_RMS_AVC.values()) + [None],\
            'Invalid value for KX132_ADP_CNTL1_RMS_AVC'
        if average is None:
            self.reset_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_RMS_OSEL)
            return
        self.set_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_RMS_OSEL)
        self.set_bit_pattern(r.KX132_ADP_CNTL1, average,
                             m.KX132_ADP_CNTL1_RMS_AVC_MASK)

    def set_adp_filter1(self, f1_value=None):
        assert (f1_value in list(filter1_values.keys())
                + [None]), 'Invalid value for f1_value'
        if f1_value is None:
            self.set_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_FLT1_BYP)
            return

        self.reset_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_FLT1_BYP)

        values = filter1_values[f1_value]
        f1_1a, f1_ba, f1_ca, f1_ish, f1_osh = values
        # Separate reg writes for stream config
        self.write_register(r.KX132_ADP_CNTL3, f1_1a)
        self.write_register(r.KX132_ADP_CNTL4, f1_ba & 255)
        self.write_register(r.KX132_ADP_CNTL5, (f1_ba >> 8) & 255)
        self.write_register(r.KX132_ADP_CNTL6, (f1_ba >> 16) & 255)
        self.write_register(r.KX132_ADP_CNTL7, f1_ca & 255)
        self.write_register(r.KX132_ADP_CNTL8, (f1_ca >> 8) & 255)
        self.write_register(r.KX132_ADP_CNTL9, (f1_ca >> 16) & 255)
        self.write_register(r.KX132_ADP_CNTL10, f1_ish)

        # NOTE: multiwrite not supported for stream configs
        # self.write_register(r.KX132_ADP_CNTL3, [
        #     f1_1a,
        #     f1_ba & 255, (f1_ba >> 8) & 255, (f1_ba >> 16) & 255,
        #     f1_ca & 255, (f1_ca >> 8) & 255, (f1_ca >> 16) & 255,
        #     f1_ish
        # ])
        self.set_bit_pattern(r.KX132_ADP_CNTL11, f1_osh <<
                             7, b.KX132_ADP_CNTL11_ADP_F1_OSH)

    def set_adp_filter2(self, f2_value=None):
        assert (f2_value in list(filter2_values.keys())
                + [None]), 'Invalid value for f2_value'
        if f2_value is None:
            self.set_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_FLT2_BYP)
            return

        self.reset_bit(r.KX132_ADP_CNTL2, b.KX132_ADP_CNTL2_ADP_FLT2_BYP)

        if f2_value.startswith('LP'):
            self.reset_bit(r.KX132_ADP_CNTL2,
                           b.KX132_ADP_CNTL2_ADP_F2_HP)

        else:
            self.set_bit(r.KX132_ADP_CNTL2,
                         b.KX132_ADP_CNTL2_ADP_F2_HP)

        values = filter2_values[f2_value]
        f2_1a, f2_ba, f2_ish, f2_osh = values
        # Separate reg writes for stream config
        self.write_register(r.KX132_ADP_CNTL12, f2_ba & 255)
        self.write_register(r.KX132_ADP_CNTL13, (f2_ba >> 8) & 255)
        self.write_register(r.KX132_ADP_CNTL18, f2_ish)
        self.write_register(r.KX132_ADP_CNTL19, f2_osh)
        # NOTE: multiwrite not supported for stream configs
        # self.write_register(r.KX132_ADP_CNTL12,
        #                     [f2_ba & 255, (f2_ba >> 8) & 255]
        #                     )
        # self.write_register(r.KX132_ADP_CNTL18,
        #                     [f2_ish, f2_osh]
        #                     )
        self.set_bit_pattern(r.KX132_ADP_CNTL11, f2_1a,
                             m.KX132_ADP_CNTL11_ADP_F2_1A_MASK)

    def set_range(self, range, _=0, channel=CH_ACC | CH_TEMP):
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        self.set_bit_pattern(r.KX132_CNTL1, range, m.KX132_CNTL1_GSEL_MASK)

    def set_interrupt_polarity(self, intpin=1, polarity=ACTIVE_LOW):
        assert intpin in self.int_pins
        assert polarity in [ACTIVE_LOW, ACTIVE_HIGH]

        if intpin == 1:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX132_INC1, b.KX132_INC1_IEA1)  # active low
            else:
                self.set_bit(r.KX132_INC1, b.KX132_INC1_IEA1)  # active high
        else:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX132_INC5, b.KX132_INC5_IEA2)  # active low
            else:
                self.set_bit(r.KX132_INC5, b.KX132_INC5_IEA2)  # active high

    def set_average(self, average, _=0, channel=CH_ACC | CH_TEMP):  # set averaging (only for low power)
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        assert average in e.KX132_LP_CNTL1_AVC.values(), 'Invalid value for KX022_LP_CNTL1_AVC'
        self.set_bit_pattern(r.KX132_LP_CNTL1, average,
                             m.KX132_LP_CNTL1_AVC_MASK)

    def set_BW(self, lpro=b.KX132_ODCNTL_LPRO, _=0, channel=CH_ACC | CH_TEMP):
        assert channel > 0 and channel & (CH_ACC | CH_TEMP) == channel, 'only accelerometer and temperature supported'
        assert lpro in [b.KX132_ODCNTL_LPRO, 0]
        if lpro:
            self.set_bit(r.KX132_ODCNTL, b.KX132_ODCNTL_LPRO)   # BW odr /2
        else:
            # BW odr /9 (default)
            self.reset_bit(r.KX132_ODCNTL, b.KX132_ODCNTL_LPRO)

    def enable_iir(self):
        self.reset_bit(r.KX132_ODCNTL, b.KX132_ODCNTL_IIR_BYPASS)

    def disable_iir(self):
        self.set_bit(r.KX132_ODCNTL, b.KX132_ODCNTL_IIR_BYPASS)

    def release_interrupts(self, intpin=1):
        # Latched interrupt source information is cleared and physical interrupt latched pin is changed to its inactive state.
        assert intpin in self.int_pins
        # NOTE this releases both even asked to release one
        self.read_register(r.KX132_INT_REL)

    def enable_fifo(
            self,
            mode=b.KX132_BUF_CNTL2_BM_STREAM,
            res=b.KX132_BUF_CNTL2_BRES,
            axis_mask=0x03):  # enable buffer with mode and resolution
        # syncronized with KXxxx, KXG03
        assert mode in e.KX132_BUF_CNTL2_BM.values()

        # 8 or 16bit resolution store
        assert res in [b.KX132_BUF_CNTL2_BRES, 0]
        assert axis_mask == 0x03, 'all axis must included to buffer storage with KXx2x'

        if res == b.KX132_BUF_CNTL2_BRES:
            self.set_bit(r.KX132_BUF_CNTL2, b.KX132_BUF_CNTL2_BRES)
        else:
            self.reset_bit(r.KX132_BUF_CNTL2, b.KX132_BUF_CNTL2_BRES)

         # combine two settings in one register write
        self.set_bit_pattern(r.KX132_BUF_CNTL2,
                             b.KX132_BUF_CNTL2_BUFE | mode,
                             m.KX132_BUF_CNTL2_BM_MASK | b.KX132_BUF_CNTL2_BUFE)

    def disable_fifo(self):  # disable buffer
        self.reset_bit(r.KX132_BUF_CNTL2, b.KX132_BUF_CNTL2_BUFE)

    def get_fifo_resolution(self):  # get resolution 0= 8b, >0 = 16b
        if self.read_register(r.KX132_BUF_CNTL2, 1)[0] & b.KX132_BUF_CNTL2_BRES > 0:
            return 1  # 16 bit resulution
        else:
            return 0  # 8 bit resolution

    # NOTE! set watermark as samples
    def set_fifo_watermark_level(self, level, axes=3):
        assert axes in [3], 'only 3 axes possible to store fifo buffer'
        if self.get_fifo_resolution() > 0:
            assert level <= 0x154, 'Watermark level too high.'    # 16b resolution
        else:
            assert level <= 0x2A8, 'Watermark level too high.'    # 8b resolution
        lsb = level & 0xff
        msb = level >> 8
        self.write_register(r.KX132_BUF_CNTL1, lsb)
        self.set_bit_pattern(r.KX132_BUF_CNTL2,
                             msb << 2,
                             m.KX132_BUF_CNTL2_SMP_TH_H_MASK)

    # set pedometer watermark
    def set_pedometer_watermark(self, level):
        # PED_STPWML, PED_STPWMH pedometer watermark threshold
        msb = level >> 8
        lsb = level & 0x00ff
        self.write_register(r.KX132_PED_STPWM_L, lsb)
        self.write_register(r.KX132_PED_STPWM_H, msb)

    def get_fifo_level(self):  # NOTE! get fifo buffer as bytes
        bytes_in_buffer = self.read_register(r.KX132_BUF_STATUS_1, 2)
        bytes_in_buffer = bin2uint16(bytes_in_buffer)
        return (bytes_in_buffer & 0x7ff)

    def clear_buffer(self):
        self.write_register(r.KX132_BUF_CLEAR, 0xff)

    # select wake or sleep mode manually
    def wake_sleep(self, mode):
        assert mode in [SLEEP, WAKE]
        if mode == WAKE:
            self.set_bit(r.KX132_CNTL5, b.KX132_CNTL5_MAN_WAKE)
            # wait until wake setup bit released
            while self.read_register(r.KX132_CNTL5, 1)[0] & b.KX132_CNTL5_MAN_WAKE != 0:
                pass
            # wait until wake mode valid
            while self.read_register(r.KX132_STATUS_REG, 1)[0] & b.KX132_STATUS_REG_WAKE == 0:
                pass
            return
        elif mode == SLEEP:
            self.set_bit(r.KX132_CNTL5, b.KX132_CNTL5_MAN_SLEEP)
            # wait until sleep setup bit released
            while self.read_register(r.KX132_CNTL5, 1)[0] & b.KX132_CNTL5_MAN_SLEEP != 0:
                pass
            # wait until sleep mode valid
            while self.read_register(r.KX132_STATUS_REG, 1)[0] & b.KX132_STATUS_REG_WAKE > 0:
                pass
            return
        assert 0, "wrong wake/sleep mode"


def directions(dir):            # print wuf+bts source directions
    fst = True
    pos = ""
    for i in range(0, 6):
        mask = 0x01 << i
        if dir & mask > 0:
            if not fst:
                pos = pos + "+" + wufbts_direction[dir & mask]
            else:
                pos = wufbts_direction[dir & mask]
                fst = False
    return pos
