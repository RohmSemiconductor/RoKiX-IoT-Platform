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
"""Driver for the ROHM BD7411G Hall-effect sensor module."""
from kx_lib.kx_configuration_enum import CH_ACC, SENSOR_TYPE_GPIO_1D
from kx_lib.kx_sensor_base import SensorDriver
from kx_lib import kx_logger

from . import imports  # pylint: disable=unused-import

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class BD7411GDriver(SensorDriver):
    """Driver for the ROHM BD7411G Hall-effect sensor module."""
    # This sensor doesn't have any configurable features and cannot be talked
    # to. Thus, most of the methods here do nothing.
    name = 'BD7411G'
    supported_parts = [name]

    def __init__(self):
        SensorDriver.__init__(self)
        self._registers = {}
        self._dump_range = (0, 0)
        self.supported_connectivity = []
        # This must be in __init__, because the superclass sets this too.
        self.sensor_type = SENSOR_TYPE_GPIO_1D

    def probe(self):
        """Check the component ID.

        This component doesn't have a way to query the ID, so this function
        always returns success.

        Returns:
            int: Always 1.
        """
        return 1

    def set_default_on(self):
        pass

    def set_power_off(self, channel=CH_ACC):
        pass

    def set_power_on(self, channel=CH_ACC):
        pass

    def set_range(self, range, channel):
        pass

    def set_BW(self, range, channel):
        pass

    def release_interrupts(self, intpin=1):
        pass

    def read_drdy(self):
        pass

    def _read_data(self, channel=CH_ACC):
        return (self.connection_manager.read_sensor_gpio(self, pin=1), )

    # This is required even though it's not in the superclass.
    def por(self):
        pass
