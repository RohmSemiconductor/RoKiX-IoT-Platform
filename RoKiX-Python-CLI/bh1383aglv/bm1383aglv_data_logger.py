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
BM1383AGLV data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config
from kx_lib.kx_configuration_enum import ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT
from kx_lib.kx_data_logger import SingleChannelReader
from bm1383aglv.bm1383aglv_driver import BM1383AGLVDriver, r, e


LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class BM1383AGLVDataStream(StreamConfig):
    fmt = ">BBBBBh"
    hdr = "ch!stat!P_msb!P_lsb!P_xl!T_raw"
    reg = r.BM1383AGLV_STATUS_REG

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in BM1383AGLVDriver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        if timer is None:
            timer = get_drdy_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer
        )


def enable_data_logging(sensor, odr, meas_time_ms=None):

    LOGGER.info('enable_data_logging start')

    sensor.set_power_on()

    #
    # parameter validation
    #

    if meas_time_ms is None:
        if odr == 17:
            meas_time_ms = 60
        elif odr == 8:
            meas_time_ms = 120
        elif odr == 4:
            meas_time_ms = 240
        else:
            raise ValueError('invalid ODR')

    # The key names are incorrect in the register file. The 50 ms keys
    # will fetch 60 ms values.
    ave_num_map = {
        (17, 6): 'AVG_1_50MS',
        (17, 9): 'AVG_2_50MS',
        (17, 16): 'AVG_4_50MS',
        (17, 30): 'AVG_8_50MS',
        (17, 60): 'AVG_16_50MS',
        (8, 120): 'AVG_32_100MS',
        (4, 240): 'AVG_64_200MS',
    }
    try:
        odrkey = ave_num_map[(odr, meas_time_ms)]
    except KeyError:
        raise ValueError('invalid measurement time or ODR')

    sensor.set_odr(e.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM[odrkey])

    #
    # interrupts settings
    #
    if evkit_config.drdy_function_mode == ADAPTER_GPIO1_INT:
        sensor.enable_drdy_pin()
        sensor.release_interrupts()
    elif evkit_config.drdy_function_mode == ADAPTER_GPIO2_INT:
        raise EvaluationKitException("ADAPTER_GPIO2_INT not supported.")

    #
    # Turn on measurement
    #

    sensor.start_continuous_measurement()

    LOGGER.info('enable_data_logging done')


class BM1383AGLVDataLogger(SingleChannelReader):

    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = 17

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    logger = BM1383AGLVDataLogger([BM1383AGLVDriver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(BM1383AGLVDataStream)


if __name__ == '__main__':
    main()
