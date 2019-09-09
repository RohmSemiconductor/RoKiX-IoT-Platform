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
import imports  # pylint: disable=unused-import
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import evkit_config, get_drdy_pin_index
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_data_stream import RequestMessageDefinition
from kx_lib.kx_configuration_enum import CFG_POLARITY, CFG_SPI_PROTOCOL, CFG_SAD, CFG_TARGET, CFG_PULLUP

from kx022.kx022_data_logger import enable_data_logging
from kx022.kx022_test_dt import enable_double_tap
from kx022.kx022_driver import KX022Driver, r


class KX022DataDTStream(StreamConfig):
    fmt = '<BhhhB'
    hdr = 'ch!ax!ay!az!direction'
    reg = r.KX022_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        sensor = sensors[0]
        assert sensor.name in KX022Driver.supported_parts
        assert timer is None, 'this stream does not support timers'
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_drdy_pin_index()

        proto = self.adapter.protocol
        message = RequestMessageDefinition(sensor,
                                           fmt=self.fmt,
                                           hdr=self.hdr,
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

        # read three separate register areas
        reg_read_cfgs = [(self.reg, 6, False),
                         (r.KX022_INS1, 1, False),
                         (r.KX022_INT_REL, 1, True)]
        for addr_start, read_size, discard in reg_read_cfgs:
            if self.sensor.resource.get(CFG_SPI_PROTOCOL, 0) == 1:
                # With Kionix components, MSB must be set 1 to indicate reading
                addr_start = addr_start | 1 << 7
            req = proto.add_macro_action_req(
                macro_id,
                action=proto.EVKIT_MACRO_ACTION_READ,
                target=self.sensor.resource[CFG_TARGET],
                identifier=self.sensor.get_identifier(),
                discard=discard,
                start_register=addr_start,
                bytes_to_read=read_size)
            self.adapter.send_message(req)
            self.adapter.receive_message(proto.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
            message.msg_req.append(req)


class KX022DataDTLogger(SingleChannelReader):
    def enable_data_logging(self, **kwargs):
        sensor = self.sensors[0]
        enable_double_tap(sensor)
        enable_data_logging(sensor)


def main():
    logger = KX022DataDTLogger([KX022Driver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(KX022DataDTStream)


if __name__ == '__main__':
    main()
