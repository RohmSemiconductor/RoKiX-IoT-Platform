# 
# Copyright 2020 Rohm Semiconductor
#
# pylint: disable=unused-argument, no-self-use
from kx_lib.kx_exception import EvaluationKitException

from kx_lib import kx_logger
LOGGER = kx_logger.get_logger(__name__)


class KxAdapterBase(object):

    def __init__(self, bus2=None):
        self.board_id = -1
        self.engine = None
        self.fw_protocol_version = "0.0"
        self.stream_support = False

    def adapter_connect(self):
        raise NotImplementedError()

    def adapter_disconnect(self):
        raise NotImplementedError()

    def adapter_read_gpio(self, gpio_pin):
        raise EvaluationKitException('Not implemented for this adapter.')

    def adapter_read_sensor_register_i2c(self, target, sad, register, length):
        raise EvaluationKitException('I2C support not available for this adapter')

    def adapter_read_sensor_register_spi(self, target, chip_select, register, length):
        raise EvaluationKitException('SPI support not available for this adapter')

    def adapter_write_sensor_register_i2c(self, target, sad, register, values):
        raise EvaluationKitException('I2C support not available for this adapter')

    def adapter_write_sensor_register_spi(self, target, chip_select, register, values):
        raise EvaluationKitException('SPI support not available for this adapter')

    def adapter_write_gpio(self, gpio_pin, value, connect_input=False):
        raise EvaluationKitException('Not implemented for this adapter.')

    def adapter_read_adc(self, target, channel, resolution,
                         oversample,
                         gain,
                         acq_time_us):
        raise EvaluationKitException('Not implemented for this adapter.')

    def selftest(self, ttype):
        raise EvaluationKitException('Not implemented for this adapter.')

    def get_dev_id(self):
        raise EvaluationKitException('Not implemented for this adapter.')

    def reset(self):
        raise EvaluationKitException('Not implemented for this adapter.')

    def configure_pin(self, gpio_pin, direction, drivemode, connect_input=False):
        raise EvaluationKitException('Not implemented for this adapter.')

    def configure_pin_as_input(self, gpio_pin, drivemode):
        raise EvaluationKitException('Not implemented for this adapter.')

    def configure_fw(self, sleep_enabled):
        LOGGER.warning('Sleep mode not supported in this board.')

    def get_firmware_id(self):
        return 0

