# 
# Copyright 2018 Kionix Inc.
#
import sys
import os
import time  # pylint: disable=unused-import
from datetime import datetime  # pylint: disable=unused-import
import array
import signal
import logging
import argparse
import six

from kx_lib import kx_logger
from kx_lib.kx_configuration_enum import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_options import EvkitConfigurations
assert True in [six.PY2, six.PY3], "Unsupported python version"

evkit_config = EvkitConfigurations()
# set up global logging level if level is defined in config file
if evkit_config.has_option('logging_level'):
    LEVEL = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    logging.getLogger().setLevel(LEVEL[evkit_config.logging_level])
else:
    # default level
    logging.getLogger().setLevel(logging.ERROR)


LOGGER = kx_logger.get_logger(__name__)
LOGGER.info('Configurations read from from {}.'.format(evkit_config.config_file))


def delay_seconds(seconds):
    time.sleep(seconds)

#
# Timing function definitions and selection based on OS
#


class Timing_datetime:
    def __init__(self):
        self.reset()

    def reset(self):
        self.starttime = datetime.now()

    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return (datetime.now() - self.starttime).total_seconds()


class Timing_time:
    def __init__(self):
        # time.clock() has been deprecated since Python 3.3 and is removed in
        # Python 3.8. The replacements are not available in Python 2, which is
        # why time.clock() is used on it.
        if sys.version_info.major == 3:
            self._time = time.perf_counter  # pylint: disable=no-member
        elif sys.version_info.major == 2:
            self._time = time.clock
        else:
            raise RuntimeError("unexpected Python major version")

        self.reset()

    def reset(self):
        self.starttime = self._time()

    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return self._time() - self.starttime


def get_timer():
    # instance for timing class.
    if sys.platform.startswith('win'):
        timing = Timing_time()  # windows
    else:
        timing = Timing_datetime()  # Linux

    return timing

# convert int and float to string which is used in enumerated values dictionaries


def get_datalogger_config():

    evkit_config.parse_args()
    return evkit_config


def get_log_file_name():
    # find next available file name
    if evkit_config.has_option('log_file'):
        fname = evkit_config.log_file
        LOGGER.debug('Logging to file %s' % fname)
        return evkit_config.log_file
    if evkit_config.filename:
        fname = evkit_config.filename
        name, extension = os.path.splitext(fname)
        if not extension:
            extension = '.csv'
        fname = name + extension
        i = 0
        while True:
            if os.path.isfile(fname):
                fname = '{}_{:05d}{}'.format(name, i, extension)
                i += 1
            else:
                LOGGER.debug('Logging to file %s' % fname)
                return fname


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
        assert 0, 'Invalid enumkey "%s"' % value
    return value

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


def get_drdy_pin_index():
    "Returns 1 if drdy_function_mode == 'ADAPTER_GPIO1_INT' and 2 if it is ADAPTER_GPIO2_INT "
    drdy = evkit_config.drdy_function_mode
    if drdy == ADAPTER_GPIO1_INT:
        pin_index = 1
    elif drdy == ADAPTER_GPIO2_INT:
        pin_index = 2
    elif drdy == TIMER_POLL:
        pin_index = None
    else:
        raise EvaluationKitException(
            'drdy_function_mode is configured to %s. Please select "ADAPTER_GPIO1_INT" or "ADAPTER_GPIO2_INT" instead'
            % drdy)
    return pin_index


def get_drdy_timer():
    drdy = evkit_config.drdy_function_mode
    if drdy == TIMER_POLL:
        return evkit_config.drdy_timer_interval
    return None


def get_other_timer():
    other_f = evkit_config.other_function_mode
    if other_f == TIMER_POLL:
        return evkit_config.other_timer_interval
    return None


def get_other_pin_index():
    "Returns 1 if other_function_mode == 'ADAPTER_GPIO1_INT' and 2 if it is ADAPTER_GPIO2_INT "
    other_f = evkit_config.other_function_mode
    if other_f == ADAPTER_GPIO1_INT:
        pin_index = 1
    elif other_f == ADAPTER_GPIO2_INT:
        pin_index = 2
    elif other_f == TIMER_POLL:
        pin_index = None
    else:
        raise EvaluationKitException(
            'other_function_mode is configured to %s. Please select "ADAPTER_GPIO1_INT" or "ADAPTER_GPIO2_INT" instead'
            % other_f)
    return pin_index


def adc_conv(raw, bits=12, gain=1.0, refv=0.6, divider=1):
    # raw      = digits in 2's complement
    # bits     = adc's resolution
    # gain     = adc's front end gain
    # refv     = adc's reference voltage
    # divider  = external input voltage divider
    return raw / ((gain / refv) * 2**bits) / divider