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
BM1383aglv data logger application
"""
import imports  # pylint: disable=unused-import,relative-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_datalogger_args, get_pin_index, evkit_config
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from bm1383aglv.bm1383aglv_driver import bm1383aglv_driver, r, e

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class BM1383aglvDataStream(StreamConfig):
    def __init__(self, sensor, pin_index=None):
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_pin_index()

        self.define_request_message(
            fmt=">BBBBBh",
            hdr="ch!stat!P_msb!P_lsb!P_xl!T_raw",
            reg=r.BM1383AGLV_STATUS_REG,
            pin_index=pin_index)

class BM1383aglvTimerDataStream(StreamConfig):
    def __init__(self, sensor, timer):
        StreamConfig.__init__(self, sensor)

        self.define_request_message(
            fmt=">BBBBBh",
            hdr="ch!stat!P_msb!P_lsb!P_xl!T_raw",
            reg=r.BM1383AGLV_STATUS_REG,
            timer=timer)

def enable_data_logging(sensor, odr=17):

    LOGGER.info('enable_data_logging start')

    sensor.set_power_on()

    #
    # parameter validation
    #
    
    if odr >= 17:
        odrkey = 'AVG_16_50MS'
    elif odr == 8:
        odrkey = 'AVG_32_100MS'
    else:  # odr == 4
        odrkey = 'AVG_64_200MS'

    sensor.set_odr(e.BM1383AGLV_MODE_CONTROL_REG_AVE_NUM[odrkey])


    #
    # interrupts settings
    #

    if evkit_config.get('generic', 'drdy_operation') == 'ADAPTER_GPIO1_INT':
        sensor.enable_drdy_pin()
        sensor.reset_drdy_pin()

    #
    # Turn on measurement
    #

    sensor.start_continuous_measurement()

    LOGGER.info('enable_data_logging done')


def read_with_polling(sensor, loop):

    count = 0
    dl = SensorDataLogger()
    dl.add_channel('ch!P_msb!P_mid!P_lsb!P_xl!T_raw')
    dl.start()

    try:
        while (loop is None) or (count < loop):
            count += 1
            sensor.drdy_function()
            p_msb, p_lsb, p_xl, t_raw = sensor.read_data()
            dl.feed_values((10, p_msb, p_lsb, p_xl, t_raw))

    except KeyboardInterrupt:
        dl.stop()


def read_with_stream(sensor, loop, timer=None):
    if timer:
        stream = BM1383aglvTimerDataStream(sensor, timer=timer)
    else:
        stream = BM1383aglvDataStream(sensor)

    stream.read_data_stream(loop)
    return stream


def app_main(odr=17):

    args = get_datalogger_args()
    if args.odr:
        odr = args.odr

    # For continuous more there 3 possible odr values: 17Hz, 8Hz and 4Hz
    allowed_odrs = (17, 8, 4)

    assert odr in allowed_odrs, \
        "Invalid odr, valid values {}".format(allowed_odrs)

    sensor = bm1383aglv_driver()
    connection_manager = ConnectionManager(odr=odr)

    connection_manager.add_sensor(sensor)

    enable_data_logging(sensor, odr=odr)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)

    elif args.timer_stream_mode:
        read_with_stream(sensor, args.loop, timer=1./odr)

    else:
        read_with_polling(sensor, args.loop)

    sensor.set_power_off()
    connection_manager.disconnect()


if __name__ == '__main__':
    app_main()
