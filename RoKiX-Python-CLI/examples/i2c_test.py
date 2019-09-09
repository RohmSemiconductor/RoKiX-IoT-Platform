# 
# Copyright 2018 Kionix Inc.
#
# test i2c bus on rokix sensor node by reading and writing register values from/to kx122 which is on the sensor node main board
import imports
from kx_lib.kx_board import ConnectionManager


def i2c_multiread_write_Test():
    i2c_target = 4  # i2c bus on rokix sensor node
    i2c_sad = 31  # kx122

    connection_manager = ConnectionManager(board_config_json='rokix_board_rokix_sensor_node_i2c.json')
    length = 4
    start_address = 0x18

    connection_manager.kx_adapter.adapter_write_sensor_register_i2c(i2c_target, i2c_sad, start_address, [1] * length)
    print(connection_manager.kx_adapter.adapter_read_sensor_register_i2c(i2c_target, i2c_sad, start_address, length))
    connection_manager.kx_adapter.adapter_write_sensor_register_i2c(i2c_target, i2c_sad, start_address, [2] * length)
    print(connection_manager.kx_adapter.adapter_read_sensor_register_i2c(i2c_target, i2c_sad, start_address, length))

    connection_manager.disconnect()


i2c_multiread_write_Test()
