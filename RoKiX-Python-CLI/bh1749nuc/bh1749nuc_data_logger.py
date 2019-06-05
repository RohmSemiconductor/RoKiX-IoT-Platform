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
"""ROHM BH1749NUC data logger application."""
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import evkit_config, convert_to_enumkey, get_drdy_pin_index
from kx_lib.kx_data_logger import SingleChannelReader
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_SAD, CFG_POLARITY, CFG_PULLUP, ADAPTER_GPIO1_INT
from kx_lib.kx_data_stream import RequestMessageDefinition
from bh1749nuc.bh1749nuc_driver import BH1749NUCDriver, R, E, B

_CODE_FORMAT_VERSION = 3.0

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

DEFAULT_ODR = 4.167


class BH1749NUCDataStream(StreamConfig):
    fmt = '<BHHHHH'
    hdr = 'ch!red!green!blue!ir!green2'

    def __init__(self, sensors, pin_index=None, timer=None):
        assert len(sensors) == 1
        assert timer is None, 'Timer-mode is not supported'
        sensor = sensors[0]
        assert sensor.name in BH1749NUCDriver.supported_parts
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

        # The data read is split into two parts, because there is a 16-bit
        # reserved register in the middle that is skipped.
        # The interrupt register is read separately, because the interrupt
        # isn't cleared properly if the register is read as part of a read that
        # doesn't start at the interrupt register address.
        reg_read_cfgs = [(R.BH1749NUC_RED_DATA_LSB, 6, False),
                         (R.BH1749NUC_IR_DATA_LSB, 4, False),
                         (R.BH1749NUC_INTERRUPT, 1, True)]
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


def enable_data_logging(sensor,
                        odr=DEFAULT_ODR,
                        rgb_gain='1X',
                        ir_gain='1X',
                        power_off_on=True):
    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #
    assert rgb_gain in E.BH1749NUC_MODE_CONTROL1_RGB_GAIN, \
        'Invalid value for RGB gain. Valid values are %s' % \
        E.BH1749NUC_MODE_CONTROL1_RGB_GAIN.keys()

    assert ir_gain in E.BH1749NUC_MODE_CONTROL1_IR_GAIN, \
        'Invalid value for IR gain. Valid values are %s' % \
        E.BH1749NUC_MODE_CONTROL1_IR_GAIN.keys()

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # select ODR
    sensor.set_measurement_time(
        E.BH1749NUC_MODE_CONTROL1_MEASUREMENT_MODE[convert_to_enumkey(odr)])

    # Select rgb gain
    sensor.set_rgb_gain(E.BH1749NUC_MODE_CONTROL1_RGB_GAIN[rgb_gain])

    # Select IR gain
    sensor.set_ir_gain(E.BH1749NUC_MODE_CONTROL1_IR_GAIN[ir_gain])

    #
    # interrupt pin routings and settings
    #

    # Interrupt every time there's a new sample available.
    sensor.set_interrupt_persistence(
        B.BH1749NUC_PERSISTENCE_PERSISTENCE_ACTIVE_AFTER_MEASUREMENT)
    sensor.set_interrupt_source_channel(B.BH1749NUC_INTERRUPT_INT_SOURCE_RED)

    # Set data-ready indication mode.
    drdymode = evkit_config.drdy_function_mode
    if drdymode == ADAPTER_GPIO1_INT:
        sensor.enable_int_pin()
    else:
        raise EvaluationKitException(
            'Unsupported drdy_function_mode setting (only ADAPTER_GPIO1_INT is supported)')

    if power_off_on:
        sensor.set_power_on()

    LOGGER.debug('enable_data_logging done')


class BH1749NUCDataLogger(SingleChannelReader):
    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.odr = DEFAULT_ODR

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensors[0], **kwargs)


def main():
    logger = BH1749NUCDataLogger([BH1749NUCDriver])
    logger.enable_data_logging(odr=evkit_config.odr)
    logger.run(BH1749NUCDataStream)


if __name__ == '__main__':
    main()
