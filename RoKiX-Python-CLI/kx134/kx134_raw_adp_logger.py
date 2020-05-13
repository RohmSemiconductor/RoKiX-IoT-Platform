# The MIT License (MIT)
#
# Copyright (c) 2020 Rohm Semiconductor
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
KX134 rms data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, get_drdy_timer, convert_to_enumkey, evkit_config
from kx_lib.kx_configuration_enum import CH_ACC, CH_ADP, CFG_AXIS_MAP
from kx134.kx134_driver import KX134Driver, filter1_values, filter2_values, r, e
from kx134.kx134_data_logger import enable_data_logging as enable_data_logging_raw
from kx134.kx134_data_logger import KX134DataLogger

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX134RmsDataStream(StreamConfig):
    fmt = "<Bhhhhhh"
    hdr = "ch!adp_x!adp_y!adp_z!ax!ay!az"
    reg = r.KX134_1211_XADP_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in KX134Driver.supported_parts

        StreamConfig.__init__(self, sensors[0])
        sensors[0].resource[CFG_AXIS_MAP] = [0, 1, 2, 3, 4, 5, 6]

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        if timer is None:
            timer = get_drdy_timer()

        self.define_request_message(
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index,
            timer=timer
        )


def configure_adp(sensor,
                  filter1_setting=None,
                  filter2_setting=None,
                  adp_odr=25,
                  rms_average=None,
                  power_off_on=True):
    #
    # parameter validation
    #
    assert sensor.name in KX134Driver.supported_parts

    assert (filter1_setting in list(filter1_values.keys()) +
            [None]), 'Invalid filter1_setting value "{}". Valid values are {}'.format(
                filter1_setting, list(filter1_values.keys()) + [None])
    assert (filter2_setting in list(filter2_values.keys()) +
            [None]), 'Invalid filter2_setting value "{}". Valid values are {}'.format(
                filter2_setting, list(filter2_values.keys()) + [None])
    assert (rms_average in list(e.KX134_1211_ADP_CNTL1_RMS_AVC.keys()) +
            [None]), 'Invalid rms_average value "{}". Valid values are {}'.format(
                rms_average, list(e.KX134_1211_ADP_CNTL1_RMS_AVC.keys() + [None]))
    assert (convert_to_enumkey(adp_odr) in list(e.KX134_1211_ADP_CNTL1_OADP.keys()) +
            [None]), 'Invalid adp_odr value "{}". Valid values are {}'.format(
                convert_to_enumkey(adp_odr), list(e.KX134_1211_ADP_CNTL1_OADP.keys() + [None]))

    if power_off_on:
        sensor.set_power_off()
    #
    # Configure sensor
    #
    # enable adp engine
    sensor.set_power_on(channel=CH_ADP)
    # set filter 1 setting
    sensor.set_adp_filter1(filter1_setting)
    # set filter 2 setting
    sensor.set_adp_filter2(filter2_setting)
    # set ADP odr
    sensor.set_odr(e.KX134_1211_ADP_CNTL1_OADP[convert_to_enumkey(adp_odr)], channel=CH_ADP)
    # set rms sampling avg
    avg = e.KX134_1211_ADP_CNTL1_RMS_AVC.get(rms_average, None)
    sensor.set_average(avg, channel=CH_ADP)

    if power_off_on:
        # NOTE: temperature sensor not available in low power mode
        sensor.set_power_on(CH_ACC)


def enable_data_logging(sensor,
                        odr=25,
                        max_range='8G',
                        lp_mode='128_SAMPLE_AVG',
                        low_pass_filter='ODR_2',
                        filter1_setting=None,
                        filter2_setting=None,
                        adp_odr=25,
                        rms_average=None,
                        power_off_on=True,
                        int_number=None):

    if power_off_on:
        sensor.set_power_off()
    #
    # Configure raw data stream
    #

    enable_data_logging_raw(
        sensor,
        odr=odr,
        max_range=max_range,
        lp_mode=lp_mode,
        low_pass_filter=low_pass_filter,
        power_off_on=False,
        int_number=int_number)

    #
    # Configure ADP data stream
    #

    configure_adp(sensor,
                  filter1_setting=filter1_setting,
                  filter2_setting=filter2_setting,
                  adp_odr=adp_odr,
                  rms_average=rms_average,
                  power_off_on=False)

    if power_off_on:
        sensor.set_power_on(CH_ACC)


class KX134ADPDataLogger(KX134DataLogger):
    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    l = KX134ADPDataLogger([KX134Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX134RmsDataStream)


if __name__ == '__main__':
    main()
