# 
# Copyright 2020 Rohm Semiconductor
#
import json
import struct

from kx_lib.kx_util import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_configuration_enum import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_exception import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_stream import StreamConfig, RequestMessageDefinition
from kx_lib.kx_sensor_base import AxisMapper
import kx_lib.kx_protocol_definition_2_x as protocol

LOGGER = kx_logger.get_logger(__name__)


class StandAloneConnectionManager(ConnectionManager):
    def __init__(self):
        if not os.path.isfile(evkit_config.board):
            # rokix_settings.cfg adds ../ to board configs
            # manually override this as cmd argument to assure board is selected properly
            evkit_config.board = evkit_config.board.lstrip('../')
        super(StandAloneConnectionManager, self).__init__(evkit_config.board)
        for target in self.board_config['configuration']['bus1']['targets']:
            for sensor_name, sensor_info in target['parts'].items():
                self.found_sensors[sensor_name] = {}
                self.found_sensors[sensor_name].update({key: value for key, value in target.items() if key != 'parts'})
                self.found_sensors[sensor_name].update(self.board_config['configuration']['bus1']['sensor_defaults'])
                self.found_sensors[sensor_name].update(sensor_info)

    def write_sensor_register_by_name(self, sensor_name, bus1_name, register, values):

        assert bus1_name in [BUS1_I2C, BUS1_SPI], 'Invalid bus1 name'
        target = self.found_sensors[sensor_name][CFG_TARGET]
        if bus1_name == BUS1_I2C:
            sad = self.found_sensors[sensor_name][CFG_SAD]

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_write_sensor_register_i2c(target, sad, register, values)

        elif bus1_name == BUS1_SPI:
            cs = self.found_sensors[sensor_name][CFG_CS]

            if self.found_sensors[sensor_name][CFG_SPI_PROTOCOL] == 1:
                # When using SPI, Kionix sensors require that the address' MSB is
                # cleared to indicate that this is a write.
                register &= ~(1 << 7)

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_write_sensor_register_spi(target, cs, register, values)

        else:
            raise EvaluationKitException('Unable write data to sensor register.')

    def get_physical_pin_for_sensor(self, sensor, pin=1):
        sensor_resource = self.found_sensors[sensor]

        if isinstance(pin, int):
            return sensor_resource[INT_GPIO_DICT[pin]]
        elif isinstance(pin, list):
            return [sensor_resource.get(ADC_GPIO_DICT[ind]) for ind in ADC_GPIO_DICT]

        raise EvaluationKitException('Invalid data type for "pin".')


class StandAloneStreamMessageDefinition(RequestMessageDefinition):
    def __init__(self, fmt, hdr, axis_map):
        self.msg_fmt = fmt
        self.msg_hdr = hdr
        self.msg_size = struct.calcsize(self.msg_fmt)
        self.axis_mapper = AxisMapper(channel_header=hdr, axis_map=None)

