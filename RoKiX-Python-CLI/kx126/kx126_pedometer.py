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
"""
KX126 pedometer
"""
import imports  # pylint: disable=unused-import
from kx126 import kx126_pedometer_params
from kx126.kx126_driver import KX126Driver, r, b, m, e
from kx_lib.kx_data_logger import SingleChannelEventReader
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import evkit_config, get_other_pin_index, convert_to_enumkey
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY
from kx_lib import kx_logger

# Example application for basic pedometer step counting
###
# Pedometer uses interrupts int1 for the step event and int2 for the watermark event
###
# Pedometer outputs
##
# ins1, STPOVI = step overflow event
# ins1, STPWMI = step watermark event
# ins2, STPINCI = step counter increment event

_CODE_FORMAT_VERSION = 3.0


LOGGER = kx_logger.get_logger(__name__)


class KX126PedometerStream(StreamConfig):
    fmt = "<BBBBBBB"
    hdr = "ch!ins1!ins2!ins3!stat!N/A!rel"
    reg = r.KX126_INS1

    def __init__(self, sensors, pin_index=2, timer=None):
        assert sensors[0].name in KX126Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])
        assert not timer, 'Timer not supported in this data stream'

        # get pin_index if it is not given and timer is not used
        if pin_index is None and timer is None:
            pin_index = get_other_pin_index()

        assert pin_index in [1, 2], 'got %s' % pin_index

        # define the data stream
        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index)


def set_pedometer_parameters(sensor, cfg):
    # PED_CNTL1
    # STP_TH; first accepted step count level = default 8 (0x4)
    # MAG_SCALE; signal scaling = default 6
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, cfg.STP_TH, m.KX126_PED_CNTL1_STP_TH_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL1, cfg.MAG_SCALE, m.KX126_PED_CNTL1_MAG_SCALE_MASK)

    # PED_CNTL2
    # HPS; Scaling factor for the output from the high-pass filter = default 3
    # LP_LEN; The length of the low-pass filter = default 100Hz (0x0c)
    # default 03 changed due 8g mode in asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, cfg.HPS, m.KX126_PED_CNTL2_HPS_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL2, cfg.LP_LEN, m.KX126_PED_CNTL2_PED_ODR_MASK)

    # PED_CNTL3
    # FCB; Scaling factors inside the high-pass filter = default 0x01, changed due to the 8g mode in the asic
    # FCA; Default 0x0E, changed due to the 8g mode in the asic
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, cfg.FCB, m.KX126_PED_CNTL3_FCB_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL3, cfg.FCA, m.KX126_PED_CNTL3_FCA_MASK)

    # PED_CNTL4
    # B_CNT; Samples below the zero threshold before setting = default 0x1
    # A_H; Maximum area of the peak (maximum impact from the floor) = default 0x0F
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, cfg.B_CNT, m.KX126_PED_CNTL4_B_CNT_MASK)
    sensor.set_bit_pattern(r.KX126_PED_CNTL4, cfg.A_H, m.KX126_PED_CNTL4_A_H_MASK)

    # PED_CNTL5
    # A_L; Minimum area of the peak (minimum impact from the floor) = default 0x3C
    sensor.write_register(r.KX126_PED_CNTL5, cfg.A_L)

    # PED_CNTL6
    # M_H; maximum time interval for the peak = default 0x14
    sensor.write_register(r.KX126_PED_CNTL6, cfg.M_H)

    # PED_CNTL7
    # M_L         - minimum time interval for the peak = default 0x06
    sensor.write_register(r.KX126_PED_CNTL7, cfg.M_L)

    # PED_CNTL8
    # T_L         - time window for noise and delay time = default 0x05
    sensor.write_register(r.KX126_PED_CNTL8, cfg.T_L)

    # PED_CNTL9
    # T_M         - time interval to prevent overflowing = default 0x16
    sensor.write_register(r.KX126_PED_CNTL9, cfg.T_M)

    # PED_CNTL10
    # T_P         - minimum time interval for a single stride = default 0x13
    sensor.write_register(r.KX126_PED_CNTL10, cfg.T_P)

# enable measurement and pedometer logger


def enable_pedometer(sensor,
                     odr=100,
                     cfg=kx126_pedometer_params.Pedometer_parameters_odr_100,
                     avg='16_SAMPLE_AVG',
                     power_off_on=True):

    LOGGER.info('Pedometer step counting init start')
    assert sensor.name in KX126Driver.supported_parts

    assert odr in [50, 100]

    assert avg in e.KX126_LP_CNTL_AVC.keys(), \
        'Invalid lp_average value "{}". Valid values are {}'.format(
            avg, e.KX126_LP_CNTL_AVC.keys())

    if power_off_on:
        sensor.set_power_off()

    # set watermark interrupt level
    # sensor.set_pedometer_watermark(0x14)
    # "disable" watermark
    sensor.set_pedometer_watermark(0xffff)

    if odr == 50:
        cfg = kx126_pedometer_params.Pedometer_parameters_odr_50
        # run pedometer with 50Hz ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_50, m.KX126_PED_CNTL2_PED_ODR_MASK)
    else:  # run pedometer with 100Hz or higher ODR
        sensor.set_bit_pattern(r.KX126_PED_CNTL2, b.KX126_PED_CNTL2_PED_ODR_100, m.KX126_PED_CNTL2_PED_ODR_MASK)

    sensor.set_average(e.KX126_LP_CNTL_AVC[avg])

    # configure interrupts
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPOVI2)  # overflow interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPWMI2)  # watermark interrupt to INT2
    sensor.set_bit(r.KX126_INC7, b.KX126_INC7_STPINCI2)  # step counter increment interrupt to INT2

    sensor.set_bit(r.KX126_INC5, b.KX126_INC5_IEN2)  # enable INT2
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEA2)  # active low
    sensor.reset_bit(r.KX126_INC5, b.KX126_INC5_IEL2)  # latched interrupt

    sensor.set_bit(r.KX126_CNTL1, b.KX126_CNTL1_PDE)  # enable pedometer

    set_pedometer_parameters(sensor, cfg)

    if power_off_on:
        sensor.set_power_on()

    LOGGER.info('Pedometer step counting initialized')


class KX126PedometerLogger(SingleChannelEventReader):

    def override_config_parameters(self):
        SingleChannelEventReader.override_config_parameters(self)
        evkit_config.odr = 100

    def enable_data_logging(self, **kwargs):
        enable_pedometer(self.sensors[0], **kwargs)


def main():
    app = KX126PedometerLogger([KX126Driver])
    app.enable_data_logging(odr=evkit_config.odr)
    app.run(KX126PedometerStream)


if __name__ == '__main__':
    main()
