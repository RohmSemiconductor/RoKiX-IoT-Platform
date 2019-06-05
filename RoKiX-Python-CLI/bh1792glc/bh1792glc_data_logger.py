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
BH1792GLC logger application, Synchronized Measurement Mode.
"""
# pylint: disable=duplicate-code
from array import array
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_POLARITY, CFG_PULLUP, CFG_SAD
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_data_stream import RequestMessageDefinition
from bh1792glc.bh1792glc_driver import BH1792GLCDriver, r, e

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class BH1792GLCDataStream(StreamConfig):
    fmt = "<BHH"
    hdr = "ch!ledoff!ledon"
    reg = r.BH1792GLC_FIFODATA0_LSB

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY data stream"
        assert timer is None, "Timer stream not supported"
        assert sensors[0].name in BH1792GLCDriver.supported_parts
        StreamConfig.__init__(self, sensors[0])

        # get pin_index if it is not given and timer is not used
        if pin_index is None:
            pin_index = get_drdy_pin_index()

        protocol = self.adapter.protocol
        message = RequestMessageDefinition(self.sensor,
                                           fmt=self.fmt,
                                           hdr=self.hdr,
                                           reg=self.reg,
                                           pin_index=pin_index)

        # Create macro handler for interrupt
        req = protocol.create_macro_req(
            trigger_type=protocol.EVKIT_MACRO_TYPE_INTR,
            gpio_pin=message.gpio_pin,
            gpio_sense=self.sense_dict[sensors[0].resource[CFG_POLARITY]],
            gpio_pullup=self.pullup_dict[sensors[0].resource[CFG_PULLUP]]
        )

        # create macro action for reading BH1792GLC OHR FIFO data over I2C
        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)
        LOGGER.debug('Macro created with id %d', macro_id)

        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            target=self.sensor.resource[CFG_TARGET],
            identifier=self.sensor.resource[CFG_SAD],
            start_register=message.reg,
            bytes_to_read=4,
            append=False,
            run_count=32)

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        message.msg_req.append(req)
        LOGGER.debug(req)

        # create macro action for reading FIFO_LEV after 32 measurements read from FIFO
        # (ref datasheet, Control sequence diagram for syncronized measurement mode)
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            target=self.sensor.resource[CFG_TARGET],
            discard=True,
            identifier=self.sensor.resource[CFG_SAD],
            start_register=r.BH1792GLC_FIFO_LEV,
            bytes_to_read=1,
            append=False)

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        message.msg_req.append(req)
        LOGGER.debug(req)

        # create macro handler for sending synchronization signal to BH1792GLC
        # sync timer

        message = RequestMessageDefinition(self.sensor,
                                           fmt='',
                                           hdr='',
                                           reg=0,
                                           pin_index=None)
        req = protocol.create_macro_req(
            trigger_type=protocol.EVKIT_MACRO_TYPE_POLL,
            timer_scale=protocol.EVKIT_TIME_SCALE_MS,
            timer_value=int(1000)
        )

        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)
        LOGGER.debug('Macro created with id %d', macro_id)

        # create macro action for syncronization signal
        write_buf = array('B', [0b00000001])
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_WRITE,
            target=self.sensor.resource[CFG_TARGET],
            discard=True,
            identifier=self.sensor.resource[CFG_SAD],
            start_register=r.BH1792GLC_MEAS_SYNC,
            write_buffer=write_buf,
        )

        self.adapter.send_message(req)
        message.msg_req.append(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        LOGGER.debug(req)


def enable_data_logging(sensor, odr, current):

    odrkey = str(convert_to_enumkey(odr)) + "HZ"
    valid_odrs = e.BH1792GLC_MEAS_CONTROL1_MSR.keys()
    assert odrkey in valid_odrs, 'Invalid odr value "{}"'.format(odr)

    mode = e.BH1792GLC_MEAS_CONTROL1_MSR[convert_to_enumkey(odrkey)]
    sensor.set_sync_measurement(mode=mode, current=current)
    sensor.sync_measurement()


class BH1792GLCDataLogger(SingleChannelReader):

    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = 256

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], odr=evkit_config.odr, current=0x3f)

    def read_with_polling(self, loop, hdr):
        raise EvaluationKitException('Polling mode not implemented')


def main():
    logger = BH1792GLCDataLogger([BH1792GLCDriver])
    logger.enable_data_logging()
    logger.run(BH1792GLCDataStream)


if __name__ == '__main__':
    main()
