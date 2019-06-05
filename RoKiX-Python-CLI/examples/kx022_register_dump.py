# 
# Copyright 2018 Kionix Inc.
#
""" Reads and prints sensor register content """
import imports  # pylint: disable=unused-import
from kx_lib.kx_board import ConnectionManager
from kx022.kx022_driver import KX022Driver


def main():
    sensor = KX022Driver()
    cm = ConnectionManager()
    cm.add_sensor(sensor)
    sensor.register_dump()


if __name__ == '__main__':
    main()
