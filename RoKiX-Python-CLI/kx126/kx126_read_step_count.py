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
Reads step count register
After register is read, stepcount is set to 0
"""

import imports  # pylint: disable=unused-import
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_util import evkit_config
from kx_lib import kx_logger
from kx126 import kx126_driver, kx126_pedometer, kx126_pedometer_params

LOGGER = kx_logger.get_logger(__name__)
LOGGER.setLevel(kx_logger.DEBUG)


def read_step_count(sensor,
                    power_off_on=False):
    steps = sensor.read_step_count()
    if power_off_on:
        sensor.set_power_off()
    LOGGER.info('Steps counted: %s' % steps)
    return steps

def start_step_count(sensor):
    kx126_pedometer.enable_pedometer(
        sensor, odr=100, cfg=kx126_pedometer_params.Pedometer_parameters_odr_100)
    LOGGER.info('Pedometer started')


def main():
    evkit_config.add_argument('--start_step_count', action='store_true')
    args = evkit_config.parse_args()
    sensor = kx126_driver.KX126Driver()
    cm = ConnectionManager(skip_init=True)
    cm.add_sensor(sensor)
    if args.start_step_count:
        start_step_count(sensor)
    else:
        read_step_count(sensor)

if __name__ == '__main__':
    main()
