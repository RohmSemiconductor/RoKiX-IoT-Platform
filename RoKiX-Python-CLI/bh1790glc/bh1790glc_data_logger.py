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
BH1790GLC logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_timer, convert_to_enumkey, evkit_config
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_logger import DataloggerBase
from bh1790glc.bh1790glc_driver import BH1790GLCDriver, b, r, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class BH1790GLCDataStream(StreamConfig):
    fmt = "<BHH"
    hdr = "ch!ledon!ledoff"
    reg = r.BH1790_DATAOUT_LEDOFF_L

    def __init__(self, sensor, pin_index=None, timer=None):
        "Timer data stream"
        assert pin_index is None, 'DRDY not supported'
        StreamConfig.__init__(self, sensor)

        if timer is None:
            timer = get_drdy_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer
        )


def enable_data_logging(sensor, odr):
    LOGGER.debug('enable_data_logging start')

    sensor.set_power_on()

    sensor.set_led_freq_128hz()

    # select ODR

    odrkey = str(convert_to_enumkey(odr)) + "HZ"
    valid_odrs = e.BH1790_MEAS_CONTROL1_RCYCLE.keys()
    assert odrkey in valid_odrs, 'Invalid odr value "{}"'.format(odr)
    mode = e.BH1790_MEAS_CONTROL1_RCYCLE[convert_to_enumkey(odrkey)]
    sensor.set_odr(mode)

    # set led modes
    sensor.set_led_pulsed(led=1)
    # sensor.set_led_constant(led=1)

    sensor.set_led_pulsed(led=2)
    # sensor.set_led_constant(led=2)

    sensor.set_led_on_time_216us()
    # sensor.set_led_on_time_216us()

    sensor.set_led_current(b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA)
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_0MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_1MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_2MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_3MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_6MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_10MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_20MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_30MA
    # b.BH1790_MEAS_CONTROL2_LED_CURRENT_60MA

    sensor.start_measurement()

    LOGGER.debug('enable_data_logging done')


class BH1790GLCDataLogger(DataloggerBase):
    def __init__(self):
        DataloggerBase.__init__(self)
        self.sensor = BH1790GLCDriver()
        self.connection_manager.add_sensor(self.sensor)

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensor, **kwargs)

    def read_with_polling(self, *args, **kwargs):  # pylint: disable=unused-argument
        raise EvaluationKitException('Polling mode not implemented')


def main():
    l = BH1790GLCDataLogger()
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(BH1790GLCDataStream)


if __name__ == '__main__':
    main()
