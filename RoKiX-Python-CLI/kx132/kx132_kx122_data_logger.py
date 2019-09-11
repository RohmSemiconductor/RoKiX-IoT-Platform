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
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_other_pin_index, evkit_config
from kx_lib.kx_data_logger import MultiChannelReader


from kx022 import kx022_data_logger
from kx022.kx022_driver import KX022Driver
from kx022.kx022_driver import r as kx022_r

from kx132 import kx132_data_logger
from kx132.kx132_driver import KX132Driver
from kx132.kx132_driver import r as kx132_r

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX132KX122DataStream(StreamConfig):

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY data stream"
        assert not timer, 'timer not supported'
        sensor_kx122, sensor_kx132 = sensors  # unpack list ofr sensors
        assert sensor_kx122.name in KX022Driver.supported_parts
        assert sensor_kx132.name in KX132Driver.supported_parts

        StreamConfig.__init__(self, sensor_kx122)

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()
        kx132_pin_index = get_other_pin_index()
        assert kx132_pin_index != pin_index, 'Dont route both streams to same GPIO'

        # Default way to define request message
        self.define_request_message(
            fmt="<Bhhh",
            hdr="ch!ax!ay!az",
            reg=kx022_r.KX022_XOUT_L,
            pin_index=pin_index)

        self.define_request_message(
            sensor=sensor_kx132,
            fmt="<Bhhh",
            hdr="ch!ax!ay!az",
            reg=kx132_r.KX132_1211_XOUT_L,
            pin_index=kx132_pin_index)


class KX132KX122DataLogger(MultiChannelReader):
    def enable_data_logging(self, **kwargs):
        kx022_data_logger.enable_data_logging(self.sensors[0], **kwargs)
        kwargs['int_number'] = get_other_pin_index()
        kx132_data_logger.enable_data_logging(self.sensors[1], **kwargs)


def main():
    l = KX132KX122DataLogger([KX022Driver, KX132Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX132KX122DataStream)


if __name__ == '__main__':
    main()
