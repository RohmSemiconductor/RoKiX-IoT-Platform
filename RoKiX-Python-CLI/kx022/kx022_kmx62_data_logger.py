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
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, evkit_config
from kx_lib.kx_data_logger import MultiChannelReader

from kx022 import kx022_data_logger
from kx022.kx022_driver import KX022Driver
from kx022.kx022_driver import r as kx022_reg

from kmx62 import kmx62_data_logger
from kmx62.kmx62_driver import KMX62Driver
from kmx62.kmx62_driver import r as kmx62_reg

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX022KMX62DataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = "ch!ax!ay!az"
    reg = kx022_reg.KX022_XOUT_L
    kmx62_fmt = "<Bhhhhhhh"
    kmx62_hdr = "ch!ax!ay!az!mx!my!mz!temp"
    kmx62_reg = kmx62_reg.KMX62_ACCEL_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY data stream"
        assert not timer, 'timer not supported'
        sensor_kx022, sensor_kmx62 = sensors

        assert sensor_kx022.name in KX022Driver.supported_parts
        assert sensor_kmx62.name in KMX62Driver.supported_parts

        StreamConfig.__init__(self, sensor_kx022)

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        # Default way to define request message
        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index)

        self.define_request_message(
            sensor=sensor_kmx62,
            fmt=self.kmx62_fmt,
            hdr=self.kmx62_hdr,
            reg=self.kmx62_reg,
            pin_index=pin_index)


class KX022KMX62DataLogger(MultiChannelReader):

    def enable_data_logging(self, **kwargs):
        kx022_data_logger.enable_data_logging(self.sensors[0], **kwargs)
        kmx62_data_logger.enable_data_logging(self.sensors[1], **kwargs)


def main():
    l = KX022KMX62DataLogger([KX022Driver, KMX62Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX022KMX62DataStream)


if __name__ == '__main__':
    main()
