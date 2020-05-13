# The MIT License (MIT)
#
# Copyright (c) 2020 Rohm Semiconductor
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
from kx_lib.kx_util import delay_seconds, bin2uint16
from kx_lib.kx_configuration_enum import CH_ACC, CH_ADP, ACTIVE_LOW, ACTIVE_HIGH
from kx134 import kx134_1211_registers

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

r = kx134_1211_registers.registers()
b = kx134_1211_registers.bits()
m = kx134_1211_registers.masks()
e = kx134_1211_registers.enums()

# activity modes
SLEEP, WAKE = range(2)

# f1_1a, f1_ba, f1_ca, f1_ish, f1_osh
filter1_values = {
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
    'LP_ODR_6p400': (15, 2934914, 2176803, 1, 0),
    'LP_ODR_4p266': (52, 4213708, 2986360, 2, 0),
    'LP_ODR_4p830': (18, 4674381, 3358701, 2, 0),

}

# f2_1a, f2_ba, f2_ish, f2_osh
filter2_values = {
    'LP_ODR_4': (0, 0, 1, 1),
    'LP_ODR_8': (22, 13573, 1, 0),
    'LP_ODR_16': (42, 21895, 2, 0),
    'LP_ODR_32': (56, 26892, 3, 0),
    'LP_ODR_64': (64, 29699, 4, 0),
    'LP_ODR_128': (68, 31198, 5, 0),
    'LP_ODR_256': (71, 31973, 6, 0),
    'LP_ODR_512': (72, 32368, 7, 0),
    'LP_ODR_1024': (72, 32568, 8, 0),
    'LP_ODR_2048': (73, 32668, 9, 0),
    'LP_ODR_8p533': (33, 22481, 2, 0),
    'HP_ODR_4': (0, 0, 1, 1),
    'HP_ODR_8': (53, 13573, 2, 2),
    'HP_ODR_16': (86, 21895, 3, 3),
    'HP_ODR_32': (105, 26892, 4, 4),
    'HP_ODR_40': (109, 27987, 4, 4),
    'HP_ODR_64': (116, 29699, 5, 5),
    'HP_ODR_128': (122, 31198, 6, 6),
    'HP_ODR_256': (125, 31973, 7, 7),
    'HP_ODR_512': (126, 32368, 8, 8),
    'HP_ODR_640': (127, 32448, 8, 8),
    'HP_ODR_1024': (127, 32568, 9, 9),
    'HP_ODR_2048': (0, 32668, 9, 10),
    'HP_ODR_6p400': (77, 19640, 3, 3),
    'HP_ODR_4p413': (59, 15006, 2, 2),
    'HP_ODR_4p266': (57, 14523, 2, 2),
    'HP_ODR_2p844': (30, 7779, 2, 2),
    'HP_ODR_3p938': (52, 13336, 2, 2),
}
## wuf and bts_directions


wufbts_direction = {
    b.KX134_1211_INS3_ZNWU: "FACE_UP",
    b.KX134_1211_INS3_ZPWU: "FACE_DOWN",
    b.KX134_1211_INS3_XNWU: "UP",
    b.KX134_1211_INS3_XPWU: "DOWN",
    b.KX134_1211_INS3_YPWU: "RIGHT",
    b.KX134_1211_INS3_YNWU: "LEFT"}
# for PC1 start delay (acc) calculation

# Note! order of hz entries for KX134
hz = [0.781, 1.563, 3.125, 6.25,
      12.5, 25.0, 50.0, 100.0,
      200.0, 400.0, 800.0, 1600.0,
      3200.0, 6400.0, 12800.0, 25600.0]