class StandAloneDataStream(StreamConfig):
    def __init__(self, stream_config_json):
        with open(stream_config_json) as stream_config:
            LOGGER.debug('Loading stream config %s' % stream_config_json)
            self.stream_config = json.load(stream_config)
        self.board = StandAloneConnectionManager()
        self.msg_ind_dict = {}
        self.adapter = self.board.kx_adapter
        self.stream_start_msgs = []
        self.sensor_id = None
        if self.adapter.stream_support is False:
            raise EvaluationKitException("Adapter %s does not support data streaming." % self.adapter)

        for section in ['configure', 'activate']:
            for register_write_node in self.stream_config[section]:
                sensor_name, addr, value, _ = register_write_node
                assert sensor_name in self.board.found_sensors.keys(), 'Sensor not found %s' % sensor_name
                self.board.write_sensor_register_by_name(sensor_name, self.board.found_sensors[sensor_name][CFG_NAME], addr, value)

        if self.stream_config['structure_version'] == "3.0":
            self._define_request_message = self._define_request_message_structure_v3
            self._start_streaming = self._start_streaming_multi_sensor
            self._stop_streaming = self._stop_streaming_multi_sensor
        else:
            self._define_request_message = self._define_request_message_structure_v2
            self._start_streaming = self._start_streaming_single_sensor
            self._stop_streaming = self._stop_streaming_single_sensor
        self._define_request_message()

    def _define_request_message_structure_v2(self):
        LOGGER.debug('>_define_request_message')
        messages = self.stream_config['start_req']['msg']
        found_sensors = self.board.found_sensors
        for msg in messages:
            if any(isinstance(_byte, list) for _byte in msg):
                formatted_msg = []
                for list_item in msg:
                    if isinstance(list_item, list):
                        self.sensor_id = list_item[0]
                        LOGGER.debug('Stream request for %s' % self.sensor_id)
                        sensor_addr_key = CFG_CS if found_sensors[self.sensor_id][CFG_NAME] == BUS1_SPI else CFG_SAD
                        list_item[0] = found_sensors[self.sensor_id][sensor_addr_key]
                        formatted_msg.extend(list_item)
                    else:
                        formatted_msg.append(list_item)
                if self.sensor_id is not None:
                    formatted_msg[5] = found_sensors[self.sensor_id][CFG_TARGET]
                    if found_sensors[self.sensor_id][CFG_NAME] == BUS1_SPI:
                        if found_sensors[self.sensor_id][CFG_SPI_PROTOCOL] == 1:
                            formatted_msg[7] = formatted_msg[7] | 1 << 7
                msg = formatted_msg

            if msg[1] == protocol.EVKIT_MSG_CREATE_MACRO_REQ and msg[2] == 0:
                if self.sensor_id is not None:
                    msg[3] = found_sensors[self.sensor_id][INT1_GPIO]

            self.stream_start_msgs.append(msg)
        LOGGER.debug('<_define_request_message')

    def _define_request_message_structure_v3(self):
        LOGGER.debug('>_define_request_message')
        create_macro_req_handled = False
        create_macro_req_msg = []
        sensor_id = None

        for start_req in self.stream_config['start_req']:
            for msg in start_req['msg']:
                if any(isinstance(_byte, list) for _byte in msg):
                    #  If list inside the payload it needs to be flattened to the payload
                    add_macro_action_msg = []
                    for list_item in msg:
                        if isinstance(list_item, list):
                            # Swap sensor id to sensor addr(SPI CS or I2C ADDR) and append every item to the payload
                            sensor_id = list_item[0]
                            LOGGER.debug('Stream request for %s' % sensor_id)
                            sensor_addr_key = CFG_CS if self.board.found_sensors[sensor_id][CFG_NAME] == BUS1_SPI else CFG_SAD
                            list_item[0] = self.board.found_sensors[sensor_id][sensor_addr_key]
                            add_macro_action_msg.extend(list_item)
                        else:
                            add_macro_action_msg.append(list_item)

                    add_macro_action_msg[5] = self.board.found_sensors[sensor_id][CFG_TARGET]
                    if self.board.found_sensors[sensor_id][CFG_NAME] == BUS1_SPI:
                        if self.board.found_sensors[sensor_id][CFG_SPI_PROTOCOL] == 1:
                            add_macro_action_msg[7] = add_macro_action_msg[7] | 1 << 7

                    # Generate message_info object for read_data_stream to be able to parse incoming stream msgs
                    message_info = StandAloneStreamMessageDefinition(start_req['fmt'],
                                                                     start_req['hdr'],
                                                                     self.board.found_sensors[sensor_id][CFG_AXIS_MAP])

                if msg[1] == protocol.EVKIT_MSG_CREATE_MACRO_REQ:
                    # Wait for sensor_id to be resolved, should be the following message
                    create_macro_req_msg = msg
                    create_macro_req_handled = False

                elif not create_macro_req_handled and sensor_id is not None:

                    # Send EVKIT_MSG_CREATE_MACRO_REQ and catch exception if GPIO is already in use and use second one
                    if create_macro_req_msg[2] == protocol.EVKIT_MACRO_TYPE_INTR:
                        try:
                            create_macro_req_msg[3] = self.board.found_sensors[sensor_id][INT1_GPIO]
                            self.adapter.send_message(create_macro_req_msg)
                            _, channel_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
                        except ProtocolException:
                            create_macro_req_msg[3] = self.board.found_sensors[sensor_id][INT2_GPIO]
                            self.adapter.send_message(create_macro_req_msg)
                            _, channel_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
                        self.msg_ind_dict[channel_id] = message_info
                    else:
                        self.adapter.send_message(create_macro_req_msg)
                        _, channel_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)
                        self.msg_ind_dict[channel_id] = message_info

                    # Send EVKIT_MSG_ADD_MACRO_ACTION_REQ
                    self.adapter.send_message(add_macro_action_msg)
                    resp = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
                    LOGGER.debug(resp)

                    # Clear variables since macro actions for given sensor are handled
                    sensor_id = None
                    message_info = None
                    create_macro_req_handled = True
                elif msg[1] == protocol.EVKIT_MSG_ADD_MACRO_ACTION_REQ:
                    # Send EVKIT_MSG_ADD_MACRO_ACTION_REQ, there can be several
                    self.adapter.send_message(add_macro_action_msg)
                    resp = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
                    LOGGER.debug(resp)

                elif msg[1] == protocol.EVKIT_MSG_START_MACRO_REQ:
                    # Send start macro's in _start_streaming
                    self.stream_start_msgs.append(msg)
                else:
                    # Send everything else
                    LOGGER.debug(msg)
                    self.adapter.send_message(msg)
                    resp = self.adapter.receive_message(wait_for_message=msg[1] + 1)  # Macor resp is macro req + 1
                    LOGGER.debug(resp)
        LOGGER.debug('<_define_request_message')

    def _start_streaming_single_sensor(self):
        LOGGER.debug(">_start_streaming")
        for stream_start_msg_bytes in self.stream_start_msgs:
            LOGGER.debug(stream_start_msg_bytes)
            self.adapter.send_message(stream_start_msg_bytes)
            resp = self.adapter.receive_message(wait_for_message=stream_start_msg_bytes[1] + 1)
            if stream_start_msg_bytes[1] == protocol.EVKIT_MSG_CREATE_MACRO_REQ:
                _, resp_payload = resp
                message_info = StandAloneStreamMessageDefinition(self.stream_config['start_req']['fmt'],
                                                                 self.stream_config['start_req']['hdr'],
                                                                 self.board.found_sensors[self.sensor_id][CFG_AXIS_MAP])

                self.msg_ind_dict[resp_payload] = message_info
        LOGGER.debug("<_start_streaming")

    def _stop_streaming_single_sensor(self):
        stop_req = self.stream_config['stop_req']['msg']
        LOGGER.debug(stop_req)
        self.adapter.send_message(stop_req)
        result = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_REMOVE_MACRO_RESP)
        LOGGER.debug(result)

    def _start_streaming_multi_sensor(self):
        LOGGER.debug(">_start_streaming")
        for stream_start_msg in self.stream_start_msgs:
            LOGGER.debug(stream_start_msg)
            self.adapter.send_message(stream_start_msg)
            resp = self.adapter.receive_message(wait_for_message=stream_start_msg[1] + 1)
            LOGGER.debug(resp)

        LOGGER.debug("<_start_streaming")

    def _stop_streaming_multi_sensor(self):
        for stop_req in self.stream_config['stop_req']:
            LOGGER.debug(stop_req)
            self.adapter.send_message(stop_req)
            result = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_REMOVE_MACRO_RESP)
            LOGGER.debug(result)
        for deactivate_msg in self.stream_config['deactivate']:
            sensor_name, addr, value, _ = deactivate_msg
            self.board.write_sensor_register_by_name(
                sensor_name, self.board.found_sensors[sensor_name][CFG_NAME], addr, value)


def app_main():
    evkit_config.add_argument('stream_config', type=str)
    args = get_datalogger_config()
    stream = StandAloneDataStream(args.stream_config)
    stream.read_data_stream(args.loop)


if __name__ == '__main__':
    app_main()
