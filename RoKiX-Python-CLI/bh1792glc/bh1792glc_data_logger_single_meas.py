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
BH1792GLC logger application,
single measurement stream
"""
from array import array
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, evkit_config
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_POLARITY, CFG_PULLUP, CFG_SAD
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_data_logger import SensorDataLogger
from kx_lib.kx_data_stream import RequestMessageDefinition
from bh1792glc.bh1792glc_driver import BH1792GLCDriver, r


LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class BH1792GLCDataStream(StreamConfig):
    fmt = "<BHH"
    hdr = "ch!ledoff!ledon"
    reg = r.BH1792_DATAOUT_LEDOFF_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY data stream"
        assert timer is None, "Timer not supported"
        assert sensors[0].name in BH1792GLCDriver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        protocol = self.adapter.protocol
        message = RequestMessageDefinition(sensors[0], self.fmt,
                                           self.hdr,
                                           reg=self.reg,
                                           pin_index=pin_index)

        polarity = self.sense_dict[sensors[0].resource[CFG_POLARITY]]
        pullup = self.pullup_dict[sensors[0].resource[CFG_PULLUP]]

        req = protocol.create_macro_req(
            trigger_type=protocol.EVKIT_MACRO_TYPE_INTR,
            gpio_pin=message.gpio_pin,
            gpio_sense=polarity,
            gpio_pullup=pullup
        )

        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
        LOGGER.debug('Macro created with id %d', macro_id)
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)

        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            target=sensors[0].resource[CFG_TARGET],
            identifier=sensors[0].resource[CFG_SAD],
            start_register=message.reg,
            append=False,
            bytes_to_read=4)

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        message.msg_req.append(req)

        # ACK interrupt by reading BH1792_INT_CLEAR (register address 0x58)
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            discard=True,
            target=sensors[0].resource[CFG_TARGET],
            identifier=sensors[0].resource[CFG_SAD],
            start_register=r.BH1792_INT_CLEAR,
            append=False,
            bytes_to_read=1)

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)

        # Start new measurement by writing 0x1 to BH1792_MEAS_START (0x47)
        write_buf = array('B', [0b00000001])
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_WRITE,
            discard=True,
            target=sensors[0].resource[CFG_TARGET],
            identifier=sensors[0].resource[CFG_SAD],
            start_register=r.BH1792_MEAS_START,
            write_buffer=write_buf,
        )

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)


def enable_data_logging(sensor, current):
    sensor.set_single_measurement(current=current)
    sensor.start_measurement()


class BH1792GLCDataLogger(SingleChannelReader):

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], current=1)

    def read_with_polling(self, loop, hdr):
        count = 0
        dl = SensorDataLogger()
        dl.add_channel(hdr)
        dl.start()
        sensor = self.sensors[0]

        try:
            while (loop is None) or (count < loop):
                count += 1
                sensor.drdy_function()
                data = sensor.read_gdata()
                dl.feed_values([10] + list(data))
                sensor.reset_drdy_pin()
                sensor.start_measurement()
        except KeyboardInterrupt:
            pass

        finally:
            dl.stop()


def main():
    logger = BH1792GLCDataLogger([BH1792GLCDriver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(BH1792GLCDataStream)


if __name__ == '__main__':
    main()