class KX134Driver(SensorDriver):
    supported_parts = ['KX134-1211']
    _WAIS = [b.KX134_1211_WHO_AM_I_WAI_ID]

    def __init__(self):
        SensorDriver.__init__(self)
        self.i2c_sad_list = [0x1F, 0x1E, 0x1D, 0x1C]
        self.supported_connectivity = [BUS1_I2C, BUS1_SPI]
        self._default_channel = CH_ACC
        self.int_pins = [1, 2]
        self.name = 'KX134-1211'
        self.axis_mapper = AxisMapper()

    def probe(self):
        """Read sensor ID register and make sure value is expected one. Return 1 if ID is correct."""
        self.connected = True
        resp = self.read_register(r.KX134_1211_WHO_AM_I)
        if resp[0] in self._WAIS:
            self.WHOAMI = resp[0]
            self._registers = dict(r.__dict__)
            self._dump_range = (r.KX134_1211_CNTL1, r.KX134_1211_ADP_CNTL19)
            return 1
        LOGGER.info("wrong KX134 WHOAMI received: 0x%02x" % resp[0])
        self.connected = False
        return 0

    def ic_test(self):  # communication self test
        """verify proper integrated circuit functionality"""
        ctl2 = self.read_register(r.KX134_1211_CNTL2)[0]

        cotr1 = self.read_register(r.KX134_1211_COTR)[0]
        self.write_register(r.KX134_1211_CNTL2, ctl2 | b.KX134_1211_CNTL2_COTC)

        cotr2 = self.read_register(r.KX134_1211_COTR)[0]
        self.write_register(r.KX134_1211_CNTL2, ctl2 & ~b.KX134_1211_CNTL2_COTC)

        if cotr1 == b.KX134_1211_COTR_DCSTR_BEFORE and cotr2 == b.KX134_1211_COTR_DCSTR_AFTER:
            return True
        return False

    def por(self):
        self.write_register(r.KX134_1211_CNTL2, b.KX134_1211_CNTL2_SRST)
        delay_seconds(1)
        LOGGER.debug("POR done")

    def set_power_on(self, channel=CH_ACC | CH_ADP):
        """
        Set operating mode to "operating mode".
        """

        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer and ADP'

        if channel & CH_ACC:
            # When changing PC1 0->1 then 2.0/ODR delay is needed

            # only CH_ACC sets PC1
            self.set_bit(r.KX134_1211_CNTL1, b.KX134_1211_CNTL1_PC1)

            odr_t = 1 / (hz[self.read_register(r.KX134_1211_ODCNTL, 1)[0] &
                            m.KX134_1211_ODCNTL_OSA_MASK]) * 2.0
            if odr_t < 0.1:
                odr_t = 0.1
            delay_seconds(odr_t)

        if channel & CH_ADP:
            self.set_bit(r.KX134_1211_CNTL5, b.KX134_1211_CNTL5_ADPE)

    def set_power_off(self, channel=CH_ACC | CH_ADP):
        """
        Set operating mode to "stand-by".
        """
        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer and ADP'
        self.reset_bit(r.KX134_1211_CNTL1, b.KX134_1211_CNTL1_PC1)

        if channel & CH_ACC:
            # When changing PC1 1->0 then 2.0/ODR delay is needed
            odr_t = 1 / \
                hz[self.read_register(r.KX134_1211_ODCNTL, 1)[0] &
                   m.KX134_1211_ODCNTL_OSA_MASK] * 2.0

            delay_seconds(max(odr_t, 0.1))  # wait at least 0.1 seconds

        if channel & CH_ADP:
            self.reset_bit(r.KX134_1211_CNTL5, b.KX134_1211_CNTL5_ADPE)

    def _read_data(self, channel=CH_ACC | CH_ADP):    # normal data
        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer and ADP'
        s_form = ()
        if channel & CH_ACC:
            data = self.read_register(r.KX134_1211_XOUT_L, 6)
            s_form = s_form + struct.unpack('hhh', data)

        if channel & CH_ADP:
            data = self.read_register(r.KX134_1211_XADP_L, 6)
            s_form = s_form + struct.unpack('hhh', data)

        return s_form

    def read_drdy(self, intpin=1, channel=CH_ACC | CH_ADP):
        assert intpin in self.int_pins
        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer supported'
        return self.read_register(r.KX134_1211_INS2)[0] & b.KX134_1211_INS2_DRDY != 0

    def set_default_on(self):
        """
        2g, 25Hz ODR, high resolution mode, dataready to INT1 latched active low
        """
        self.set_power_off()

        # select ODR
        self.set_odr(b.KX134_1211_ODCNTL_OSA_25)  # default for basic applications

        # select g-range
        self.set_range(b.KX134_1211_CNTL1_GSEL_8G)

        # high resolution mode
        self.set_bit(r.KX134_1211_CNTL1, b.KX134_1211_CNTL1_RES)

        # interrupt settings
        self.enable_drdy(intpin=1)                          # drdy to INT1
        self.reset_bit(r.KX134_1211_CNTL1, b.KX134_1211_INC1_IEL1)    # latched interrupt
        self.reset_bit(r.KX134_1211_INC1, b.KX134_1211_INC1_IEA1)     # active low
        self.set_bit(r.KX134_1211_INC1, b.KX134_1211_INC1_IEN1)       # interrupt 1 set

        # power on sensor
        self.set_power_on()
        self.release_interrupts()                       # clear all interrupts

    def enable_drdy(self, intpin=1, channel=CH_ACC | CH_ADP):
        """enables and routes dataready, but not enable physical interrupt"""
        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer supported'
        assert intpin in self.int_pins
        self.set_bit(r.KX134_1211_CNTL1, b.KX134_1211_CNTL1_DRDYE)
        if intpin == 1:

            # data ready to int1
            self.set_bit(r.KX134_1211_INC4, b.KX134_1211_INC4_DRDYI1)
        else:

            # data ready to int2
            self.set_bit(r.KX134_1211_INC6, b.KX134_1211_INC6_DRDYI2)

    def disable_drdy(self, intpin=1, channel=CH_ACC | CH_ADP):
        """disables and routes dataready, but not enable physical interrupt"""
        assert channel > 0 and channel & (CH_ACC | CH_ADP) == channel, 'only accelerometer and temperature supported'
        assert intpin in self.int_pins
        self.reset_bit(r.KX134_1211_CNTL1, b.KX134_1211_CNTL1_DRDYE)
        if intpin == 1:

            # remove drdy to int1 routing
            self.reset_bit(r.KX134_1211_INC4, b.KX134_1211_INC4_DRDYI1)
        else:

            # remove drdy to int2 routing
            self.reset_bit(r.KX134_1211_INC6, b.KX134_1211_INC6_DRDYI2)

    def set_odr(self, odr, channel=CH_ACC):
        # NOTE odr is either KX134_ADP_CNTL1_OADP_* or KX134_ODCNTL_OSA_*! not int or float value of ODR
        assert channel == CH_ACC or channel == CH_ADP, 'Only ACC and ADP channels supported. One channel at time'

        if channel == CH_ACC:
            assert odr in e.KX134_1211_ODCNTL_OSA.values()
            self.set_bit_pattern(r.KX134_1211_ODCNTL, odr,
                                 m.KX134_1211_ODCNTL_OSA_MASK)
        elif channel == CH_ADP:
            assert odr in e.KX134_1211_ADP_CNTL1_OADP.values()
            self.set_bit_pattern(r.KX134_1211_ADP_CNTL1, odr,
                                 m.KX134_1211_ADP_CNTL1_OADP_MASK)

    def set_range(self, range, channel=CH_ACC):
        assert channel == CH_ACC, 'only accelerometer and temperature supported'
        self.set_bit_pattern(r.KX134_1211_CNTL1, range, m.KX134_1211_CNTL1_GSEL_MASK)

    def set_interrupt_polarity(self, intpin=1, polarity=ACTIVE_LOW):
        assert intpin in self.int_pins
        assert polarity in [ACTIVE_LOW, ACTIVE_HIGH]

        if intpin == 1:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX134_1211_INC1, b.KX134_1211_INC1_IEA1)  # active low
            else:
                self.set_bit(r.KX134_1211_INC1, b.KX134_1211_INC1_IEA1)  # active high
        else:
            if polarity == ACTIVE_LOW:
                self.reset_bit(r.KX134_1211_INC5, b.KX134_1211_INC5_IEA2)  # active low
            else:
                self.set_bit(r.KX134_1211_INC5, b.KX134_1211_INC5_IEA2)  # active high

    def set_average(self, average, channel=CH_ACC):  # set averaging (only for low power)
        assert channel == CH_ACC or channel == CH_ADP

        if channel == CH_ACC:
            assert average in e.KX134_1211_LP_CNTL1_AVC.values(), \
                'Invalid value for KX134_LP_CNTL1_AVC'
            self.set_bit_pattern(r.KX134_1211_LP_CNTL1, average,
                                 m.KX134_1211_LP_CNTL1_AVC_MASK)

        elif channel == CH_ADP:
            assert average in list(e.KX134_1211_ADP_CNTL1_RMS_AVC.values()) + [None],\
                'Invalid value for KX134_ADP_CNTL1_RMS_AVC'

            if average is None:
                # Route ADP data before RMS block to XADP, YADP, ZADP
                self.reset_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_RMS_OSEL)
            else:
                # Route ADP data after RMS block to XADP, YADP, ZADP
                self.set_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_RMS_OSEL)
                self.set_bit_pattern(r.KX134_1211_ADP_CNTL1, average,
                                     m.KX134_1211_ADP_CNTL1_RMS_AVC_MASK)

    def set_BW(self, lpro=b.KX134_1211_ODCNTL_LPRO, _=0, channel=CH_ACC):
        assert lpro in e.KX134_1211_ODCNTL_LPRO, 'valid lpro values are %s' % e.KX134_1211_ODCNTL_LPRO.keys()
        assert channel == CH_ACC, 'only accelerometer supported'
        self.set_bit_pattern(r.KX134_1211_ODCNTL,
                             e.KX134_1211_ODCNTL_LPRO[lpro],
                             m.KX134_1211_ODCNTL_LPRO_MASK)

    def set_adp_filter1(self, f1_value=None):
        assert (f1_value in list(filter1_values.keys())
                + [None]), 'Invalid value for f1_value'
        if f1_value is None:
            self.set_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_FLT1_BYP)
            return

        self.reset_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_FLT1_BYP)

        values = filter1_values[f1_value]
        f1_1a, f1_ba, f1_ca, f1_ish, f1_osh = values
        # Separate reg writes for stream config
        self.write_register(r.KX134_1211_ADP_CNTL3, f1_1a)
        self.write_register(r.KX134_1211_ADP_CNTL4, f1_ba & 255)
        self.write_register(r.KX134_1211_ADP_CNTL5, (f1_ba >> 8) & 255)
        self.write_register(r.KX134_1211_ADP_CNTL6, (f1_ba >> 16) & 255)
        self.write_register(r.KX134_1211_ADP_CNTL7, f1_ca & 255)
        self.write_register(r.KX134_1211_ADP_CNTL8, (f1_ca >> 8) & 255)
        self.write_register(r.KX134_1211_ADP_CNTL9, (f1_ca >> 16) & 255)
        self.write_register(r.KX134_1211_ADP_CNTL10, f1_ish)

        # NOTE: multiwrite not supported for stream configs
        # self.write_register(r.KX134_1211_ADP_CNTL3, [
        #     f1_1a,
        #     f1_ba & 255, (f1_ba >> 8) & 255, (f1_ba >> 16) & 255,
        #     f1_ca & 255, (f1_ca >> 8) & 255, (f1_ca >> 16) & 255,
        #     f1_ish
        # ])
        self.set_bit_pattern(r.KX134_1211_ADP_CNTL11, f1_osh <<
                             7, b.KX134_1211_ADP_CNTL11_ADP_F1_OSH)

    def set_adp_filter2(self, f2_value=None):
        assert (f2_value in list(filter2_values.keys())
                + [None]), 'Invalid value for f2_value'
        if f2_value is None:
            self.set_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_FLT2_BYP)
            return

        self.reset_bit(r.KX134_1211_ADP_CNTL2, b.KX134_1211_ADP_CNTL2_ADP_FLT2_BYP)

        if f2_value.startswith('LP'):
            self.reset_bit(r.KX134_1211_ADP_CNTL2,
                           b.KX134_1211_ADP_CNTL2_ADP_F2_HP)

        else:
            self.set_bit(r.KX134_1211_ADP_CNTL2,
                         b.KX134_1211_ADP_CNTL2_ADP_F2_HP)

        values = filter2_values[f2_value]
        f2_1a, f2_ba, f2_ish, f2_osh = values
        # Separate reg writes for stream config
        self.write_register(r.KX134_1211_ADP_CNTL12, f2_ba & 255)
        self.write_register(r.KX134_1211_ADP_CNTL13, (f2_ba >> 8) & 255)
        self.write_register(r.KX134_1211_ADP_CNTL18, f2_ish)
        self.write_register(r.KX134_1211_ADP_CNTL19, f2_osh)
        # NOTE: multiwrite not supported for stream configs
        # self.write_register(r.KX134_1211_ADP_CNTL12,
        #                     [f2_ba & 255, (f2_ba >> 8) & 255]
        #                     )
        # self.write_register(r.KX134_1211_ADP_CNTL18,
        #                     [f2_ish, f2_osh]
        #                     )
        self.set_bit_pattern(r.KX134_1211_ADP_CNTL11, f2_1a,
                             m.KX134_1211_ADP_CNTL11_ADP_F2_1A_MASK)

    def release_interrupts(self, intpin=1):
        # Latched interrupt source information is cleared and physical interrupt latched pin is changed to its inactive state.
        assert intpin in self.int_pins
        # NOTE this releases both even asked to release one
        self.read_register(r.KX134_1211_INT_REL)

    def enable_fifo(
            self,
            mode=b.KX134_1211_BUF_CNTL2_BM_STREAM,
            res=b.KX134_1211_BUF_CNTL2_BRES,
            axis_mask=0x03):  # enable buffer with mode and resolution

        assert mode in e.KX134_1211_BUF_CNTL2_BM.values()

        # 8 or 16bit resolution store
        assert res in [b.KX134_1211_BUF_CNTL2_BRES, 0]
        assert axis_mask == 0x03, 'xyz axes must included to buffer storage with KX134'

        if res == b.KX134_1211_BUF_CNTL2_BRES:
            self.set_bit(r.KX134_1211_BUF_CNTL2, b.KX134_1211_BUF_CNTL2_BRES)
        else:
            self.reset_bit(r.KX134_1211_BUF_CNTL2, b.KX134_1211_BUF_CNTL2_BRES)

         # combine two settings in one register write
        self.set_bit_pattern(r.KX134_1211_BUF_CNTL2,
                             b.KX134_1211_BUF_CNTL2_BUFE | mode,
                             m.KX134_1211_BUF_CNTL2_BM_MASK | b.KX134_1211_BUF_CNTL2_BUFE)

    def disable_fifo(self):  # disable buffer
        self.reset_bit(r.KX134_1211_BUF_CNTL2, b.KX134_1211_BUF_CNTL2_BUFE)

    def get_fifo_resolution(self):  # get resolution 0= 8b, >0 = 16b
        if self.read_register(r.KX134_1211_BUF_CNTL2, 1)[0] & b.KX134_1211_BUF_CNTL2_BRES > 0:
            return 1  # 16 bit resulution
        else:
            return 0  # 8 bit resolution

    # NOTE! set watermark as samples
    def set_fifo_watermark_level(self, level, axes=3):
        assert axes in [3], 'only 3 axes possible to store fifo buffer'
        if self.get_fifo_resolution() > 0:
            assert level <= 85, 'Watermark level too high.'    # 16b resolution
        else:
            assert level <= 170, 'Watermark level too high.'    # 8b resolution
        self.write_register(r.KX134_1211_BUF_CNTL1, level)

    def get_fifo_level(self):  # NOTE! get fifo buffer as bytes
        bytes_in_buffer = self.read_register(r.KX134_1211_BUF_STATUS_1, 2)
        bytes_in_buffer[1] = bytes_in_buffer[1] & m.KX134_1211_BUF_STATUS_2_SMP_LEV_H_MASK
        bytes_in_buffer = bin2uint16(bytes_in_buffer)
        return (bytes_in_buffer & 0x3ff)

    def clear_buffer(self):
        self.write_register(r.KX134_1211_BUF_CLEAR, 0xff)

    # select wake or sleep mode manually
    def wake_sleep(self, mode):
        assert mode in [SLEEP, WAKE]
        if mode == WAKE:
            self.set_bit(r.KX134_1211_CNTL5, b.KX134_1211_CNTL5_MAN_WAKE)
            # wait until wake setup bit released
            while self.read_register(r.KX134_1211_CNTL5, 1)[0] & b.KX134_1211_CNTL5_MAN_WAKE != 0:
                pass
            # wait until wake mode valid
            while self.read_register(r.KX134_1211_STATUS_REG, 1)[0] & b.KX134_1211_STATUS_REG_WAKE == 0:
                pass
            return
        elif mode == SLEEP:
            self.set_bit(r.KX134_1211_CNTL5, b.KX134_1211_CNTL5_MAN_SLEEP)
            # wait until sleep setup bit released
            while self.read_register(r.KX134_1211_CNTL5, 1)[0] & b.KX134_1211_CNTL5_MAN_SLEEP != 0:
                pass
            # wait until sleep mode valid
            while self.read_register(r.KX134_1211_STATUS_REG, 1)[0] & b.KX134_1211_STATUS_REG_WAKE > 0:
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
