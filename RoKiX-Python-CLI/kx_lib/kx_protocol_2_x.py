# 
# Copyright 2018 Kionix Inc.
#
# pylint: disable=duplicate-code
import struct
from array import array
from kx_lib.kx_exception import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_protocol_definition_2_x import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_protocol import ProtocolEngine
from kx_lib import kx_protocol
import kx_lib.kx_logger as kx_logger
LOGGER = kx_logger.get_logger(__name__)

# LOGGER.setLevel(kx_logger.INFO)
# LOGGER.setLevel(kx_logger.DEBUG)


class KxMessageContainer(kx_protocol.KxMessageContainer):
    """Message container for protocol v2 messages."""

    def append_payload16bit(self, data):
        """Append a 16-bit value to the payload.

        Args:
            data (int): The value to append.
        """
        if not isinstance(data, int):
            raise ProtocolException('invalid value for message append_payload16bit')

        self.payload += array('B', struct.pack('<H', data))
        self.len += 2


#
# request message packing
#


def version_req():
    msg = KxMessageContainer(EVKIT_MSG_VERSION_REQ)
    return msg.get_message()


def spi_rw_req(target, identifier, read_size, tx_data):
    """Create a SPI RW request message.

    Args:
        target (int): enum of microcontroller hw resource
        identifier (int): CS GPIO pin#
        read_size (int): amount of bytes to read
        tx_data (array.array): array of bytes to write via SPI

    Returns:
        array.array: the message as an array of bytes

    """
    msg = KxMessageContainer(EVKIT_MSG_SPI_RW_REQ)
    msg.append_payload(target)
    msg.append_payload(identifier)
    msg.append_payload(read_size)
    msg.append_payload(tx_data)
    return msg.get_message()


def read_req(target, identifier, register, length=1):
    msg = KxMessageContainer(EVKIT_MSG_READ_REQ)
    if isinstance(register, list):  # This is not supported in default firmware.
        msg.append_payload([target, identifier])
        msg.append_payload(register)
        msg.append_payload([length])
    else:
        msg.append_payload([target, identifier, register, length])

    return msg.get_message()


def write_req(target, identifier, register, value):
    """ value can be single byte or bytearray """
    msg = KxMessageContainer(EVKIT_MSG_WRITE_REQ)
    msg.append_payload(target)
    msg.append_payload(identifier)
    msg.append_payload(register)
    msg.append_payload(value)
    return msg.get_message()


def gpio_state_req(gpio_pin):
    msg = KxMessageContainer(EVKIT_MSG_GPIO_STATE_REQ)
    msg.append_payload(gpio_pin)
    return msg.get_message()


def gpio_config_req(gpio_pin, direction, input_connected, position):
    """Create a GPIO configure request message.

    Args:
        gpio_pin (int): microcontroller's pin index
        direction (int): EVKIT_GPIO_PIN_INPUT or EVKIT_GPIO_PIN_OUTPUT
        input_connected (int): Whether the input buffer is connected or not.
            Valid values are EVKIT_GPIO_PIN_DISCONNECTED and
            EVKIT_GPIO_PIN_CONNECTED.
        positition (int): Pin drive mode. If direction is input, then one of
            EVKIT_GPIO_PIN_NODRIVE,
            EVKIT_GPIO_PIN_DRIVELOW,
            EVKIT_GPIO_PIN_DRIVEHIGH. If direction is output, then one of
            EVKIT_GPIO_PIN_NOPULL,
            EVKIT_GPIO_PIN_PULLUP,
            EVKIT_GPIO_PIN_PULLDOWN.

    Returns:
        array.array: The request message as an array of bytes.
    """
    assert direction in [EVKIT_GPIO_PIN_INPUT,
                         EVKIT_GPIO_PIN_OUTPUT]

    assert input_connected in [EVKIT_GPIO_PIN_DISCONNECTED,
                               EVKIT_GPIO_PIN_CONNECTED]

    if direction == EVKIT_GPIO_PIN_OUTPUT:
        assert position in [EVKIT_GPIO_PIN_NODRIVE,
                            EVKIT_GPIO_PIN_DRIVELOW,
                            EVKIT_GPIO_PIN_DRIVEHIGH]
    elif direction == EVKIT_GPIO_PIN_INPUT:
        assert position in [EVKIT_GPIO_PIN_NOPULL,
                            EVKIT_GPIO_PIN_PULLUP,
                            EVKIT_GPIO_PIN_PULLDOWN]

    msg = KxMessageContainer(EVKIT_MSG_GPIO_CONFIG_REQ)
    msg.append_payload(gpio_pin)
    msg.append_payload(direction)
    msg.append_payload(input_connected)
    msg.append_payload(position)
    return msg.get_message()


