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
BH1792GLC logger application,
Non synchronized measurement mode using IR leds

The only available ODR in non-synchronized mode is 4 Hz.
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config
from kx_lib.kx_data_logger import SingleChannelReader
from bh1792glc.bh1792glc_driver import BH1792GLCDriver, r

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class BH1792GLCDataStream(StreamConfig):
    fmt = "<BHHHHB"
    hdr = "ch!iroff!iron!NA!NA!int"
    reg = r.BH1792GLC_IRDATA_LEDOFF_LSB

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in BH1792GLCDriver.supported_parts
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


def enable_data_logging(sensor, current, threshold):
    sensor.set_nonsync_measurement(current=current, threshold=threshold)
    sensor.start_measurement()


class BH1792GLCDataLogger(SingleChannelReader):
    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], current=10, threshold=0)


def main():
    logger = BH1792GLCDataLogger([BH1792GLCDriver])
    logger.enable_data_logging()
    logger.run(BH1792GLCDataStream)


if __name__ == '__main__':
    main()
