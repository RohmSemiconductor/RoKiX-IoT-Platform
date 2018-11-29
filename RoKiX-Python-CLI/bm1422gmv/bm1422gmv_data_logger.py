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
BM1422gmv data logger application
"""
import imports  # pylint: disable=unused-import,relative-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_datalogger_args, get_pin_index, evkit_config, \
    convert_to_enumkey
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_POLARITY, \
    ACTIVE_HIGH
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from bm1422gmv.bm1422gmv_driver import bm1422gmv_driver, r, e

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class BM1422gmvDataStream(StreamConfig): # pylint: disable=too-few-public-methods
    def __init__(self, sensor, pin_index=None):
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        self.define_request_message(
            fmt="<Bhhh",
            hdr="ch!mx!my!mz",
            reg=r.BM1422GMV_DATAX,
            pin_index=pin_index)


def enable_data_logging(sensor,
                        odr=20,
                        avg="4TIMES"):

    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    assert avg in e.BM1422GMV_AVER_AVG, \
        'Invalid value for avg. Valid values are %s' % \
        e.BM1422GMV_AVER_AVG.keys()

    valid_odrs = e.BM1422GMV_CNTL1_ODR.keys()

    assert convert_to_enumkey(odr) in valid_odrs, \
        'Invalid odr value "{}". Valid values are {}'.format(odr, valid_odrs)

    sensor.set_power_on()

    sensor.set_odr(e.BM1422GMV_CNTL1_ODR[convert_to_enumkey(odr)])

    sensor.set_averaging(e.BM1422GMV_AVER_AVG[avg])

    #
    # interrupts settings
    #

    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy_pin()
        if POLARITY_DICT[sensor.resource[CFG_POLARITY]] == ACTIVE_HIGH:
            sensor.set_drdy_high_active()
            #print("active high")
        else:
            sensor.set_drdy_low_active()
            #print("active low")
    elif evkit_config.get('generic', 'drdy_operation') == 'DRDY_REG_POLL':
        sensor.enable_drdy_pin()

    #
    # Turn on measurement
    #

    sensor.start_continuous_measurement()

    LOGGER.info('enable_data_logging done')


def read_with_polling(sensor, loop):
    count = 0
    dl = SensorDataLogger()
    dl.add_channel('ch!mx!my!mz')
    dl.start()

    try:
        while (loop is None) or (count < loop):
            count += 1
            sensor.drdy_function()
            _, mx, my, mz = sensor.read_data()
            dl.feed_values((10, mx, my, mz))

    except KeyboardInterrupt:
        dl.stop()


def read_with_stream(sensor, loop):
    stream = BM1422gmvDataStream(sensor)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=10):

    args = get_datalogger_args()
    if args.odr:
        odr = args.odr

    sensor = bm1422gmv_driver()
    connection_manager = ConnectionManager(odr=odr)

    connection_manager.add_sensor(sensor)

    enable_data_logging(sensor, odr=odr)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)

    elif args.timer_stream_mode:
        raise EvaluationKitException('Timer polling not yet implemented')

    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    connection_manager.disconnect()


if __name__ == '__main__':
    app_main()
