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
KX132 adp data logger application
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig, ExtraData
from kx_lib.kx_util import get_datalogger_args, get_pin_index, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, CH_TEMP, CFG_AXIS_MAP
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from kx132.kx132_driver import KX132Driver, r, b, m, e, filter1_values, filter2_values
from kx132.kx132_data_logger import enable_data_logging

_CODE_FORMAT_VERSION = 2.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class KX132AdpDataStream(StreamConfig):
    def __init__(self, sensor, pin_index=None):
        StreamConfig.__init__(self, sensor)
        sensor.resource[CFG_AXIS_MAP] = [3, 4, 5, 0, 1, 2, 6]
        if pin_index is None:
            pin_index = get_pin_index()

        self.define_request_message(
            fmt="<Bhhhhhhh",
            hdr="ch!ax!ay!az!adp_x!adp_y!adp_z!temp",
            reg=r.KX132_XADP_L,
            pin_index=pin_index)


def configure_adp(sensor,
                  filter1_setting='LP_ODR_4',
                  filter2_setting='HP_ODR_128',
                  adp_odr=25,
                  rms_average='4_SAMPLE_AVG',
                  power_off_on=True):

    #
    # parameter validation
    #

    assert (filter1_setting in list(filter1_values.keys()) +
            [None]), 'Invalid filter1_setting value "{}". Valid values are {}'.format(
                filter1_setting, list(filter1_values.keys()) + [None])
    assert (filter2_setting in list(filter2_values.keys()) +
            [None]), 'Invalid filter2_setting value "{}". Valid values are {}'.format(
                filter2_setting, list(filter2_values.keys()) + [None])
    assert (rms_average in list(e.KX132_ADP_CNTL1_RMS_AVC.keys()) +
            [None]), 'Invalid adp_average value "{}". Valid values are {}'.format(
                rms_average, list(e.KX132_ADP_CNTL1_RMS_AVC.keys() + [None]))
    assert (convert_to_enumkey(adp_odr) in list(e.KX132_ADP_CNTL1_OADP.keys()) +
            [None]), 'Invalid adp_odr value "{}". Valid values are {}'.format(
                convert_to_enumkey(adp_odr), list(e.KX132_ADP_CNTL1_OADP.keys() + [None]))

    if power_off_on:
        sensor.set_power_off()
    #
    # Configure sensor
    #
    # enable adp
    sensor.enable_adp()
    # set filter 1 setting
    sensor.set_adp_filter1(filter1_setting)
    # set filter 2 setting
    sensor.set_adp_filter2(filter2_setting)
    # set adp odr
    sensor.set_adp_odr(e.KX132_ADP_CNTL1_OADP[convert_to_enumkey(adp_odr)])
    # set adp sampling avg
    if rms_average is None:
        sensor.set_rms_average(None)
    else:
        sensor.set_rms_average(e.KX132_ADP_CNTL1_RMS_AVC[rms_average])

    if power_off_on:
        # NOTE: temperature not available on low power mode, enabling only accel channel
        sensor.set_power_on(CH_ACC)

def enable_adp_data_logging(sensor,
                            odr=25,
                            max_range='8G',
                            lp_mode='NO_AVG',
                            low_pass_filter='BYPASS',
                            filter1_setting=None,
                            filter2_setting=None,
                            adp_odr=25,
                            rms_average=None,
                            power_off_on=True,
                            int_number=None):


    if power_off_on:
        sensor.set_power_off()
    #
    # Configure sensor
    #

    enable_data_logging(
        sensor,
        odr=odr,
        max_range=max_range,
        lp_mode=lp_mode,
        low_pass_filter=low_pass_filter,
        power_off_on=False,
        int_number=int_number)

    configure_adp(sensor,
                  filter1_setting=filter1_setting,
                  filter2_setting=filter2_setting,
                  adp_odr=adp_odr,
                  rms_average=rms_average,
                  power_off_on=False)

    # sensor.register_dump()
    if power_off_on:
        sensor.set_power_on(CH_ACC)


def read_with_polling(sensor, loop):
    count = 0
    dl = SensorDataLogger()
    dl.add_channel("ch!ax!ay!az!adp_x!adp_y!adp_z!temp")
    dl.start()
    try:
        while (loop is None) or (count < loop):
            count += 1
            sensor.drdy_function()
            ax, ay, az, adp_x, adp_y, adp_z, temp = sensor.read_combined_adp_data(
                CH_ACC | CH_TEMP)
            dl.feed_values((10, ax, ay, az, adp_x, adp_y, adp_z, temp))
    except KeyboardInterrupt:
        dl.stop()


def read_with_stream(sensor, loop, timer=None, pin_index=None):
    assert not timer or not pin_index, 'Both timer and pin_index cannot be set at same time.'
    if timer:
        raise NotImplementedError
    else:
        stream = KX132AdpDataStream(sensor, pin_index)
    stream.read_data_stream(loop)
    return stream


def app_main(odr=25):

    args = get_datalogger_args()

    if args.odr:
        odr = args.odr

    sensor = KX132Driver()
    connection_manager = ConnectionManager(odr=odr)
    connection_manager.add_sensor(sensor)

    enable_adp_data_logging(
        sensor, 
        odr=odr, 
        max_range='8G',
        lp_mode='128_SAMPLE_AVG',
        low_pass_filter='BYPASS',
        filter1_setting='LP_ODR_4', # low pass cut off at ODR/4
        filter2_setting='HP_ODR_128', # high pass cut off at ODR/128
        adp_odr=25,
        rms_average='16_SAMPLE_AVG',
        power_off_on=True,
        int_number=None)

    if args.stream_mode:
        read_with_stream(sensor, args.loop)

    elif args.timer_stream_mode:
        read_with_stream(sensor, loop=args.loop, timer=1. / odr)

    else:
        read_with_polling(sensor, args.loop)
    sensor.set_power_off()
    connection_manager.disconnect()


if __name__ == '__main__':
    app_main()
