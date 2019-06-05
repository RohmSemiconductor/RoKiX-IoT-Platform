# 
# Copyright 2018 Kionix Inc.
#
import os
import json
from kx_lib.kx_configuration_enum import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_bus2 import KxComPort, KxSocket, KxWinBLE, KxLinuxBLE, KxLinuxI2C
from kx_lib.kx_adapter_aardvark import KxAdapterAardvark
from kx_lib.kx_adapter_evk import KxAdapterEvk
from kx_lib.kx_exception import *  # pylint: disable=unused-wildcard-import,wildcard-import
from kx_lib.kx_util import DelayedKeyboardInterrupt, evkit_config

from kx_lib import kx_logger
LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.INFO)
# LOGGER.setLevel(kx_logger.DEBUG)
# LOGGER.setLevel(kx_logger.ERROR)

_GPIO_STATE_INPUT, _GPIO_STATE_OUTPUT = range(2)


class ConnectionManager(object):
    """Handle communication from client application to firmware and sensor.
         - Load given board configuration
         - Open connection to selected bus2 (self.kx_adapter)
         - Connect to board firmware and run board_init

        Args:
            board_config_json(string): File name of board configoration json file
        """

    def __init__(self, board_config_json=None, odr=None, skip_init=False):
        LOGGER.debug('>init')

        if board_config_json is None:
            board_config_json = evkit_config.board

        LOGGER.info('Opening board configuration %s' % format(board_config_json))

        bus2_name = evkit_config.bus2

        assert bus2_name in [BUS2_USB, BUS2_BLE, BLE_PYGATT, BUS2_SOCKET, BUS2_USB_SERIAL, BUS2_USB_AARDVARK]

        self.found_sensors = {}
        self._pin_mode_cache = {}  # store gpio pin mode _GPIO_STATE_INPUT / _GPIO_STATE_OUTPUT
        self.bus2_configuration = None
        self.board_config = None

        self.board_config_json = board_config_json

        # list of location from where to look configuration file
        filepath_list = [
            os.path.join('cfg', board_config_json), 
            os.path.join(os.path.dirname(__file__), '..', 'cfg', board_config_json)]

        for filepath in filepath_list:
            LOGGER.debug('Search configuration %s' % format(filepath))
            board_file_name = os.path.abspath(filepath)
            if os.path.isfile(board_file_name):
                LOGGER.info('Loading %s' % format(board_file_name))
                with open(board_file_name, 'r') as infile:
                    self.board_config = json.load(infile)
                break
        
        assert self.board_config is not None, 'No configuration file found \n%s.' % '\n'.join(filepath_list)
        

        # verify board config version
        if self.board_config['structure_version'] not in SUPPORTED_BOARD_CONFIGURATION_VERSIONS:
            raise EvaluationKitException('Board config version is %s. Supported versions are %s' % (
                self.board_config['structure_version'], SUPPORTED_BOARD_CONFIGURATION_VERSIONS))

        # verify that asked connection was found from board configuration
        connections_list = self.board_config['configuration']['bus2']['connections']
        number_of_usb_bus2 = sum(
            [BUS2_USB in bus2_connection['connection'] for bus2_connection in connections_list])

        if number_of_usb_bus2 > 1 and bus2_name == BUS2_USB:
            raise EvaluationKitException(
                'Multiple USB bus2 connections found from board configuration %s. Please select which one to use.' %
                board_config_json)

        # find asked bus2 configuration
        for bus2_connection in connections_list:
            if bus2_connection['connection'] == bus2_name:
                self.bus2_configuration = bus2_connection
                break

            # check that BUS2_USB is supported in board config
            elif bus2_name == BUS2_USB and bus2_connection['connection'].startswith(BUS2_USB):
                LOGGER.info('%s bus2 selected' % format(bus2_connection['connection']))
                self.bus2_configuration = bus2_connection
                break

        if self.bus2_configuration is None:
            raise EvaluationKitException('Selected bus2 "{}" not found from board configuration {}'.format(bus2_name, board_config_json))

        # open the connection
        if self.bus2_configuration['connection'] in [BUS2_USB_SERIAL]:
            bus2connection = KxComPort(bus2_configuration=self.bus2_configuration)
            serial_port = evkit_config.serial_port

            if serial_port == 'auto':
                # auto discover the com port
                found_ports = bus2connection.get_com_port()
            else:
                # com port defined in rokix_settings.cfg
                found_ports = [serial_port]

            for com_port in found_ports:
                LOGGER.debug("Finding board from %s" % com_port)
                bus2connection.initialize(com_port)
                self.kx_adapter = KxAdapterEvk(bus2=bus2connection)

                if self.kx_adapter.board_id != self.board_config[CFG_CONFIGURATION]['board_id']:
                    bus2connection.close()  # this was not right port. close it.
                    LOGGER.debug('Board id %s received. Expected id is %s.' % (
                        self.kx_adapter.board_id, self.board_config[CFG_CONFIGURATION]['board_id']))
                else:
                    break

            if self.kx_adapter.board_id != self.board_config[CFG_CONFIGURATION]['board_id']:
                raise EvaluationKitException('Expected evaluation board not found.')

        elif self.bus2_configuration['connection'] == BUS2_USB_AARDVARK:
            self.kx_adapter = KxAdapterAardvark(bus1config=self.board_config['configuration']['bus1']['targets'][0])

        elif self.bus2_configuration['connection'] == BUS2_BLE:
            bus2connection = KxWinBLE(bus2_configuration=self.bus2_configuration)
            # use mac address with BLE
            bus2connection.initialize(mac_address=evkit_config.ble_mac)

            self.kx_adapter = KxAdapterEvk(bus2=bus2connection)
        
        elif self.bus2_configuration['connection'] == BLE_PYGATT:
            bus2connection = KxLinuxBLE(bus2_configuration=self.bus2_configuration)

            bus2connection.initialize(mac_address=evkit_config.ble_mac)

            self.kx_adapter = KxAdapterEvk(bus2=bus2connection)

        else:
            raise EvaluationKitException('No rule found to configure bus 2.')

        # verify that board FW is supported
        if self.kx_adapter.fw_protocol_version not in SUPPORTED_FIRMWARE_PROTOCOL_VERSIONS:
            raise EvaluationKitException("Board reported protocol version %s. Supported versions are %s" % (
                self.kx_adapter.fw_protocol_version, SUPPORTED_FIRMWARE_PROTOCOL_VERSIONS))

        # verify that board fw is compatible with board config
        if self.kx_adapter.fw_protocol_version not in self.board_config['protocol_version']:
            raise EvaluationKitException("Board reported protocol version %s. Board config expects %s" % (
                self.kx_adapter.fw_protocol_version, self.board_config['protocol_version']))

        # Apply board init if found from board configuration
        if not skip_init and 'board_init' in self.board_config[CFG_CONFIGURATION]:
            if self.board_config['configuration']['board_init']['reg_write']:
                LOGGER.debug('board_init found from board configuration. Initializing the board')

                for message_content in self.board_config['configuration']['board_init']['reg_write']:
                    sensor_name, sensor_register, register_value = message_content
                    for target_blob in self.board_config['configuration']['bus1']['targets']:
                        if sensor_name in target_blob['parts']:
                            sensor_resource = target_blob['parts'][sensor_name]

                            LOGGER.debug('%d %d %d %d' % (
                                target_blob[CFG_TARGET], sensor_resource[CFG_SAD],
                                sensor_register, register_value))

                            self.kx_adapter.adapter_write_sensor_register_i2c(
                                target_blob[CFG_TARGET], sensor_resource[CFG_SAD],
                                sensor_register, register_value)

        else:
            LOGGER.debug('board_init not found from board configuration')

        # configure power mode
        if odr:
            self.set_cpu_power_mode(odr)
        else:
            # if odr is not given then assume it is high and disable power save.
            self.set_cpu_power_mode(1000) 

        LOGGER.debug('<init')

    # Following two methods are needed when creating this class using "with"-compound statement
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

    def read_sensor_register(self, sensor_driver, register, length=1):
        """Read sensor register value(s)

        Args:
            sensor_driver(SensorDriver): sensor driver instance
            register(int): Register value where reading starts
            length(int): how many bytes to read. Defaults to 1

        Returns:
            array.array: sensor register values as binary array

        Note:
            Sensor must be first added with add_sensor() before this operation can be done.

        """

        _, sensor_resource = self.found_sensors[sensor_driver.name]
        bus1_name = sensor_driver.selected_connectivity

        if bus1_name == BUS1_I2C:
            target = sensor_resource[CFG_TARGET]
            sad = sensor_resource[CFG_SAD]

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_read_sensor_register_i2c(target, sad, register, length)

        elif bus1_name == BUS1_SPI:
            target = sensor_resource[CFG_TARGET]
            cs = sensor_resource[CFG_CS]

            if sensor_resource[CFG_SPI_PROTOCOL] == 1:
                # With Kionix components, MSB must be set 1 to indicate reading
                register = register | 1 << 7

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_read_sensor_register_spi(target, cs, register, length)

        raise EvaluationKitException('Unable read sensor register.')

    def write_sensor_register(self, sensor_driver, register, values):
        """Write sensor register value(s)

        Args:
            sensor_driver(SensorDriver): sensor driver instance
            register(int): Register value where writing starts
            values ?

        Note:
            Sensor must be first added with add_sensor() before this operation can be done.
        """
        _, sensor_resource = self.found_sensors[sensor_driver.name]
        bus1_name = sensor_driver.selected_connectivity

        if bus1_name == BUS1_I2C:
            target = sensor_resource[CFG_TARGET]
            sad = sensor_resource[CFG_SAD]

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_write_sensor_register_i2c(target, sad, register, values)

        elif bus1_name == BUS1_SPI:
            target = sensor_resource[CFG_TARGET]
            cs = sensor_resource[CFG_CS]

            if sensor_resource[CFG_SPI_PROTOCOL] == 1:
                # When using SPI, Kionix sensors require that the address' MSB is
                # cleared to indicate that this is a write.
                register &= ~(1 << 7)

            with DelayedKeyboardInterrupt():
                return self.kx_adapter.adapter_write_sensor_register_spi(target, cs, register, values)

        else:
            raise EvaluationKitException('Unable write data to sensor register.')

    def gpio_config_for_adc(self, sensor_driver):
        """Configure GPIO lines to enable analog sensor.

        Some analog sensors are GPIO controlled. Set GPIO lines to needed states to get analog sensor to
        wanted operational mode.

        Args:
            sensor_driver (SensorDriver): sensor driver instance

        """
        if 'gpio_conf' in sensor_driver.resource:
            for index, pin in enumerate(sensor_driver.resource['gpio_conf'][0]):
                # [0] is for pin number and [1] is for pin value
                value = sensor_driver.resource['gpio_conf'][1][index]
                assert value in [0, 1]

                # Update _pin_mode_cache.
                current_state = self._pin_mode_cache.get(pin, None)
                if current_state != _GPIO_STATE_OUTPUT:
                    LOGGER.debug("Changing pin %d mode from %s to %s" % (pin, current_state, _GPIO_STATE_OUTPUT))
                    self._pin_mode_cache[pin] = _GPIO_STATE_OUTPUT

                self.kx_adapter.configure_pin_as_output(pin, value)
                LOGGER.debug('gpio_conf %d=%d.' % (pin, value))
        else:
            LOGGER.debug('No gpio_conf done.')

    def read_adc(self, sensor_driver):
        result = []

        self.gpio_config_for_adc(sensor_driver)

        for sensor_channel in sensor_driver.int_pins:
            board_channel = self.get_physical_pin_for_sensor(sensor_driver, sensor_channel)
            result.append(self.kx_adapter.adapter_read_adc(
                target=sensor_driver.resource[CFG_TARGET],
                channel=board_channel,
                resolution=sensor_driver.resource[CFG_ADC_RESOLUTION],
                oversample=sensor_driver.resource['adc_msg_oversampling_enum'],
                gain=sensor_driver.resource['adc_msg_gain_enum'],
                acq_time_us=sensor_driver.resource['adc_msg_conversion_time_us']
            ))
        return result

    def read_gpio_pin(self, gpio_pin, pull=NOPULL):
        """Read GPIO line value based on HW index

        Args:
            gpio_pin(int): pin index (physical index)
            pull(int): NOPULL, PULLDOWN, PULLUP = range(3). Defalults to NOPULL
        """
        current_state = self._pin_mode_cache.get(gpio_pin, None)
        if current_state != (_GPIO_STATE_INPUT, pull):

            LOGGER.debug("Changing pin %d mode from %s to %s" % (gpio_pin, current_state, _GPIO_STATE_INPUT))
            LOGGER.debug("Changing pull to %s" % pull)

            self.kx_adapter.configure_pin_as_input(gpio_pin=gpio_pin, drivemode=pull)
            self._pin_mode_cache[gpio_pin] = (_GPIO_STATE_INPUT, pull)

        with DelayedKeyboardInterrupt():
            return self.kx_adapter.adapter_read_gpio(gpio_pin)

    def write_gpio_pin(self, gpio_pin, value):
        """Set GPIO line value based don HW index

        Args:
            gpio_pin(int): pin index (physical index)
            value(int): 0 or 1

        """
        assert isinstance(gpio_pin, int)
        assert value in [0, 1]

        # Update _pin_mode_cache.
        current_state = self._pin_mode_cache.get(gpio_pin, None)
        if current_state != _GPIO_STATE_OUTPUT:
            LOGGER.debug("Changing pin %d mode from %s to %s" % (gpio_pin, current_state, _GPIO_STATE_OUTPUT))
            self._pin_mode_cache[gpio_pin] = _GPIO_STATE_OUTPUT

        with DelayedKeyboardInterrupt():
            return self.kx_adapter.adapter_write_gpio(gpio_pin, value)

    def read_sensor_gpio(self, sensor_driver, pin=1):
        """Read state sensor's interrupt line

        Physical state of the interrupt line is read (e.g. it is not logical state for example in case active low).
        Physical GPIO line in MCU is retrieved from board_config.json

        Args:
            sensor_driver(SensorDriver): sensor driver instance
            pin(int): Sensor's interrupt pin number. Defaults to 1.

        Returns:
            int: 0 or 1
        """
        assert pin in sensor_driver.int_pins, 'Interrupt pin %d does not exists in sensor.' % pin

        gpio_pin = self.get_physical_pin_for_sensor(sensor_driver, pin)
        # Map config text to enum
        pull = PULL_DICT[sensor_driver.resource[CFG_PULLUP]]
        return self.read_gpio_pin(gpio_pin, pull=pull)

    def disconnect(self):
        """Close bus2 connection"""
        self.kx_adapter.adapter_disconnect()

    def get_physical_pin_for_sensor(self, sensor, pin=1):
        """Retrieve physical GPIO line for sensor interrupt pin in current board.

        Args:
            sensor_driver(SensorDriver): sensor driver instance
            pin(int): Sensor's interrupt pin number. Defaults to 1.
        """

        # sensor.resource {u'gpio1': 0, u'SAD': 31, u'target': 4, u'name': u'KX122'}
        if isinstance(pin, int):
            return sensor.resource[INT_GPIO_DICT[pin]]
        elif isinstance(pin, list):
            return [sensor.resource.get(ADC_GPIO_DICT[ind]) for ind in ADC_GPIO_DICT if sensor.resource.get(ADC_GPIO_DICT[ind]) is not None]

        raise EvaluationKitException('Invalid data type for "pin".')

    def _configure_target(self, target_blob):
        """Configure bus1 properties"""

        LOGGER.debug('> %d' % target_blob[CFG_TARGET])

        if target_blob[CFG_NAME] == BUS1_I2C:
            if target_blob[CFG_FREQ] != -1:
                LOGGER.debug('Configure i2c bus speed to %d kHz' % target_blob[CFG_FREQ])
                self.kx_adapter.configure_i2c(target_blob[CFG_TARGET], target_blob[CFG_FREQ])

        elif target_blob[CFG_NAME] == BUS1_SPI:
            if target_blob[CFG_FREQ] != -1:
                LOGGER.debug('Configure spi bus speed to %d kHz' % target_blob[CFG_FREQ])
                LOGGER.debug('Configure SPI mode to %d' % target_blob[CFG_SPI_MODE])
                self.kx_adapter.configure_spi(
                    target_blob[CFG_TARGET], target_blob[CFG_FREQ], target_blob[CFG_SPI_MODE])

        if target_blob[CFG_NAME] == BUS1_ADC:
            # Configuration done when reading ADC nothing to do here
            LOGGER.debug('Configure ADC mode - no actions')

    def add_sensor(self, sensor_driver, bus1_name=None, sensor_resource_definition=None):
        """ Connect to sensor on board and probe that sensor is found.

        Args:
            sensor_driver(SensorDriver): sensor driver instance
            bus1_name(string): BUS1_I2C, BUS1_SPI. Name of the bus where sensor is connected. Defaults to None
            sensor_resource_definition(?): Sensor's resource blob from board_config.json. Defaults to None

        Options:

        1) bus1_name is not given.
            Adds sensor by giving just sensor_driver instance. In this case sensor is configred based on board configuration.
            sensor name is searched from board config and found sensor_resource_definition is used from there.

        2) bus1_name is given.
        2.1) sensor_resource_definition is given
        Adds sensor based on sensor_resource_definition and probe that sensor is found

        2.2) sensor_resource_definition is not given
        Automatic probe for sensor. FIXME how to do? in case of protocol 2, need to scan through all buses in hw config.

        """
        LOGGER.debug('>')
        if sensor_driver.name in self.found_sensors:
            LOGGER.debug('%s already added earlier. Do nothing' % sensor_driver.name)
            return

        # if bus1 is not defined then look for board configuration json
        if bus1_name is None:
            assert sensor_resource_definition is None

            # find this sensor from board configuration
            target_blob = None
            for target_blob in self.board_config['configuration']['bus1']['targets']:

                if sensor_driver.name in target_blob['parts']:

                    # take default configuration blob
                    sensor_defaults = self.board_config['configuration']['bus1']['sensor_defaults'].copy()

                    # update target spesific configurations
                    sensor_defaults['target'] = target_blob['target']

                    # update sensor spesific configurations
                    sensor_defaults.update(target_blob['parts'][sensor_driver.name])
                    self._configure_target(target_blob)

                    # update sensor_driver properties
                    sensor_driver.resource = sensor_defaults
                    sensor_driver.assign_connection_manager(self)
                    sensor_driver.selected_connectivity = target_blob[CFG_NAME]

                    # update found sensors dict
                    self.found_sensors[sensor_driver.name] = (target_blob, sensor_driver.resource)

                    LOGGER.debug(sensor_driver.resource)

                    break

            # verify that configuration is found
            if sensor_driver.resource is None:
                raise EvaluationKitException(
                    ("Sensor '%s' not found from board configuration file '%s'. Possible reason is" +
                     " that wrong board configuration file selected in rokix_settings.cfg") % 
                     (sensor_driver.name, self.board_config_json))

            _probe_status = sensor_driver.probe()
            if _probe_status != 1:
                raise EvaluationKitException("Sensor probe failed with return value %s" % _probe_status)

            if target_blob[CFG_NAME] == BUS1_I2C:
                LOGGER.info('Sensor %s found. I2C address 0x%x' % (sensor_driver.name, sensor_driver.resource[CFG_SAD]))
            elif target_blob[CFG_NAME] == BUS1_SPI:
                LOGGER.info('Sensor %s found. SPI CS pin 0x%x' % (sensor_driver.name, sensor_driver.resource[CFG_CS]))
            elif target_blob[CFG_NAME] == BUS1_ADC:
                LOGGER.info('Sensor %s found. ADC pins used.' % (sensor_driver.name))
            else:
                assert 0, '%s not implemented' % target_blob[CFG_NAME]

            LOGGER.debug('<')
            return True

        else:
            # bus 1 name is given
            assert bus1_name in [BUS1_I2C, BUS1_SPI, BUS1_ADC]
            assert bus1_name in sensor_driver.supported_connectivity

            if sensor_resource_definition is not None:
                # sensor_resource_definition is given

                # update sensor_driver properties
                sensor_driver.resource = sensor_resource_definition
                sensor_driver.assign_connection_manager(self)
                sensor_driver.selected_connectivity = bus1_name

                # update found sensors dict
                self.found_sensors[sensor_driver.name] = (None, sensor_resource_definition)

                LOGGER.debug(sensor_driver.resource)
                assert sensor_driver.probe() is True

                LOGGER.debug('<')
                return True

            else:
                # auto discover
                if bus1_name == BUS1_I2C:
                    LOGGER.info('Autodiscovery sensor from I2C')
                    found = False
                    sad = '?'  # in case sensor_driver.i2c_sad_list is empty
                    for sad in sensor_driver.i2c_sad_list:
                        self.found_sensors[sensor_driver.name] = (target_blob, {CFG_SAD: sad})
                        LOGGER.info('Probing %s from address 0x%x' % (sensor_driver.name, sad))
                        try:
                            found = sensor_driver.probe()
                            break

                        except ProtocolBus1Exception:
                            LOGGER.debug('No response got from slave address 0x%02x' % sad)

                    if found:
                        LOGGER.info('Sensor %s found from slave address 0x%02x' % (sensor_driver.name, sad))
                        return True
                    else:
                        # remove sensor from self.found_sensors
                        self.found_sensors.pop(sensor_driver.name)
                        LOGGER.info('Sensor %s not found.' % sensor_driver.name)
                        return False

                elif bus1_name == BUS1_SPI:
                    LOGGER.info('Autodiscovery sensor from SPI')
                    found = False

                    for cs in [0]:
                        self.found_sensors[sensor_driver.name] = (target_blob, {CFG_CS: cs})
                        LOGGER.info('Probing %s with CS 0x%x' % (sensor_driver.name, cs))
                        try:
                            found = sensor_driver.probe()
                            break

                        except ProtocolBus1Exception:
                            LOGGER.debug('No response got from slave address 0x%02x' % sad)

                    if found:
                        LOGGER.info('Sensor %s found from slave address 0x%02x' % (sensor_driver.name, sad))
                        return True

                    assert 0, 'not implemented'
                else:
                    assert 0, 'not implemented'

    def get_stream_config_location(self):
        """Get location of the stream configuration files."""
        return self.board_config['configuration']['stream_config']['directory']

    def set_cpu_power_mode(self, odr):
        """Allow CPU sleep if ODR is low"""
        LOGGER.debug('Configure CPU mode')
        # odr setting for data logging
        if odr >= 100:
            self.kx_adapter.configure_fw(sleep_enabled=False)
        else:
            self.kx_adapter.configure_fw(sleep_enabled=True)