def create_macro_req(trigger_type=EVKIT_MACRO_TYPE_INTR,
                     gpio_pin=None,
                     gpio_sense=None,
                     gpio_pullup=None,
                     timer_scale=None,
                     timer_value=None):
    """

        EVKIT_MACRO_TYPE_INTR
             gpio_pin
             gpio_sense
             gpio_pullup

        EVKIT_MACRO_TYPE_POLL
            timer_scale
            timer_value

    """
    msg = KxMessageContainer(EVKIT_MSG_CREATE_MACRO_REQ)
    msg.append_payload(trigger_type)

    if trigger_type == EVKIT_MACRO_TYPE_INTR:
        assert (timer_scale, timer_value) == (None, None)
        msg.append_payload([gpio_pin, gpio_sense, gpio_pullup])

    if trigger_type == EVKIT_MACRO_TYPE_POLL:
        assert (gpio_pin, gpio_sense, gpio_pullup) == (None, None, None)
        msg.append_payload(timer_scale)
        msg.append_payload16bit(timer_value)
    LOGGER.debug(msg)
    return msg.get_message()


def remove_macro_req(macro_id):
    msg = KxMessageContainer(EVKIT_MSG_REMOVE_MACRO_REQ)
    msg.append_payload(macro_id)
    return msg.get_message()


def add_macro_action_req(
        macro_id,
        action,
        target,
        identifier,
        append=True,
        discard=False,
        start_register=None,
        write_buffer=None,
        bytes_to_read=None,
        run_count=1,
        gpio_drive=None,
        adc_oversample=EVKIT_ADC_OVERSAMPLE_NONE,
        adc_gain=EVKIT_ADC_GAIN_NONE,
        adc_resolution=None,
        adc_acq_time_us=0):
    """Create an "add macro action" request message.

    Args:
        macro_id (int):        Macro ID as given by a platform.
        action (int):          EVKIT_MACRO_ACTION_X
        target (int):          enumerated hw peripheral id : EVKIT_BUS1_TARGET_X
        identifier (int):      SPI CS GPIO pin, I2C sad, etc...
        append (bool):         append previous return message or send new return message (NOTE packet size limit is 20 bytes)
        discard (bool):        if True, discard this action's payload
        bytes_to_read (int):   in case of read action
        start_register (int):  register number where to write from or write to
        write_buffer:          data to be written in case of write action
        run_count (int):       amount of times to run the action per macro trigger
        gpio_drive (int):      pin drive state for GPIO_WRITE action
        adc_oversample (int):  ADC oversampling: EVKIT_ADC_OVERSAMPLE_x
        adc_gain (int):        ADC gain: EVKIT_ADC_GAIN_x
        adc_resolution (int):  ADC resolution in bits
        adc_acq_time_us (int): ADC acquisition time in microseconds. 0 means
            the longest acquisition time supported by the platform.

    Returns:
        array.array: the message as an array of bytes

    """
    assert append in (0, 1)
    assert action == action & 0b01111111

    msg = KxMessageContainer(EVKIT_MSG_ADD_MACRO_ACTION_REQ)
    msg.append_payload(macro_id)
    msg.append_payload((action & 0b00111111) | (append << 7) | (discard << 6))
    msg.append_payload(run_count)
    msg.append_payload(target)
    msg.append_payload(identifier)

    if action == EVKIT_MACRO_ACTION_NONE:
        raise ProtocolException('EVKIT_MACRO_ACTION_NONE is not valid action')

    elif action == EVKIT_MACRO_ACTION_PKT_COUNT:
        # identifier defines couter size
        pass

    elif action == EVKIT_MACRO_ACTION_READ:
        assert bytes_to_read > 0
        assert write_buffer is None

        msg.append_payload(start_register)
        msg.append_payload(bytes_to_read)

    elif action == EVKIT_MACRO_ACTION_WRITE:
        assert write_buffer is not None

        msg.append_payload(start_register)
        msg.append_payload(write_buffer)

    elif action == EVKIT_MACRO_ACTION_SPI_RW:
        assert write_buffer is not None
        assert bytes_to_read is not None

        msg.append_payload(bytes_to_read)
        msg.append_payload(write_buffer)

    elif action == EVKIT_MACRO_ACTION_TIMESTAMP:
        # identifier defines time scale
        pass

    elif action == EVKIT_MACRO_ACTION_ADC_READ:
        # identifier indicates the pin
        conf_vars = [
            adc_gain, adc_resolution, adc_acq_time_us, adc_oversample,
        ]
        for var in conf_vars:
            assert var is not None
            msg.append_payload(var)

    elif action == EVKIT_MACRO_ACTION_ADC_READ2:
        # identifier indicates the channel
        pass

    elif action == EVKIT_MACRO_ACTION_GPIO_READ:
        # Identifier defines the GPIO pin.
        pass

    elif action == EVKIT_MACRO_ACTION_GPIO_WRITE:
        assert gpio_drive is not None
        msg.append_payload(gpio_drive)

    return msg.get_message()


