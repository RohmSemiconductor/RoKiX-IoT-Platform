# 
# Copyright 2018 Kionix Inc.
#
import os
import sys
import time
from datetime import datetime
import types
import traceback
from six import string_types

#
# Timing function definitions and selection based on OS
#


class TimingDaTetime(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.starttime = datetime.now()

    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return (datetime.now() - self.starttime).total_seconds()


class TimingTime(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.starttime = time.clock()

    def time_elapsed(self):
        "returns time elapsed in seconds with microsecond resolution"
        return time.clock() - self.starttime


# instance for timing class.
if sys.platform.startswith('win'):
    TIMING = TimingTime()  # windows
else:
    TIMING = TimingDaTetime()  # Linux

DELIMITER = ';\t'
NEW_LINE = '\n'


def timenow_str():
    return time.strftime('%Y-%m-%d %H:%M:%S:000')


def start_time_str():
    caller = 'NA'
    try:
        caller = os.path.split(traceback.extract_stack()[0][0])[1]
    except BaseException:
        caller = 'Error'
    return '# Log File Format Version = 1.0\n# Stream Configuration File = {}\n# Start time = {}'.format(caller, timenow_str())


def end_time_str():
    return '# End time = ' + timenow_str()


class SensorDataLogger(object):
    def __init__(self,
                 console=True,
                 log_file_name=None,
                 additional_info=None):
        self.console = console
        assert additional_info is None, 'Not implemented'  # TODO  3 additional_info
        self.count = 0
        self.channels = []
        self.file_handle = None

    # create file object form string or function which generates file name
        if isinstance(log_file_name, string_types):
            self.file_handle = open(log_file_name, 'w')

    # log_file_name is types.FunctionType if providing function which generates file name
        elif isinstance(log_file_name, types.FunctionType):
            self.file_handle = open(log_file_name(), 'w')

    def start(self):
        TIMING.reset()
        if self.console is True:
            print(start_time_str())
            for channel in self.channels:
                labels, number, _ = channel
                labels = labels.split('!')
                labels[0] = str(number)

                print('# timestamp%s%s' % (DELIMITER, DELIMITER.join(labels)))

    def stop(self):
        if self.console is True:
            print(end_time_str())

        if self.file_handle is not None:
            self.file_handle.close()

    def add_channel(self,
                    channel_dimension_labels,
                    channel_number=10,
                    channel_formatter=None):

        assert channel_dimension_labels.startswith('ch!')

        self.channels.append((channel_dimension_labels,
                              channel_number,
                              channel_formatter))

    def feed_values(self, data):
        # TODO 1 file logging, now done in kx_util by redirecting stdout to file
        # TODO 3 user delayedkeyboardinterrupt, otherwise end can happen in the middle of feed_values()
        self.count += 1
        now = TIMING.time_elapsed()
        if self.console is True:
            print('{:.6f}{}'.format(now, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in data))
