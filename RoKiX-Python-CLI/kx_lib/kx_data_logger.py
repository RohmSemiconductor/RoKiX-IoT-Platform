# 
# Copyright 2020 Rohm Semiconductor
#
import os
import time
import struct
import types
from array import array
import traceback
from six import string_types


from kx_lib.kx_configuration_enum import TIMER_POLL, REG_POLL
from kx_lib.kx_util import get_datalogger_config, evkit_config, get_timer, get_log_file_name
from kx_lib.kx_board import ConnectionManager
from kx_lib import kx_logger
LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class DataloggerBase(object):

    def __init__(self, sensors=None, kwargs_parser=get_datalogger_config):
        """
            sensors : list of sensor objects to be initialized. (Not instances!)
            odr : total ODR of all sensor (ODR is needed here to determine board power saving mode)
            args : global parameters
        """

        # override .cfg parameters in application if needed
        self.override_config_parameters()

        # override .cfg paramters with command line arguments
        if kwargs_parser:
            kwargs_parser()

        self.sensors = []
        self.sensor = None

        # ODR is needed here to determine board power saving mode
        self.connection_manager = ConnectionManager(
            odr=evkit_config.odr)
        self.stream = None

        # add sensors if sensor list given
        if sensors:
            for sensor in sensors:
                self.add_sensor(sensor())

            # reset the sensor so no any old settings are in place
            for sensor in self.sensors:
                sensor.por()

    def override_config_parameters(self):
        # .cfg parameters can be overriden here
        pass

    def add_sensor(self, sensor):
        self.sensors.append(sensor)
        self.connection_manager.add_sensor(sensor)

    def enable_data_logging(self, **kwargs):
        raise NotImplementedError()

    def make_reader_arguments(self, reader_arguments={}):

        if evkit_config.loop == 0:
            reader_arguments['loop'] = None
        else:
            reader_arguments['loop'] = evkit_config.loop

        if evkit_config.max_timeout_count == 0:
            reader_arguments['max_timeout_count'] = None
        else:
            reader_arguments['max_timeout_count'] = evkit_config.max_timeout_count

        return reader_arguments

    def read_with_polling(
            self,
            loop,
            hdr,
            console=True,
            callback=None,
            max_timeout_count=0):

        sensor = self.sensors[0]

        count = 0
        dl = SensorDataLogger(console=console)
        dl.add_channel(hdr)
        dl.start()
        try:
            while (loop is None) or (count < loop):
                count += 1
                sensor.drdy_function(timeout=max_timeout_count)
                data = sensor.read_data()
                data = [10] + data
                dl.feed_values(data)

                if callback is not None:
                    # callback function returns False if need to stop reading
                    if callback(data) is False:
                        break

        except KeyboardInterrupt:
            pass

        finally:
            dl.stop()

    def read_with_stream(self, stream_class, pin_index=None, reader_arguments={}):
        self.stream = stream_class(
            sensors=self.sensors,
            pin_index=pin_index,  # None = fetches pin_index from settings.cfg
            timer=None if evkit_config.drdy_function_mode != TIMER_POLL else evkit_config.drdy_timer_interval
        )
        self.stream.read_data_stream(**reader_arguments)

    def run(self, stream_class, pin_index=None, reader_arguments={}):
        "Read sensor data until stopped or loop count reached"

        if self.sensor:
            self.sensors = [self.sensor]
            LOGGER.error('Old way to use this class')
        try:
            reader_arguments = self.make_reader_arguments(reader_arguments)
            if evkit_config.stream_mode:
                self.read_with_stream(
                    stream_class,
                    pin_index,
                    reader_arguments=reader_arguments
                )
            else:
                self.read_with_polling(
                    hdr=stream_class.hdr,
                    **reader_arguments
                )
        finally:
            self.power_off()
            self.connection_manager.disconnect()

    def power_off(self):
        for sensor in self.sensors:
            sensor.set_power_off()
            # # reset the sensor so no any old settings are in place. Sensor goes to power off state
            # sensor.por()


class SingleChannelReader(DataloggerBase):
    pass


