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
"""ROHM RPR-0521RS Proximity and ALS sensor data logger application.

Note:
    The 20 Hz ODR mode (50 ms measurement time) is special; see the
    datasheet for details.
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import evkit_config, get_drdy_pin_index
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_SAD, CFG_POLARITY, CFG_PULLUP
from kx_lib.kx_data_stream import RequestMessageDefinition

from rpr0521rs.rpr0521rs_driver import RPR0521RSDriver, R, E

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

DEFAULT_ODR = 10


def _map_odr_to_meas_time(odr):
    # The keys are integers to avoid issues caused by floating point
    # inaccuracies.
    mapping = {
        2: "400MS_400MS",  # This is actually 2.5 Hz
        10: '100MS_100MS',
        20: '50MS_50MS',
    }
    meas_time_key = mapping.get(int(odr))
    if meas_time_key is None:
        raise ValueError("ODR does not map to any measurement time")
    return E.RPR0521RS_MODE_CONTROL_MEASUREMENT_TIME[meas_time_key]


class RPR0521RSDataStream(StreamConfig):
    fmt = '<BHHH'
    # vis == DATA0, ir == DATA1
    hdr = 'ch!prox!vis!ir'

    def __init__(self, sensors, pin_index=None, timer=None):
        assert timer is None, 'Timer-mode is not supported'
        assert len(sensors) == 1
        sensor = sensors[0]
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_drdy_pin_index()
        assert pin_index == 1, 'Invalid pin index'

        proto = self.adapter.protocol
        message = RequestMessageDefinition(self.sensor,
                                           fmt=self.fmt,
                                           hdr=self.hdr,
                                           reg=0,  # not used
                                           pin_index=pin_index)

        req = proto.create_macro_req(
            trigger_type=proto.EVKIT_MACRO_TYPE_INTR,
            gpio_pin=message.gpio_pin,
            gpio_sense=self.sense_dict[sensor.resource[CFG_POLARITY]],
            gpio_pullup=self.pullup_dict[sensor.resource[CFG_PULLUP]])
        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(
            proto.EVKIT_MSG_CREATE_MACRO_RESP)
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)

        # Reading the interrupt register will clear the interrupt.
        reg_read_cfgs = [(R.RPR0521RS_PS_DATA_LSBS, 6, False),
                         (R.RPR0521RS_INTERRUPT, 1, True)]
        for addr_start, read_size, discard in reg_read_cfgs:
            req = proto.add_macro_action_req(
                macro_id,
                action=proto.EVKIT_MACRO_ACTION_READ,
                target=self.sensor.resource[CFG_TARGET],
                identifier=self.sensor.resource[CFG_SAD],
                start_register=addr_start,
                discard=discard,
                bytes_to_read=read_size)
            self.adapter.send_message(req)
            self.adapter.receive_message(proto.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
            message.msg_req.append(req)


def enable_data_logging(sensor, odr=DEFAULT_ODR, ps_gain='X1',
                        als0_gain='X1', als1_gain='X1'):
    sensor.set_default_on()
    sensor.enable_drdy_int()

    ps_gain_val = E.RPR0521RS_PS_CONTROL_PS_GAIN.get(ps_gain)
    if ps_gain_val is None:
        raise ValueError('invalid ps_gain')
    sensor.set_ps_gain(ps_gain_val)

    gain0_val = E.RPR0521RS_ALS_PS_CONTROL_ALS_DATA0_GAIN.get(als0_gain)
    if gain0_val is None:
        raise ValueError('invalid als0_gain')
    sensor.set_als_data0_gain(gain0_val)

    gain1_val = E.RPR0521RS_ALS_PS_CONTROL_ALS_DATA1_GAIN.get(als1_gain)
    if gain1_val is None:
        raise ValueError('invalid als1_gain')
    sensor.set_als_data1_gain(gain1_val)

    # The odr param will set both proximity and ALS to the same ODR.
    if odr == 20:
        LOGGER.warning(
            "ODR set to 20 Hz, which is special (see datasheet for details)")
    meas_time = _map_odr_to_meas_time(odr)
    sensor.set_measurement_time(meas_time)


class RPR0521RSDataLogger(SingleChannelReader):
    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = DEFAULT_ODR

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    logger = RPR0521RSDataLogger([RPR0521RSDriver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(RPR0521RSDataStream)


if __name__ == '__main__':
    main()