def start_macro_action_req(macro_id=None, apply_all=False):
    """
    enable_all True / False
    """
    assert apply_all in (True, False)
    if apply_all is True:
        macro_id = EVKIT_MACRO_APPLY_ACTION_ALL
    assert macro_id is not None

    msg = KxMessageContainer(EVKIT_MSG_START_MACRO_REQ)
    msg.append_payload(macro_id)
    return msg.get_message()


def stop_macro_action_req(macro_id=None, apply_all=False):
    """
    enable_all True / False
    """
    assert apply_all in (True, False)
    if apply_all is True:
        macro_id = EVKIT_MACRO_APPLY_ACTION_ALL
    assert macro_id is not None

    msg = KxMessageContainer(EVKIT_MSG_STOP_MACRO_REQ)
    msg.append_payload(macro_id)
    return msg.get_message()


def reset_req(reset_type=EVKIT_RESET_SOFT):
    assert reset_type in [EVKIT_RESET_SOFT, EVKIT_RESET_HARD]
    msg = KxMessageContainer(EVKIT_MSG_RESET_REQ)
    msg.append_payload(reset_type)
    return msg.get_message()


def dev_id_req():
    # MAC address or HWID
    msg = KxMessageContainer(EVKIT_MSG_DEV_INFO_REQ)
    msg.append_payload(EVKIT_DEV_ID)
    return msg.get_message()


def dev_fw_id_req():
    # firmware version
    msg = KxMessageContainer(EVKIT_MSG_DEV_INFO_REQ)
    msg.append_payload(EVKIT_FW_SW_VER)
    return msg.get_message()


def dev_fw_bl_id_req():
    # bootloader version
    msg = KxMessageContainer(EVKIT_MSG_DEV_INFO_REQ)
    msg.append_payload(EVKIT_FW_BL_SW_VER)
    return msg.get_message()


def selftest_req(type=None):
    """Create a selftest request message.

    Args:
        type (int): Test type. Valid values: EVKIT_SELFTEST_x

    Returns:
        array.array: the message as an array of bytes
    """
    assert type in [EVKIT_SELFTEST_MEM, EVKIT_SELFTEST_RSSI, EVKIT_SELFTEST_DISABLE_SD]
    msg = KxMessageContainer(EVKIT_MSG_SELFTEST_REQ)
    msg.append_payload(type)
    return msg.get_message()


def adc_read_req(target, channel,
                 oversample=EVKIT_ADC_OVERSAMPLE_NONE,
                 gain=EVKIT_ADC_GAIN_NONE,
                 resolution=None,
                 acq_time_us=0):
    """Create a legacy ADC-read request message.

    Args:
        target (int):      enumerated hw peripheral id : EVKIT_BUS1_TARGET_X
        channel (int):     ADC channel (pin number) to read from.
        oversample (int):  ADC oversampling: EVKIT_ADC_OVERSAMPLE_x
        gain (int):        ADC gain: EVKIT_ADC_GAIN_x
        resolution (int):  ADC resolution in bits
        acq_time_us (int): ADC acquisition time in microseconds. 0 means
            the longest acquisition time supported by the platform.

    Returns:
        array.array: the message as an array of bytes
    """
    conf_vars = [
        target, channel,
        gain, resolution, acq_time_us, oversample,
    ]
    msg = KxMessageContainer(EVKIT_MSG_ADC_READ_REQ)
    for var in conf_vars:
        assert var is not None
        msg.append_payload(var)

    return msg.get_message()


