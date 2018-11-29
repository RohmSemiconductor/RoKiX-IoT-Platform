# 
# Copyright 2018 Kionix Inc.
#
import sys
import os
import time
import array
import argparse
import configparser
import signal
import six
import logging

from kx_lib import kx_logger
from kx_lib.kx_configuration_enum import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_exception import EvaluationKitException
assert True in [six.PY2, six.PY3], "Unsupported python version"

evkit_config = configparser.RawConfigParser()
# try to find cfg from different locations
_RESULT = evkit_config.read(
    ['../../rokix_settings.cfg', '../rokix_settings.cfg', 'rokix_settings.cfg'])
assert _RESULT != [], "rokix_settings.cfg not found"
assert evkit_config.getint('root', 'version') == 2, 'Not supported configuration file version'

# set up global logging level if level is defined in config file
if evkit_config.has_option('generic', 'logging_level'):
    LEVEL = {
        'DEBUG':logging.DEBUG,
        'INFO':logging.INFO,
        'WARNING':logging.WARNING,
        'ERROR':logging.ERROR,
        'CRITICAL':logging.CRITICAL,
    }
    logging.getLogger().setLevel(LEVEL[evkit_config.get('generic', 'logging_level')])
else:
    # default level
    logging.getLogger().setLevel(logging.ERROR)


LOGGER = kx_logger.get_logger(__name__)
LOGGER.info('Configurations read from from {}.'.format(_RESULT[0]))

def delay_seconds(seconds):
    time.sleep(seconds)


# convert int and float to string which is used in enumerated values dictionaries


def convert_to_enumkey(value):
    "Hepler function for using enum values in register_definition files"

    # covert 100.0 to 100 etc
    if isinstance(value, float):
        if value == int(value):
            value = int(value)

    if isinstance(value, int):
        value = str(value)
    elif isinstance(value, float):
        value = str(value)
        value = value.replace('.', 'P')
    elif isinstance(value, str):
        value = value.replace('p', 'P')
    else:
        assert 0, 'Invalid enumkey'
    return value


def get_datalogger_args(sensor_driver=None):
    argparser = argparse.ArgumentParser(description='Example: %(prog)s -s')
    argparser.add_argument('-l', '--loop', default=None, type=int, help='How many samples to read in loop (default None = infinite loop).')
    argparser.add_argument('-s', '--stream_mode', action='store_true', help='Data stream mode with data ready interrupt trigger')
    argparser.add_argument('-t', '--timer_stream_mode', action='store_true', help='Data stream mode with timer trigger')
    argparser.add_argument('-f', '--filename_prefix', default=None, type=str,
                           help='Filename prefix for log file where to log data. Each file name has uniqe number after prefix.')
    argparser.add_argument('-b', '--board', default=None, type=str, help='Override board setting from settings.cfg')
    argparser.add_argument('-o', '--odr', default=None, type=float, help='Override default(25Hz) data logger ODR.')
    argparser.add_argument('-c', '--com_port', default=None, type=str, help='Override com port setting from settings.cfg')
    argparser.add_argument('-d', '--drdy_operation', default=None, type=str, help='Override drdy_operation setting from settings.cfg')

    # TODO 2 enable_data_logging parameters as kwargs
    # TODO 2 override setting.cfg with kwargs. -t overrides drdy_poll_interval

    args = argparser.parse_args()

    if args.board:
        assert os.path.isfile(args.board), 'File "%s" not found' % args.board
        evkit_config.set('configuration', 'board', args.board)

    if args.odr:
        evkit_config.set('generic', 'drdy_poll_interval', 1000. / args.odr)

    if args.com_port:
        evkit_config.set('bus2_settings', 'serial_port', args.com_port)

    if args.drdy_operation:
        evkit_config.set('generic', 'drdy_operation', args.drdy_operation)

    # find next available file name
    if args.filename_prefix is not None:
        fname = args.filename_prefix
        name, extension = os.path.splitext(fname)
        i = 0
        while True:
            if os.path.isfile(fname):
                fname = '{}_{:05d}{}'.format(name, i, extension)
                i += 1
            else:
                # NOTE: stdout is redirected to file "fname"
                LOGGER.debug('Logging to file %s' % fname)
                sys.stdout = open(fname, 'w')
                break

    if args.stream_mode and sensor_driver:
        stream_config_check(sensor_driver)

    return args


def stream_config_check(sensor_driver):

#   sensor is not yet assigned to board so not possible to check does the board support streaming
#    if sensor_driver.connection_manager.kx_adapter.engine is None:
#        raise EvaluationKitException('Selected board does not support data streaming.')

    # TODO 2 consider  improving logic of stream_config_check
    "Verify that needed settings are in place when streaming mode is used"
    if sensor_driver.sensor_type in [
            SENSOR_TYPE_DIGITAL_1D,
            SENSOR_TYPE_DIGITAL_2D,
            SENSOR_TYPE_DIGITAL_3D]:

        if (evkit_config.get('generic', 'drdy_operation') not in ['ADAPTER_GPIO1_INT', 'ADAPTER_GPIO2_INT']):
            raise EvaluationKitException('Stream mode requires GPIO drdy_operation in settings.cfg')

    return True


#
# DelayedKeyboardInterrupt is needed to handle ctrl+C properly during communication to firmware
#
# http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-being-interrupted-by-keyboardinterrupt-in-py


class DelayedKeyboardInterrupt(object):
    def __enter__(self):
        self.signal_received = False  # pylint: disable=attribute-defined-outside-init
        self.old_handler = signal.getsignal(signal.SIGINT)  # pylint: disable=attribute-defined-outside-init
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)  # pylint: disable=attribute-defined-outside-init
        LOGGER.debug('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, signal_type, signal_value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)


def to_hex_str(data):
    return ' '.join(['0x%02x' % ord(_t) for _t in data])


def bin2uint16(data):
    return data[0] | data[1] << 8


def bin2uint8(data):
    if isinstance(data, array):
        data = data[0]
    return data

def get_pin_index():
    "Returns 1 if drdy_operation == 'ADAPTER_GPIO1_INT' and 2 if it is ADAPTER_GPIO2_INT "
    drdy = evkit_config.get('generic', 'drdy_operation')
    if drdy == 'ADAPTER_GPIO1_INT':
        pin_index = 1
    elif drdy == 'ADAPTER_GPIO2_INT':
        pin_index = 2
    else:
        raise EvaluationKitException(
            'drdy_operation is configured to %s. Please select "ADAPTER_GPIO1_INT" or "ADAPTER_GPIO2_INT" instead'\
             % drdy)

    return pin_index
