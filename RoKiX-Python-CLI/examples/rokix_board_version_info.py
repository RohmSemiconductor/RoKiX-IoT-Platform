# 
# Copyright 2018 Kionix Inc.
#
import imports  # pylint: disable=unused-import
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_exception import ProtocolException


def print_version_info():
    cm = ConnectionManager()
    print ('Protocol version   ' + cm.kx_adapter.fw_protocol_version)
    print ('Device UID         ' + ':'.join(['%02X' % t for t in cm.kx_adapter.get_dev_id()]))
    print ('Firmware version   ' + ''.join(['%02x' % t for t in cm.kx_adapter.get_firmware_id()]))

    try:
        # Bootloader version only on nRF based boards
        print ('Bootloader version ' + ''.join(['%02x' % t for t in cm.kx_adapter.get_bootloader_id()]))
    except ProtocolException:
        pass

    cm.disconnect()


if __name__ == '__main__':
    print_version_info()
