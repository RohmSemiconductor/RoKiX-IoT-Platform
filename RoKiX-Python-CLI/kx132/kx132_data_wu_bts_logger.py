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
Example app for WakeUp/Back To Sleep  (WU and BTS) detection
"""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, evkit_config
from kx_lib.kx_configuration_enum import CFG_SPI_PROTOCOL, CFG_POLARITY, CFG_TARGET, CFG_PULLUP
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_data_stream import RequestMessageDefinition
from kx132.kx132_driver import KX132Driver, r
from kx132.kx132_data_logger import enable_data_logging
from kx132.kx132_test_wu_bts import enable_wu_bts


LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX132DataWuBtsStream(StreamConfig):
    fmt = "<BhhhB"
    hdr = "ch!ax!ay!az!stat"
    reg = r.KX132_1211_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY data stream"
        assert timer is None, "timer not supported"
        assert sensors[0].name in KX132Driver.supported_parts
        StreamConfig.__init__(self, sensors[0])
        sensor = sensors[0]

        # get pin_index if it is not given and timer is not used
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
                         (r.KX132_1211_STATUS_REG, 1, False),
                         (r.KX132_1211_INT_REL, 1, True)]
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


class KX132DataWuBtsLogger(SingleChannelReader):

    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = 12.5

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)
        enable_wu_bts(self.sensors[0], ADP_WB_ISEL=0)


def main():
    l = KX132DataWuBtsLogger([KX132Driver])
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX132DataWuBtsStream)


if __name__ == '__main__':
    main()
