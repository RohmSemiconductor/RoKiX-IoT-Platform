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
from . import imports  # pylint: disable=unused-import
from kx_lib.kx_configuration_enum import BUS1_ADC, CH_ACC, SENSOR_TYPE_ANALOG_3D
from kx_lib.kx_sensor_base import AnalogSensorDriver
from kx_lib import kx_logger

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class KX220Driver(AnalogSensorDriver):
    """A bare-bones driver for Kionix KX220.

    The sensor has no registers. The only configurable things are self-test
    (on/off) and sensor-enable (on/off), both of which are controlled via
    digital pins.
    """
    supported_parts = ['KX220']

    def __init__(self):
        AnalogSensorDriver.__init__(self)
        self.supported_connectivity = [BUS1_ADC]
        self.name = 'KX220'
        self.sensor_type = SENSOR_TYPE_ANALOG_3D
        self._default_channel = CH_ACC

    def set_power_on(self, channel=CH_ACC):
        assert channel == CH_ACC

    def set_power_off(self, channel=CH_ACC):
        assert channel == CH_ACC

    def _read_data(self, channel=CH_ACC):
        assert channel == CH_ACC
        return self.connection_manager.read_adc(self)

    def set_default_on(self):
        pass