def adc_read2_req(target, channel):
    """Create an ADC-read request message for the new ADC interface.

    Args:
        target (int): Peripheral ID. Valid values are prefixed with
            ``EVKIT_BUS1_TARGET_``.
        channel (int): Channel from which to read.

    Returns:
        array.array: The message as an array of bytes.
    """
    msg = KxMessageContainer(EVKIT_MSG_ADC_READ2_REQ)
    msg.append_payload(target)
    msg.append_payload(channel)
    return msg.get_message()


def configure_i2c_reqest(target, frequency=400):
    """
        target (int):      enumerated hw peripheral id : EVKIT_BUS1_TARGET_TWIX
        frequency (int):      clock speed in kHz
    """
    assert target in [EVKIT_BUS1_TARGET_TWI0, EVKIT_BUS1_TARGET_TWI1]
    msg = KxMessageContainer(EVKIT_MSG_CONFIGURE_REQ)
    msg.append_payload(target)
    msg.append_payload16bit(frequency)
    return msg.get_message()


def configure_spi_reqest(target, frequency, mode=EVKIT_SPI_MODE_0):
    """
        target (int):      enumerated hw peripheral id : EVKIT_BUS1_TARGET_SPIX
        mode (int):      SPI mode (0-3)
        frequency (int):      clock speed in kHz
    """
    assert target in [EVKIT_BUS1_TARGET_SPI0, EVKIT_BUS1_TARGET_SPI1, EVKIT_BUS1_TARGET_SPI2]
    assert mode in [EVKIT_SPI_MODE_0, EVKIT_SPI_MODE_1, EVKIT_SPI_MODE_2, EVKIT_SPI_MODE_3]
    msg = KxMessageContainer(EVKIT_MSG_CONFIGURE_REQ)
    msg.append_payload(target)
    msg.append_payload(mode)
    msg.append_payload16bit(frequency)
    return msg.get_message()


def configure_adc_request(target, channel, resolution, gain, oversample,
                          acq_time_us=0):
    """Create a configure request for an ADC.

    Args:
        target (int): Peripheral identifier. Valid identifiers are
            ``EVKIT_BUS1_TARGET_ADCx``.
        resolution (int): Resolution in bits.
        gain (int): Gain enum. Valid values are prefixed with
            ``EVKIT_ADC_GAIN_``.
        oversample (int): Valid values are prefixed with
            ``EVKIT_ADC_OVERSAMPLE_``.
        acq_time_us (int): Acquisition time in microseconds.

    Returns:
        array.array: The request as an array of bytes.
    """
    assert target in [EVKIT_BUS1_TARGET_ADC0]
    assert resolution <= 32
    assert gain in [
        EVKIT_ADC_GAIN_A,
        EVKIT_ADC_GAIN_B,
        EVKIT_ADC_GAIN_C,
        EVKIT_ADC_GAIN_D,
        EVKIT_ADC_GAIN_E,
        EVKIT_ADC_GAIN_F,
        EVKIT_ADC_GAIN_G,
        EVKIT_ADC_GAIN_H,
        EVKIT_ADC_GAIN_NONE,
    ]
    assert oversample in [
        EVKIT_ADC_OVERSAMPLE_2X,
        EVKIT_ADC_OVERSAMPLE_4X,
        EVKIT_ADC_OVERSAMPLE_8X,
        EVKIT_ADC_OVERSAMPLE_16X,
        EVKIT_ADC_OVERSAMPLE_NONE,
    ]
    assert acq_time_us < (2**8 - 1)

    msg = KxMessageContainer(EVKIT_MSG_CONFIGURE_REQ)
    msg.append_payload(target)
    msg.append_payload(channel)
    msg.append_payload(gain)
    msg.append_payload(resolution)
    msg.append_payload(acq_time_us)
    msg.append_payload(oversample)
    return msg.get_message()


def configure_fw_reqest(sleep_mode):
    """
        sleep_mode(int): EVKIT_CPU_SLEEP_DISABLE, EVKIT_CPU_SLEEP_ENABLE
    """
    assert sleep_mode in [EVKIT_CPU_SLEEP_DISABLE, EVKIT_CPU_SLEEP_ENABLE]
    msg = KxMessageContainer(EVKIT_MSG_CONFIGURE_REQ)
    msg.append_payload(EVKIT_BUS1_TARGET_FW)
    msg.append_payload(sleep_mode)
    return msg.get_message()

