# 
# Copyright 2018 Kionix Inc.
#
import math
import imports  # pylint: disable=unused-import
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_util import evkit_config

from kx022 import kx022_data_logger
from kx022.kx022_driver import KX022Driver

from examples.rokix_sensor_node_gpio import RoKixSensorNode


class Algorithm(object):
    def __init__(self, connection_manager, stream):
        self.angle = 0
        self.led_state = 0
        self.stream = stream
        self.connection_manager = connection_manager

    def feed(self, data):
        channel, ax, ay, az = data

        del channel  # not used
        if abs(az) < 8000:
            self.angle = math.degrees(math.atan2(ax, ay))
            print('angle {}'.format(self.angle))
            if self.angle > 0:
                if self.led_state == 0:
                    self.led_state = 1
                    self.connection_manager.write_gpio_pin(RoKixSensorNode.LED_R, self.led_state)
            else:
                if self.led_state == 1:
                    self.led_state = 0
                    self.connection_manager.write_gpio_pin(RoKixSensorNode.LED_R, self.led_state)

        return True  # continue reading data stream


def read_with_stream(sensor_kx022, connection_manager):
    stream = kx022_data_logger.KX022DataStream(sensor_kx022)
    algorithm = Algorithm(connection_manager, stream)
    stream.read_data_stream(console=False, callback=algorithm.feed)
    return stream


def app_main():
    """

    """
    connection_manager = ConnectionManager(board_config_json='rokix_board_rokix_sensor_node_i2c.json')

    # make pin as input then green LED will be turned off
    connection_manager.read_gpio_pin(RoKixSensorNode.LED_G)
    connection_manager.read_gpio_pin(RoKixSensorNode.LED_Y)

    sensor_kx022 = KX022Driver()

    connection_manager.add_sensor(sensor_kx022)

    kx022_data_logger.enable_data_logging(sensor_kx022, odr=12.5)

    read_with_stream([sensor_kx022], connection_manager)

    sensor_kx022.set_power_off()

    # make pin as output
    connection_manager.write_gpio_pin(RoKixSensorNode.LED_G, 0)
    connection_manager.write_gpio_pin(RoKixSensorNode.LED_Y, 0)

    connection_manager.disconnect()


if __name__ == '__main__':
    print("Tilt detection demonstration application")
    print("This apllication connects to RoKiX Sensor node and reads accelerometer data.")
    print("Keep gravity on x-y axis and rotate the sensor node.")
    print("Tilt angle is printed to display.")
    print("If angle is positive then red LED is lit on sensor node.")
    print("Press CTRL+C to stop.")
    app_main()
