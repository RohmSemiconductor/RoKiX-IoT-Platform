# 
# Copyright 2020 Rohm Semiconductor
#
import array
import time
import struct
from kx_lib import kx_protocol
from kx_lib import kx_protocol_2_x
from kx_lib.kx_exception import ProtocolException
from kx_lib.kx_base_class import KxAdapterBase
from kx_lib import kx_logger
from kx_lib.kx_configuration_enum import PULLUP, PULLDOWN, NOPULL, NODRIVE, DRIVELOW, DRIVEHIGH

LOGGER = kx_logger.get_logger(__name__)

# LOGGER.setLevel(kx_logger.INFO)
# LOGGER.setLevel(kx_logger.DEBUG)


class KxAdapterEvk(KxAdapterBase):
    def __init__(self, bus2):
        KxAdapterBase.__init__(self)
        self.stream_support = True
        self.bus2 = bus2
        self.protocol = None  # protocol engine instance and message definitions

        self.adapter_connect()

    def __pyreverse(self):
        "This method is just for  crating proper UML chart with pyreverse"
        from kx_lib.kx_bus2 import KxComPort, KxSocket, KxWinBLE, KxLinuxBLE, KxLinuxI2C
        self.bus2 = KxComPort
        self.bus2 = KxSocket
        self.bus2 = KxWinBLE
        self.bus2 = KxLinuxBLE
        self.bus2 = KxLinuxI2C
        self.protocol = kx_protocol

    def adapter_read_sensor_register_i2c(self, target, sad, register, length):
        msg = self.protocol.read_req(target, sad, register, length)
        self.send_message(msg)
        message_type_, message_data = self.receive_message(self.protocol.EVKIT_MSG_READ_RESP)
        del message_type_
        return message_data

    def adapter_write_sensor_register_i2c(self, target, sad, register, values):
        # pack the message
        msg = self.protocol.write_req(target, sad, register, values)
        # send the message
        self.send_message(msg)
        # wait for response message
        self.receive_message(self.protocol.EVKIT_MSG_WRITE_RESP)

    def adapter_read_gpio(self, gpio_pin):

        msg = self.protocol.gpio_state_req(gpio_pin)
        self.send_message(msg)

        resp = self.receive_message(self.protocol.EVKIT_MSG_GPIO_STATE_RESP)
        message_type_, (gpio_pin_, gpio_state) = resp
        del gpio_pin_, message_type_
        if gpio_state == self.protocol.EVKIT_GPIO_PIN_SENSE_LOW:
            return 0
        elif gpio_state == self.protocol.EVKIT_GPIO_PIN_SENSE_HIGH:
            return 1
        raise ProtocolException('Unknown EVKIT_MSG_GPIO_STATE_RESP')

    def adapter_write_gpio(self, gpio_pin, value, connect_input=False):
        """Set a GPIO pin to some state.

        Args:
            gpio_pin (int): GPIO pin to configure.
            value (int): 0 to drive low, 1 to drive high.
            connect_input (bool): Whether to keep the input buffer connected or
                not. (This is not supported by all platforms.)
        """
        self.configure_pin(gpio_pin,
                           self.protocol.EVKIT_GPIO_PIN_OUTPUT,
                           value, connect_input)

    def adapter_read_adc(
            self, target, channel, resolution,
            oversample=kx_protocol_2_x.EVKIT_ADC_OVERSAMPLE_NONE,
            gain=kx_protocol_2_x.EVKIT_ADC_GAIN_NONE,
            acq_time_us=0):
        """Read a value from an ADC.

        Args:
            target (int):      enumerated hw peripheral id : EVKIT_BUS1_TARGET_X
            channel (int):     ADC channel (pin number) to read from.
            oversample (int):  ADC oversampling: EVKIT_ADC_OVERSAMPLE_x
            gain (int):        ADC gain: EVKIT_ADC_GAIN_x
            resolution (int):  ADC resolution in bits
            acq_time_us (int): ADC acquisition time in microseconds. 0 means
                the longest acquisition time supported by the platform.

        Returns:
            int: The ADC counts.
        """
        req = self.protocol.adc_read_req(
            target, channel, resolution=resolution,
            acq_time_us=acq_time_us, gain=gain, oversample=oversample)
        self.send_message(req)
        _, adc_counts = self.receive_message(
            self.protocol.EVKIT_MSG_ADC_READ_RESP)

        if len(adc_counts) == 1:
            return struct.unpack('<b', adc_counts)[0]
        elif len(adc_counts) == 2:
            return struct.unpack('<h', adc_counts)[0]
        elif len(adc_counts) == 4:
            return struct.unpack('<l', adc_counts)[0]
        else:
            raise ValueError('unsupported ADC count size')

    def selftest(self, ttype):
        """Run a selftest of the specified type on the board.

        Args:
            ttype (int): Test type. Valid values: EVKIT_SELFTEST_x

        Returns:
            (int, array.array): The status code returned by the selftest and
                the potential payload as bytes.
        """
        self.send_message(self.protocol.selftest_req(ttype))
        try:
            _, payload = self.receive_message(self.protocol.EVKIT_MSG_SELFTEST_RESP)
        except ProtocolException as err:
            if err.status is None:
                raise

            return (err.status, array.array('B', []))

        return (self.protocol.EVKIT_SUCCESS, payload)

    def get_dev_id(self):
        """Return the device's unique hw identifier.

        Note:
            This only works with Evkit protocol v2.

        Returns:
            array.array: The identifier as plain bytes.
        """
        assert self.engine.version == 2
        self.send_message(self.protocol.dev_id_req())
        _, dev_id = self.receive_message(self.protocol.EVKIT_MSG_DEV_INFO_RESP)
        return dev_id

    def get_firmware_id(self):
        """Return the device's firmware version.

        The version is 1 or more bytes from the beginning of the SHA1 of
        the commit from which the firmware was built.

        Note:
            This only works with Evkit protocol v2.

        Returns:
            array.array: The version as plain bytes.

        """
        assert self.engine.version == 2
        self.send_message(self.protocol.dev_fw_id_req())
        _, firmware_id = self.receive_message(self.protocol.EVKIT_MSG_DEV_INFO_RESP)
        return firmware_id

    def get_bootloader_id(self):
        """Return the device's bootloader version.

        Bytes from the beginning of the SHA1 of the commit from
        which the bootloader was built.

        Note:
            This only works with Evkit protocol v2 + new memory region images.

        Returns:
            array.array: The version as plain bytes.

        """
        assert self.engine.version == 2
        self.send_message(self.protocol.dev_fw_bl_id_req())
        _, bootloader_id = self.receive_message(self.protocol.EVKIT_MSG_DEV_INFO_RESP)
        return bootloader_id

    def reset(self):
        """Reset the attached device.

        Note:
            This action is not supported by all platforms.
        """
        req = self.protocol.reset_req(self.protocol.EVKIT_RESET_HARD)
        self.send_message(req)

    def configure_i2c(self, target, frequency):
        self.send_message(self.protocol.configure_i2c_reqest(target, frequency))
        self.receive_message(self.protocol.EVKIT_MSG_CONFIGURE_RESP)

    def configure_spi(self, targe, frequency, mode):
        self.send_message(self.protocol.configure_spi_reqest(targe, frequency, mode))
        self.receive_message(self.protocol.EVKIT_MSG_CONFIGURE_RESP)

    def configure_fw(self, sleep_enabled=True):

        if self.protocol.EVKIT_PROTOCOL_VERSION_MAJOR == 1:
            # GPIO configuration on FW 1 is not working.
            # This will not be implemented until there is need for it.
            LOGGER.warning('FW configuration notsupported on FW 1. Do nothing.')
            return

        if sleep_enabled:
            sleep_mode = self.protocol.EVKIT_CPU_SLEEP_ENABLE
        else:
            sleep_mode = self.protocol.EVKIT_CPU_SLEEP_DISABLE

        self.send_message(self.protocol.configure_fw_reqest(sleep_mode))
        self.receive_message(self.protocol.EVKIT_MSG_CONFIGURE_RESP)

    def configure_pin(self, gpio_pin, direction, drivemode, connect_input=True):
        """Configure a GPIO pin.

        Args:
            gpio_pin (int): Pin which to configure.
            direction (int): EVKIT_GPIO_PIN_INPUT or
                EVKIT_GPIO_PIN_OUTPUT
            drivemode (int):
                PULLUP,
                PULLDOWN,
                NOPULL for inputs.
                or
                DRIVEHIGH,
                DRIVELOW,
                NODRIVE for outputs.

            connect_input (bool): Whether to keep the input buffer connected or
                not. (This is not supported by all platforms.)
        """
        if self.protocol.EVKIT_PROTOCOL_VERSION_MAJOR == 1:
            # GPIO configuration on FW 1 is not working.
            # This will not be implemented until there is need for it.
            LOGGER.warning('GPIO configuration not supported on FW 1. Nothing to do.')
            return

        if connect_input:
            input_conn_arg = self.protocol.EVKIT_GPIO_PIN_CONNECTED
        else:
            input_conn_arg = self.protocol.EVKIT_GPIO_PIN_DISCONNECTED

        if direction == self.protocol.EVKIT_GPIO_PIN_INPUT:
            drivemode = self.pullup_dict[drivemode]
        elif direction == self.protocol.EVKIT_GPIO_PIN_OUTPUT:
            drivemode = self._drivemode_dict[drivemode]
        else:
            raise ValueError('invalid pin direction')

        req = self.protocol.gpio_config_req(
            gpio_pin, direction, input_conn_arg, drivemode)
        self.send_message(req)
        resp = self.receive_message(self.protocol.EVKIT_MSG_GPIO_CONFIG_RESP)
        LOGGER.debug(resp)

    def configure_pin_as_input(self, gpio_pin, drivemode):
        """Configure GPIO pin as input

            Args:
            gpio_pin(int) : physical gpio pin to configure
            drivemode(int) : NOPULL, PULLDOWN, PULLUP = range(3)
        """

        connect_input = True

        self.configure_pin(gpio_pin, self.protocol.EVKIT_GPIO_PIN_INPUT,
                           drivemode, connect_input=connect_input)

    def configure_pin_as_output(self, gpio_pin, drivemode, connect_input=False):
        self.configure_pin(gpio_pin, self.protocol.EVKIT_GPIO_PIN_OUTPUT,
                           drivemode, connect_input)

    def send_message(self, message):
        LOGGER.debug(message)
        self.bus2.write(message)

    def receive_message(self, wait_for_message=None, cache_messages=True):
        resp = self.engine.receive_single_message(wait_for_message, cache_messages)
        LOGGER.debug(resp)
        return self.protocol.unpack_response_data(resp)

    def adapter_connect(self):
        LOGGER.debug('>connect')

        # create protocol and engine for making version query
        self.protocol = kx_protocol
        self.engine = kx_protocol.ProtocolEngine(self.bus2)

        for retry in range(2):
            self.bus2.flush()  # Flush com port in case there is already some unwanted data

            self.send_message(kx_protocol.version_req())  # Version REQ is same for all protocol versions

            # Ref
            # windows user guide 4.1.4. FTDI USB Serial driver and
            # linux  /sys/bus/usb-serial/devices/ttyUSB0/latency_timer
            # https://github.com/pyserial/pyserial/issues/287

            try:
                _, [major_version, minor_version] = self.receive_message(wait_for_message=kx_protocol.EVKIT_MSG_VERSION_RESP)
                self.fw_protocol_version = '%d.%d' % (major_version, minor_version)
                break

            except ProtocolException as exception:
                LOGGER.error(exception)
                time.sleep(0.5)
                if retry == 1:
                    self.adapter_disconnect()
                    raise exception

        LOGGER.info('Firmware protocol version %d.%d' % (major_version, minor_version))

        if (major_version, minor_version) == (1, 1) or \
           (major_version, minor_version) == (1, 2):
            self.protocol = kx_protocol
            self.engine = kx_protocol.ProtocolEngine(self.bus2)

        elif (major_version, minor_version) == (2, 0):
            self.protocol = kx_protocol_2_x
            self.engine = kx_protocol_2_x.ProtocolEngine2(self.bus2)

            self.adapter_read_sensor_register_spi = self.adapter_read_sensor_register_i2c
            self.adapter_write_sensor_register_spi = self.adapter_write_sensor_register_i2c

            # ask board_id
            self.send_message(kx_protocol.version_req())
            _, [_, _, board_id] = self.receive_message(wait_for_message=kx_protocol.EVKIT_MSG_VERSION_RESP)
            self.board_id = board_id
            LOGGER.info('Board hw id %s' % board_id)

            LOGGER.info('Device UID ' + ':'.join(['%02X' % t for t in self.get_dev_id()]))
            LOGGER.info('Firmware version '
                        + ''.join(['%02x' % t for t in self.get_firmware_id()]))

        else:
            raise ProtocolException('Invalid protocol version (%d.%d)' % (major_version, minor_version))

        # map logical pull mode to corresponding protocol definition
        self.pullup_dict = {
            NOPULL: self.protocol.EVKIT_GPIO_PIN_NOPULL,
            PULLDOWN: self.protocol.EVKIT_GPIO_PIN_PULLDOWN,
            PULLUP: self.protocol.EVKIT_GPIO_PIN_PULLUP
        }
        self._drivemode_dict = {
            NODRIVE: self.protocol.EVKIT_GPIO_PIN_NODRIVE,
            DRIVELOW: self.protocol.EVKIT_GPIO_PIN_DRIVELOW,
            DRIVEHIGH: self.protocol.EVKIT_GPIO_PIN_DRIVEHIGH,
        }

        LOGGER.debug('<connect')

    def adapter_disconnect(self):
        LOGGER.debug('>disconnect')
        self.bus2.close()
        LOGGER.debug('<disconnect')
