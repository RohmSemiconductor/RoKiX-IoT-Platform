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
KX132 data logger application
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, evkit_config
from kx_lib.kx_configuration_enum import POLARITY_DICT, CFG_PULLUP, CFG_TARGET, CFG_POLARITY, CFG_SAD, CFG_CS
from kx_lib.kx_data_logger import SingleChannelReader
from kx132.kx132_driver import KX132Driver, r, b
from kx132.kx132_data_logger import enable_data_logging
from kx_lib.kx_data_stream import RequestMessageDefinition

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0

WATERMARK_LEVEL = 10


class KX132FIFODataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = "ch!ax!ay!az"
    reg = r.KX132_1211_BUF_READ

    def __init__(self, sensors, pin_index=None, timer=None):
        "DRDY and timer data stream"
        assert sensors[0].name in KX132Driver.supported_parts
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
        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(
            wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)
        LOGGER.debug('Macro created with id %d', macro_id)

        SPI_MODE = 0 if CFG_SAD in self.sensor.resource else 128

        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            target=self.sensor.resource[CFG_TARGET],
            identifier=self.sensor.get_identifier(),
            start_register=message.reg | SPI_MODE,
            bytes_to_read=6,
            append=False,
            run_count=WATERMARK_LEVEL)

        self.adapter.send_message(req)
        self.adapter.receive_message(
            wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        message.msg_req.append(req)
        LOGGER.debug(req)


def enable_fifo_logging(
    sensor,
    buffer_mode=b.KX132_1211_BUF_CNTL2_BM_FIFO,
    buffer_res=b.KX132_1211_BUF_CNTL2_BRES,
    axis_mask=0x03,
    watermark_level=2,
    **kwargs
):
    kwargs.pop("sensor", None)
    kwargs.pop("power_off_on", None)
    sensor.set_power_off()
    enable_data_logging(sensor, power_off_on=False, **kwargs)
    sensor.enable_fifo(buffer_mode, buffer_res, axis_mask)
    sensor.set_fifo_watermark_level(watermark_level, axes=axis_mask)

    # interrupt to int 1
    # sensor.set_bit(r.KX132_1211_BUF_CNTL2, b.KX132_1211_BUF_CNTL2_BFIE)
    intpin = 1
    if intpin == 1:
        sensor.reset_bit(r.KX132_1211_INC4, b.KX132_1211_INC4_DRDYI1)
        sensor.disable_drdy(1)
        sensor.reset_bit(r.KX132_1211_INC1, b.KX132_1211_INC1_IEL1)  # latched interrupt
        sensor.set_bit(r.KX132_1211_INC1, b.KX132_1211_INC1_IEN1)  # enable interrupt
        # watermark interrupt to 1
        sensor.set_bit(r.KX132_1211_INC4, b.KX132_1211_INC4_WMI1)
    elif intpin == 2:
        pass

    polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    LOGGER.debug('Configuring interrupt polarity {}'.format(
        sensor.resource[CFG_POLARITY]))
    sensor.set_interrupt_polarity(intpin=intpin, polarity=polarity)
    sensor.set_power_on()
    # sensor.register_dump() # print register content
    # sensor.register_dump_listed([0x18, 0x3a, 0x3b]) # print register content
    # empty FIFO otherwise there may be samples over watermark level and no int is received
    sensor.clear_buffer()


class KX132FifoDataLogger(SingleChannelReader):
    def enable_data_logging(self, **kwargs):
        enable_fifo_logging(self.sensors[0], **kwargs)


def main():
    l = KX132FifoDataLogger([KX132Driver])
    l.enable_data_logging(odr=evkit_config.odr,
                          watermark_level=WATERMARK_LEVEL)
    l.run(KX132FIFODataStream)


if __name__ == '__main__':
    main()
