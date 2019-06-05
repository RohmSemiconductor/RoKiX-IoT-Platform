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
KX126 data and pedometer
"""
# Example application for basic pedometer step counting
###
# Pedometer uses interrupts int1 for the step event and int2 for the watermark event
###
# Pedometer outputs
##
# ins1, STPOVI = step overflow event
# ins1, STPWMI = step watermark event
# ins2, STPINCI = step counter increment event

import imports  # pylint: disable=unused-import
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index
from kx_lib.kx_data_logger import MultiChannelReader

from kx126 import kx126_data_logger
from kx126 import kx126_pedometer
from kx126 import kx126_pedometer_params

from kx126.kx126_driver import KX126Driver
from kx126.kx126_driver import r


class KX126PedometerDataStream(StreamConfig):
    def __init__(self, sensors, pin_index=None, timer=None):
        assert sensors[0].name in KX126Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        self.define_request_message(
            fmt="<BBBBBBB",
            hdr="ch!ins1!ins2!ins3!stat!N/A!rel",
            reg=r.KX126_INS1,
            pin_index=2)

        # packet index number after xyz data
        self.define_request_message(
            fmt="<Bhhh",
            hdr="ch!ax!ay!az",
            reg=r.KX126_XOUT_L,
            pin_index=1)


class KX126PedometerDataLogger(MultiChannelReader):
    def enable_data_logging(self, **kwargs):
        kx126_pedometer.enable_pedometer(self.sensors[0], cfg=kx126_pedometer_params.Pedometer_parameters_odr_100)
        kx126_data_logger.enable_data_logging(self.sensors[0], **kwargs)


def main():
    l = KX126PedometerDataLogger([KX126Driver])
    l.enable_data_logging(odr=100)
    l.run(KX126PedometerDataStream)


if __name__ == '__main__':
    main()