#
# response message unpacking
#


def unpack_response_data(message):
    # convert string to list of int8
    # message_length = message[0] # not used anymore
    LOGGER.debug('Unpack : %s' % message)
    message_type = message[1]

    # Macro indicators don't have a status octet.
    if message_type >= EVKIT_MSG_MACRO_IND_BASE:
        # NOTE : message_type is EVKIT_MSG_MACRO_IND_X, now it is sent twice. massage_type must be also on payload
        # since struct unpack format string also includes it
        return (message_type, message[1:])

    message_status = message[2]
    if message_status != EVKIT_SUCCESS:
        raise ProtocolException('Protocol error: ({}; {})'
                                .format(EVKIT_ERR_NAMES[message_status],
                                        EVKIT_ERR_DESCS[message_status]),
                                message_status)

    if message_type == EVKIT_MSG_SPI_RW_RESP:
        payload = message[3:]
        return (message_type, payload)

    elif message_type == EVKIT_MSG_READ_RESP:
        payload = message[3:]
        return (message_type, payload)

    elif message_type == EVKIT_MSG_VERSION_RESP:
        version_major, version_minor, board_id = message[3:6]
        return message_type, (version_major, version_minor, board_id)

    elif message_type == EVKIT_MSG_GPIO_STATE_RESP:
        gpio_pin, gpio_state = message[3:5]
        return message_type, (gpio_pin, gpio_state)

    elif message_type == EVKIT_MSG_GPIO_CONFIG_RESP:
        gpio_pin = message[3]
        return message_type, gpio_pin

    elif message_type == EVKIT_MSG_CREATE_MACRO_RESP:
        macro_id = message[3]
        return message_type, macro_id

    elif message_type == EVKIT_MSG_DEV_INFO_RESP:
        # this is for both device info and firmware sw id
        return message_type, message[3:]

    elif message_type == EVKIT_MSG_SELFTEST_RESP:
        return message_type, message[3:]

    elif message_type in (EVKIT_MSG_ADC_READ_RESP, EVKIT_MSG_ADC_READ2_RESP):
        return message_type, message[3:]

    elif message_type in [EVKIT_MSG_REMOVE_MACRO_RESP,
                          EVKIT_MSG_WRITE_RESP,
                          EVKIT_MSG_ADD_MACRO_ACTION_RESP,
                          EVKIT_MSG_START_MACRO_RESP,
                          EVKIT_MSG_STOP_MACRO_RESP,
                          EVKIT_MSG_CONFIGURE_RESP]:

        return message_type, None

    raise ProtocolException('Invalid response message received %s' % message)


def seconds_to_proto_time(seconds):
    """Convert seconds to RoKiX protocol time.

    The protocol only supports microsecond resolution for times. Any
    extra precision will be lost in the conversion.

    Due to protocol time limitations, the resolution will get worse the
    larger the time value is. For example, 100000.5 seconds is such a
    large value that it cannot be expressed as milliseconds in protocol
    time. The value will instead be expressed as 1000000 seconds. Such
    precision losses will always round towards zero.

    Args:
        seconds (float): Time to convert.

    Returns:
        Tuple[int, int]: ``(PROTO_TIME_UNIT, PROTO_TIME_VALUE)``
    """
    micros = int(seconds * 1e6)
    if micros < 1:
        raise ValueError(
            'protocol does not support times smaller than 1 microsecond')

    max_time_val = 2**16 - 1
    if micros <= max_time_val:
        unit = EVKIT_TIME_SCALE_US
        timeval = micros
    elif micros // 1000 <= max_time_val:
        unit = EVKIT_TIME_SCALE_MS
        timeval = micros // 1000
    elif micros // 1000000 <= max_time_val:
        unit = EVKIT_TIME_SCALE_S
        timeval = micros // 1000000
    elif micros // (1000000 * 60) <= max_time_val:
        unit = EVKIT_TIME_SCALE_M
        timeval = micros // (1000000 * 60)
    else:
        raise ValueError('time is too large for the protocol')

    return (unit, timeval)


class ProtocolEngine2(ProtocolEngine):
    def __init__(self, connection):
        ProtocolEngine.__init__(self, connection)
        self.version = 2
        self.EVKIT_MSG_ERROR_IND = EVKIT_MSG_ERROR_IND  # from kx_protocol_definition_2_x
