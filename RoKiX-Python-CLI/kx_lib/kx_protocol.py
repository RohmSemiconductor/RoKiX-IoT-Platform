# 
# Copyright 2018 Kionix Inc.
#
# pylint: disable=duplicate-code
from array import array
import struct
from kx_lib.kx_exception import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_protocol_definition import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_configuration_enum import MAX_PACKET_SIZE
import kx_lib.kx_logger as kx_logger
LOGGER = kx_logger.get_logger(__name__)

# LOGGER.setLevel(kx_logger.DEBUG)

#
# request message packing
#


def reset_req(reset_type=EVKIT_RESET_SOFT):
    assert reset_type in [EVKIT_RESET_SOFT, EVKIT_RESET_HARD]
    msg = KxMessageContainer(EVKIT_MSG_RESET_REQ)
    msg.append_payload(reset_type)
    return msg.get_message()


def write_req(_, sad, register, value):
    msg = KxMessageContainer(EVKIT_MSG_WRITE_REQ)
    msg.append_payload(sad)
    msg.append_payload(register)
    if value is not None:  # only one byte write
        msg.append_payload(value)
    return msg.get_message()


def read_req(_, sad, register, length=1):
    msg = KxMessageContainer(EVKIT_MSG_READ_REQ)
    msg.append_payload([sad, register, length])
    return msg.get_message()


def version_req():
    msg = KxMessageContainer(EVKIT_MSG_VERSION_REQ)
    return msg.get_message()


def gpio_state_req(gpio_nrb):
    msg = KxMessageContainer(EVKIT_MSG_GPIO_STATE_REQ)
    msg.append_payload(gpio_nrb)
    return msg.get_message()


def interrupt_disable_req(pin,
                          sense=EVKIT_GPIO_PIN_SENSE_LOW,
                          pull=EVKIT_GPIO_PIN_PULLUP):

    msg = KxMessageContainer(EVKIT_MSG_DISABLE_INT_REQ)
    msg.append_payload(pin)
    msg.append_payload(sense)
    msg.append_payload(pull)
    return msg.get_message()


def interrupt_enable_req(pin,
                         payload_definition,
                         sense=EVKIT_GPIO_PIN_SENSE_LOW,
                         pull=EVKIT_GPIO_PIN_PULLUP):

    msg = KxMessageContainer(EVKIT_MSG_ENABLE_INT_REQ)
    msg.append_payload(pin)
    msg.append_payload(sense)
    msg.append_payload(pull)
    msg.append_payload(payload_definition)
    if len(payload_definition) % 3 != 0:
        raise ProtocolException('payload definition must be in format (sad,reg,len)*n')
    return msg.get_message()


# Default configuration is input with disconnect, high-z


def gpio_config_req(
        pin,
        direction=EVKIT_GPIO_PIN_INPUT,
        input_connected=EVKIT_GPIO_PIN_DISCONNECTED,
        io_config=EVKIT_GPIO_PIN_NOPULL):
    msg = KxMessageContainer(EVKIT_MSG_GPIO_CONFIG_REQ)
    msg.append_payload(pin)
    msg.append_payload(direction)
    msg.append_payload(input_connected)
    msg.append_payload(io_config)
    return msg.get_message()


#
# response message unpacking
#


def _check_response_status(message_status):
    if message_status == EVKIT_BUS1_ERROR:
        raise ProtocolBus1Exception()

    if message_status != EVKIT_SUCCESS:
        raise ProtocolException('Error message received %d' % message_status)


class KxMessageContainer(object):
    "Class for creating content for kionix protocol message"

    def __init__(self, message_type, max_len=MAX_PACKET_SIZE):
        self.message_type = message_type
        self.len = 2
        self.payload = array('B')
        self.max_len = max_len

    def __repr__(self):
        return str(self.payload)

    def append_payload(self, data):
        "accepts int8 or string lenght of 1 or more"
        if isinstance(data, array):
            self.payload += data
            self.len += len(data)

        elif isinstance(data, int):
            self.payload += array('B', [data])
            self.len += 1

        elif isinstance(data, list):
            self.payload += array('B', data)
            self.len += len(data)

        else:
            raise ProtocolException('Invalid value for message payload.')

    def append_payload16bit(self, data):  # unsigned int 16bit
        #LOGGER.warning("deprecated %s", DeprecationWarning)
        if isinstance(data, int):
            self.payload += array('B', struct.pack('>H', data))
            self.len += 2
        else:
            raise ProtocolException('Invalid value for message append_payload16bit')

    def get_message(self):
        "Returns created message as binary string"
        message = array('B', [self.len, self.message_type])
        message += self.payload
        if len(message) > self.max_len:
            raise ProtocolException('Message too long')

        return message


