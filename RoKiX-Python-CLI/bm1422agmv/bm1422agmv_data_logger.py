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
BM1422AGMV data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY
from kx_lib.kx_data_logger import SingleChannelReader
from bm1422agmv.bm1422agmv_driver import BM1422AGMVDriver, r, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class BM1422AGMVDataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = "ch!mx!my!mz"
    reg = r.BM1422AGMV_DATAX

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in BM1422AGMVDriver.supported_parts
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


def enable_data_logging(sensor,
                        odr=20,
                        avg="4TIMES"):

    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert avg in e.BM1422AGMV_AVER_AVG, \
        'Invalid value for avg. Valid values are %s' % \
        e.BM1422AGMV_AVER_AVG.keys()

    valid_odrs = e.BM1422AGMV_CNTL1_ODR.keys()

    assert convert_to_enumkey(odr) in valid_odrs, \
        'Invalid odr value "{}". Valid values are {}'.format(odr, valid_odrs)

    sensor.set_power_on()

    sensor.set_odr(e.BM1422AGMV_CNTL1_ODR[convert_to_enumkey(odr)])

    sensor.set_averaging(e.BM1422AGMV_AVER_AVG[avg])

    #
    # interrupts settings
    #
    _intpin = 1
    if evkit_config.drdy_function_mode in ("ADAPTER_GPIO1_INT", "REG_POLL"):
        sensor.enable_drdy_pin()

    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity %s',
                 sensor.resource[CFG_POLARITY])

    sensor.set_interrupt_polarity(intpin=_intpin, polarity=polarity)

    #
    # Turn on measurement
    #
    sensor.start_continuous_measurement()

    LOGGER.info('enable_data_logging done')


class BM1422AGMVDataLogger(SingleChannelReader):

    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = 20

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], odr=evkit_config.odr, **kwargs)


def main():
    logger = BM1422AGMVDataLogger([BM1422AGMVDriver])
    logger.enable_data_logging()
    logger.run(BM1422AGMVDataStream)


if __name__ == '__main__':
    main()
