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
"""Kionix KXR94 data logger application."""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_timer, evkit_config, adc_conv
from kx_lib.kx_data_logger import SingleChannelReader
from kxd94.kxd94_driver import KXD94Driver
from kx_lib.kx_configuration_enum import CFG_ADC_RESOLUTION, CFG_ADC_REF_V, CFG_ADC_GAIN

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


def adc_value(resource, payload, divider=1):

    res = resource[CFG_ADC_RESOLUTION]
    gain = resource[CFG_ADC_GAIN]
    vref = resource[CFG_ADC_REF_V]

    return adc_conv(payload,
                    bits=res,
                    gain=gain,
                    refv=vref,
                    divider=1)


class KXD94DataStream(StreamConfig):
    fmt = '<BHHH'
    hdr = 'ch!ax!ay!az'
    reg = None

    def __init__(self, sensors, pin_index=None, timer=None):
        """DRDY and timer data stream."""
        assert len(sensors) == 1
        sensor = sensors[0]
        assert sensor.name in KXD94Driver.supported_parts
        StreamConfig.__init__(self, sensor)

        # Get the ADC channels masquerading as interrupt pins.
        if pin_index is None:
            pin_index = sensor.int_pins

        # Get the data-read timer interval.
        if timer is None:
            timer = get_drdy_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer)


class KXD94DataLogger(SingleChannelReader):
    @staticmethod
    def enable_data_logging(**kwargs):
        timer_interval = kwargs.get('timer_interval')
        if timer_interval is not None:
            evkit_config.set('drdy_timer_interval', timer_interval)

    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        key = 'drdy_function_mode'
        new_value = 'TIMER_POLL'
        LOGGER.info(
            'Only the timer DRDY-mode is supported; forcing {:s} to {:s}'
            .format(key, new_value))
        evkit_config.set(key, new_value)


def main():
    logger = KXD94DataLogger([KXD94Driver])
    logger.enable_data_logging(
        timer_interval=evkit_config.drdy_timer_interval)

    # def callback(data):
    #    resource = logger.sensors[0].resource
    #    print("{:.2f}, {:1.2f}, {:1.2f}".format(
    #        adc_value(resource, data[1]), adc_value(resource, data[2]), adc_value(resource, data[3])))

    logger.run(KXD94DataStream)
    #logger.run(KXD94DataStream, reader_arguments={'console' : False, 'callback': callback})


if __name__ == '__main__':
    main()
