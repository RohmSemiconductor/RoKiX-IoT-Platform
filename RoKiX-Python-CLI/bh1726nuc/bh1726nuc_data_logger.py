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
"""BH1726NUC ALS sensor data logger application."""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import evkit_config, get_drdy_pin_index
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_SAD, CFG_POLARITY, CFG_PULLUP
from kx_lib.kx_data_stream import RequestMessageDefinition
from bh1726nuc.bh1726nuc_driver import BH1726NUCDriver, R, E, B

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

DEFAULT_ODR = 10


def _odr_to_itime(odr):
    """Calculate an ITIME register value for an ODR.

    Args:
        odr (float or int): Desired measurement frequency in Hertz.

    Returns:
        int: The calculated ITIME value.
    """
    t_int = 2.8e-6  # typical = 2.8 us, max = 4.0 us
    t_meas = 1.0 / odr
    # This is from the datasheet.
    itime_reg_val = int(-((t_meas - 714 * t_int) / (964 * t_int)) + 256)
    if itime_reg_val < 0:
        raise ValueError('ODR is too low; ITIME would be negative')
    if itime_reg_val > 0xff:
        # ITIME is an 8-bit register field.
        raise ValueError('ODR is too high; ITIME would not fit in the register')
    return itime_reg_val


class BH1726NUCDataStream(StreamConfig):
    fmt = '<BHH'
    hdr = 'ch!data0!data1'

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

        # Reading the control register will clear the interrupt.
        reg_read_cfgs = [(R.BH1726NUC_DATA0_LSB, 4, False),
                         (R.BH1726NUC_CONTROL, 1, True)]
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


def enable_data_logging(sensor, odr=DEFAULT_ODR, gain0='X1', gain1='X1'):
    sensor.set_power_on()
    sensor.start_measurement()

    # Note that the ODR is not very accurate and the actual ODR tends to be
    # faster than what was set. (The sensor doesn't have an ODR setting; ODR is
    # simulated by adjusting integration time.)
    itime = _odr_to_itime(odr)
    sensor.set_odr(itime)

    gain0_value = E.BH1726NUC_GAIN_DATA0_GAIN[gain0]
    sensor.set_gain0(gain0_value)
    gain1_value = E.BH1726NUC_GAIN_DATA1_GAIN[gain1]
    sensor.set_gain1(gain1_value)

    sensor.write_interrupt_thresholds(1, 0)  # Always interrupt.
    sensor.set_interrupt_persistence(
        B.BH1726NUC_INTERRUPT_PERSIST_TOGGLE_AFTER_MEASUREMENT)
    sensor.enable_int_pin()
    sensor.start_measurement()


class BH1726NUCDataLogger(SingleChannelReader):
    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = DEFAULT_ODR

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    logger = BH1726NUCDataLogger([BH1726NUCDriver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(BH1726NUCDataStream)


if __name__ == '__main__':
    main()