class SingleChannelEventReader(SingleChannelReader):
    def override_config_parameters(self):
        SingleChannelReader.override_config_parameters(self)
        evkit_config.max_timeout_count = None  # Waits events forever without bus2 timeout

    def read_with_polling(
            self,
            loop,
            fmt,
            hdr,
            reg,
            console=True,
            callback=None,
            max_timeout_count=0):

        sensor = self.sensors[0]

        count = 0
        dl = SensorDataLogger(console=console)
        dl.add_channel(hdr)
        dl.start()
        data_len = struct.calcsize(fmt)
        __channel = array('B', [10])

        try:
            while (loop is None) or (count < loop):
                count += 1
                sensor.asic_function(timeout=max_timeout_count)
                data = sensor.read_register(reg, data_len - 1)
                data = list(struct.unpack(fmt, __channel + data))
                dl.feed_values(data)

                if callback is not None:
                    # callback function returns False if need to stop reading
                    if callback(data) is False:
                        break

        except KeyboardInterrupt:
            pass

        finally:
            dl.stop()

    def read_with_stream(self, stream_class, pin_index=None, reader_arguments={}):

        self.stream = stream_class(
            sensors=self.sensors,
            pin_index=pin_index,  # None = fetches pin_index from settings.cfg
        )
        self.stream.read_data_stream(**reader_arguments)

    def run(self, stream_class, pin_index=None, reader_arguments={}):
        "Read sensor data until stopped or loop count reached"
        reader_arguments = self.make_reader_arguments(reader_arguments)
        try:
            if evkit_config.stream_mode:
                assert evkit_config.other_function_mode != REG_POLL, "Cannot use streaming and function mode REG_POLL"
                self.read_with_stream(
                    stream_class,
                    pin_index=pin_index,  # None = fetches pin_index from settings.cfg
                    reader_arguments=reader_arguments
                )

            else:
                self.read_with_polling(
                    fmt=stream_class.fmt,
                    hdr=stream_class.hdr,
                    reg=stream_class.reg,
                    **reader_arguments
                )
        finally:
            self.power_off()
            self.connection_manager.disconnect()


class MultiChannelReader(SingleChannelReader):
    def read_with_polling(self, sensor, loop, channels):
        raise NotImplementedError('Multiple streams not supported in polling mode. Use stream mode instead.')

    def run(self, stream_class, pin_index=None, reader_arguments={}):

        if not evkit_config.stream_mode:
            raise NotImplementedError('Multiple streams not supported in polling mode. Use stream mode instead.')

        SingleChannelReader.run(self, stream_class, pin_index, reader_arguments)

#
# Timing function definitions and selection based on OS
#


TIMING = get_timer()

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
        assert additional_info is None, 'Not implemented'
        self.count = 0
        self.channels = []
        self.file_handle = None
        # create file object form string or function which generates file name
        if log_file_name is None:
            log_file_name = get_log_file_name()
        if isinstance(log_file_name, string_types):
            self.file_handle = open(log_file_name, 'w')

        # log_file_name is types.FunctionType if providing function which generates file name
        elif isinstance(log_file_name, types.FunctionType):
            self.file_handle = open(log_file_name(), 'w')

    def start(self):
        TIMING.reset()
        start_msg = start_time_str()
        for channel in self.channels:
            labels = channel[0]
            start_msg += NEW_LINE + '# timestamp%s%s' % (DELIMITER, labels.replace('!', DELIMITER))
        if self.console is True:
            print(start_msg)
        if self.file_handle is not None:
            self.file_handle.write(start_msg + NEW_LINE)

    def stop(self):
        if self.console is True:
            print(end_time_str())

        if self.file_handle is not None:
            self.file_handle.write(end_time_str())
            self.file_handle.close()

    def add_channel(self,
                    channel_dimension_labels,
                    channel_number=10,
                    channel_formatter=None):

        self.channels.append((channel_dimension_labels,
                              channel_number,
                              channel_formatter))

    def feed_values(self, data):
        self.count += 1
        now = TIMING.time_elapsed()
        data = '{:.6f}{}'.format(now, DELIMITER) + DELIMITER.join('{:d}'.format(t) for t in data)
        if self.console is True:
            print(data)
        if self.file_handle is not None:
            self.file_handle.write(data + NEW_LINE)