def unpack_response_data(message):
    # convert string to list of int8
    LOGGER.debug('Received message : %s' % message)
    message_type = message[1]

    if message_type in [EVKIT_MSG_READ_RESP, EVKIT_MSG_WRITE_RESP]:
        # message_sad = message[2] # not used
        # message_register = message[3] # not used
        message_status = message[4]
        _check_response_status(message_status)

        if message_type == EVKIT_MSG_READ_RESP:
            message_payload = message[5:]
            return message_type, message_payload

    elif message_type in [EVKIT_MSG_VERSION_RESP]:
        message_status = message[2]
        _check_response_status(message_status)

        message_major_version = message[3]
        message_minor_version = message[4]
        return message_type, (message_major_version, message_minor_version)

    elif message_type in [EVKIT_MSG_ENABLE_INT_RESP]:
        message_stream_id = message[2]
        message_status = message[3]
        _check_response_status(message_status)
        return message_type, message_stream_id

    elif message_type in [EVKIT_MSG_DISABLE_INT_RESP]:
        message_status = message[2]
        _check_response_status(message_status)

    elif message_type in [EVKIT_MSG_GPIO_STATE_RESP]:
        # message_stream_gpio_ind = message[2] # not used
        message_stream_gpio_state = message[3]
        message_status = message[4]
        _check_response_status(message_status)
        # None used here to match return data type with v2
        return message_type, (None, message_stream_gpio_state)

    elif message_type in [EVKIT_MSG_GPIO_CONFIG_RESP]:
        message_status = message[6]
        _check_response_status(message_status)

    elif message_type in [EVKIT_MSG_INTERRUPT_IND1,
                          EVKIT_MSG_INTERRUPT_IND2,
                          EVKIT_MSG_INTERRUPT_IND3,
                          EVKIT_MSG_INTERRUPT_IND4]:

        message_payload = message[1:]

        return message_type, message_payload

    elif message_type in [EVKIT_MSG_ERROR_IND]:
        message_status = message[2]
        raise ProtocolException('Request failed. Error response code %d' % message_status)
        # return message_type, message_status

    else:
        raise ProtocolException('Unknown message received 0x%02x' % message_type)

    return message_type


class ProtocolEngine(object):
    "Class for sending, receiving and interpreting evaluation kit protocol messages"

    def __init__(self, connection):
        "Connection = instance of kx_connection"
        self.connection = connection
        self.message_fifo = []
        self.max_retry_count = 2  # max_retry_count
        self.max_fifo_size = 1000  # max_fifo_size
        self.EVKIT_MSG_ERROR_IND = EVKIT_MSG_ERROR_IND  # from kx_protocol_definition
        self.version = 1

    def __pyreverse(self):
        # not used just for pyreverse
        self.container = KxMessageContainer  # pylint: disable=attribute-defined-outside-init

    def send_message(self, data):
        self.connection.write(data)

    def get_message_type(self, message):
        return message[1]

    def receive_single_message(self, wait_for_message=None, cache_messages=True):
        """Receive message from bus.

        Receive message. If message type is defined in wait_for_message argument
        then it can be selected wether to store messages (cache_messages) received
        before receiving the message what is waited.

        Keyword arguments:

        wait_for_message -- which message to wait. (Default None, e.g. accept
                            first message which is received.

        cache_messages -- Store received messages to FIFO if other than
                            expected message (defined in wait_for_message)
                            is received (default True)

        """
        retry_count = self.max_fifo_size  # max size of FIFO

        # check if wanted message already received and can be found from FIFO
        if self.message_fifo:  # if len > 0
            for fifo_index in range(len(self.message_fifo)):
                received_message = self.message_fifo[fifo_index]

                if wait_for_message is None or \
                   self.get_message_type(received_message) == wait_for_message:
                    self.message_fifo.pop(fifo_index)  # remove this message from fifo
                    return received_message

        # continue to receive new messages if wanted message was not in FIFO
        while retry_count:
            received_message = self._receive_single_message()
            if wait_for_message is None or \
               self.get_message_type(received_message) == wait_for_message:
                return received_message

            # not an error message?
            elif self.get_message_type(received_message) != self.EVKIT_MSG_ERROR_IND:
                retry_count -= 1

                # store message to FIFO
                if cache_messages:
                    self.message_fifo.append(received_message)

            else:
                # handle error message
                message_status = ord(received_message[2])
                raise ProtocolException('Error message received. Error id %d' % message_status)

        raise ProtocolException('Message FIFO full')

    def _receive_single_message(self):
        received_message = array('B')
        partial_message = array('B')
        retry_count = self.max_retry_count
        #BLE_PYGATT returns strings, windows
        length_byte = array('B',  [ord(self.connection.read(1))])
        if not length_byte:
            raise ProtocolTimeoutException('Timeout on message receiving 1.')

        message_length = length_byte[0] - 1  # -1 since length takes 1 byte
        while retry_count:
            partial_message = self.connection.read(message_length - len(partial_message))
            retry_count -= 1
            if isinstance(partial_message, str):
                partial_message = [ord(msg_item) for msg_item in partial_message]
            received_message += array('B', partial_message)
            if len(partial_message) == message_length:
                if len(received_message) < 1:
                    raise ProtocolBus2Exception("No data received.")

                return length_byte + received_message

        raise ProtocolTimeoutException('Timeout on message receiving 2.')
