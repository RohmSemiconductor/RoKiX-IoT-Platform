# 
# Copyright 2018 Kionix Inc.
#
import time
from kx_lib.kx_exception import EvaluationKitException, ProtocolTimeoutException, FunctionalityNotInDevice
from kx_lib.kx_configuration_enum import CFG_POLARITY, EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW, SENSOR_TYPE_DIGITAL_3D, CH_ACC, CFG_AXIS_MAP, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT, TIMER_POLL, REG_POLL
from kx_lib.kx_util import evkit_config, get_timer
import kx_lib.kx_logger as kx_logger
LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.INFO)
# LOGGER.setLevel(kx_logger.DEBUG)
# LOGGER.setLevel(kx_logger.ERROR)
"""

self.resource example
{
    "target":4,
    "name": "KX122",
    "SAD": 31,
    "gpio1": 0
}
"""


class AxisMapper(object):
    def __init__(self, channel_header="x!y!z", axis_map=None):
        """"Initialize AxisMapper

        Args:
            channel_header(string) : channel header definition. Example "ch!ax!ay!az"

            axis_map (list) : descrption how axis order and polarity is converted. Default None e.g. no mapping.
                Examples:
                 [0,1,2] maps x,y,z
                 [2,1,0] maps z,y,x
                 [3,4,5] maps -x,-y,-z
                 [0,1,5] maps x,y,-z
        """
        # header and map is not defined if no 3d data
        if not axis_map:  # empty list or None etc...
            self.axis_map = None
            return
        # find dimension indexes holding xyz data
        self.xyz_ind = [ind for ind, label in enumerate(channel_header.split('!')) if label[-1] in ['x', 'y', 'z']]
        if not self.xyz_ind:
            self.axis_map = None
        else:
            self.axis_map = axis_map

    def map_xyz_axis(self, measurement):
        """ Conver measurement to match wanted sensor axis directions.

        This methods goes through channel_header and check if dimension ends with [xyz] then
        maps these dimensions based on axis_map.

        Args:
            measurement (list) : full data from channel

        """
        # is this 3d sensor data
        if self.axis_map is None:
            return measurement

        # covert tuple to list
        measurement = list(measurement)

        # get xyz data values from full data
        xyz_data = [measurement[ind] for ind in self.xyz_ind]

        # make list of xyz data + negated xyz data
        xyz_data_extended = xyz_data + [-value for value in xyz_data]

        # make mapping for extended xyz data (e.g. update location and sign)
        xyz_mapped = [xyz_data_extended[ind] for ind in self.axis_map]

        # apply mapped data back to raw data
        for xyz_data_ind, measurement_data_ind in enumerate(self.xyz_ind):
            measurement[measurement_data_ind] = xyz_mapped[xyz_data_ind]

        return measurement


class SensorDriver(object):
    supported_parts = ['undefined']  # define names of sensor parts which are supported by the driver

    def __init__(self):

        # assert self.read_data.__func__ == SensorDriver.read_data.__func__,\
        #'read_data() must not be overriden. Implement sensor spesific data reading to __read_data().'

        # These must be defined in sensor driver
        self.supported_connectivity = None  # define in driver [BUS1_I2C, BUS1_SPI]
        self.i2c_sad_list = []
        self._default_channel = None
        self.name = self.supported_parts[0]  # driver class needs to define self.name only if there are more that one supported_pats

        self.sensor_type = SENSOR_TYPE_DIGITAL_3D
        self.int_pins = [1, 2]
        assert self.supported_parts is not None, 'Supported_parts attribute must be defined in sensor driver %s.' % self

        # These will be set automatically
        self.connected = False
        self.connection_manager = None
        self.resource = {}
        self._registers = {}
        self._dump_range = [0, 2]
        self.WHOAMI = None
        self.poll_delay_s = evkit_config.drdy_timer_interval
        self.poll_delay_s_other = evkit_config.other_timer_interval
        self.axis_mapper = None
        self.selected_connectivity = None

        # to be fixed later
        self.channel_header = 'ax!ay!az'  # define in driver
        self._timing = get_timer()

        self._drdy_LUT = {
            TIMER_POLL: self._poll_delay,
            REG_POLL: self._poll_drdy_register,
            ADAPTER_GPIO1_INT: self._poll_gpio_line1,
            ADAPTER_GPIO2_INT: self._poll_gpio_line2,
        }

        # Drdy function mode
        drdy_function_mode = evkit_config.drdy_function_mode
        LOGGER.debug('Using "{}" for data ready.'.format(drdy_function_mode))
        self.drdy_function = self._drdy_LUT[drdy_function_mode]

        # Other function mode
        other_function_mode = evkit_config.other_function_mode
        self._drdy_LUT[TIMER_POLL] = self._poll_delay_other  # Other function has its own poll intervall
        LOGGER.debug('Using "{}" for asic events.'.format(other_function_mode))
        self.asic_function = self._drdy_LUT[other_function_mode]

    def _read_data(self, channel=None):
        "Override this method on sensor spesific driver"
        raise NotImplementedError()

    def read_data(self, channel=None):
        "Read sensor data and rotate 3d sensor coordinates"

        if channel is None:
            channel = self._default_channel

        data = self._read_data(channel)

        if self.axis_mapper is not None:
            data = self.axis_mapper.map_xyz_axis(data)

        return list(data)

    def probe(self):
        return False

    def drdy_function(self):  # pylint: disable=method-hidden
        "Wait until sensor signals data ready"
        # This will be overwritten in __init__()
        pass

    def assign_connection_manager(self, connection_manager):

        self.connection_manager = connection_manager

        # self.resource is set when this method is called
        self.axis_mapper = AxisMapper(
            channel_header=self.channel_header,
            axis_map=self.resource[CFG_AXIS_MAP])

    def write_register(self, register, data):
        assert self.connected
        LOGGER.debug('0x%02x=%s' % (register, data))
        self.connection_manager.write_sensor_register(self, register, data)

    def set_bit(self, register, bit):
        """Set the specified bits in a register."""
        value = self.read_register(register)[0]
        value = value | bit
        assert value == value & 0xff  # overflow test
        self.write_register(register, value)

    def reset_bit(self, register, bit):
        """Clear the specified bits in a register."""
        value = self.read_register(register)[0]
        value = value & ~bit
        self.write_register(register, value)

    def read_register(self, register, length=1):
        assert self.connected
        return self.connection_manager.read_sensor_register(self, register, length)

    def set_range(self, range, channel):
        raise NotImplementedError()

    def set_BW(self, range, channel):
        raise NotImplementedError()

    def set_power_on(self, channel=CH_ACC):
        raise NotImplementedError()

    def set_power_off(self, channel=CH_ACC):
        raise NotImplementedError()

    def set_default_on(self):
        raise NotImplementedError()

    def release_interrupts(self, intpin=1):
        raise NotImplementedError()

    def _poll_delay(self, timeout=0):
        del timeout  # not used
        time.sleep(self.poll_delay_s)
        return 0

    def _poll_delay_other(self, timeout=0):
        del timeout  # not used
        time.sleep(self.poll_delay_s_other)
        return 0

    def read_drdy(self):
        raise NotImplementedError()

    def read_asic_event(self):
        "Override this method on sensor spesific datalogger"
        raise FunctionalityNotInDevice()

    def _poll_drdy_register(self, timeout=5.0):
        """Wait for data ready register value change.

            Returns
                0  if successfully seend gpio line change
                -1 if no gpio line change not seen
        """
        count = 0
        self._timing.reset()
        while not self.read_drdy():
            count += 1
            if timeout and self._timing.time_elapsed() > timeout:
                LOGGER.error('DRDY not detected. Please check sensor configuration.')
                return -1

        if count == 0:
            LOGGER.warning('Possible data overflow. ODR may be too high for host adapter or GPIO lines may not be connected.')
            return -1
        return 0

    def _poll_gpio_line1(self, timeout=5.0):
        assert self.resource[CFG_POLARITY] in [EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW]

        return self.bus_poll_gpio(
            pin=1,
            polarity=self.resource[CFG_POLARITY] == EVKIT_GPIO_PIN_SENSE_HIGH,
            timeout=timeout)

    def _poll_gpio_line2(self, timeout=5.0):
        assert self.resource[CFG_POLARITY] in [EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW]
        return self.bus_poll_gpio(
            2,
            self.resource[CFG_POLARITY] == EVKIT_GPIO_PIN_SENSE_HIGH,
            timeout=timeout)

    def bus_poll_gpio(self, pin, polarity, timeout):
        """Wait for GPIO line change.

        Args:
            pin (int): Logical sensor pin to poll.
            polarity (int): 0 is active low, 1 is active high.
            timeout (float): Timeout in seconds.

        Returns:
            bool: True if the active state was detected. Otherwise False.
        """
        assert polarity in [0, 1]
        self._timing.reset()

        count = 0
        while self.connection_manager.read_sensor_gpio(self, pin) != polarity:
            count += 1
            if timeout and self._timing.time_elapsed() > timeout:
                raise ProtocolTimeoutException('No interrupts received. Please check interrupt line connections and sensor configuration.')

        #      the polled state before we start polling it.
        if count == 0:
            LOGGER.warning('Possible data overflow. ODR may be too high for host adapter or GPIO lines may not be connected.')
            return False
        return True

    def i2c_address(self):
        _, sensor_resource = self.connection_manager.found_sensors[self.name]
        i2c_slave_address = sensor_resource['SAD']
        return i2c_slave_address

    def set_bit_pattern(self, register, bit_pattern, mask):
        # Mask out "mask" bits and apply "bit_pattern" bits.
        # Note: bit_pattern may contain also bits outside the mask
        if bit_pattern & ~mask != 0:
            LOGGER.warning('Bit pattern defined outside from the mask.' +
                           'Bit pattern 0b{0:08b}, mask 0b{1:08b}'.format(bit_pattern, mask))

        value = self.read_register(register)[0] & ~mask
        value |= bit_pattern
        assert value == value & 0xff  # overflow test
        self.write_register(register, value)

    def register_dump(self):
        """
        Printout values from all registers in _dump_range.
        """
        self.register_dump_range()

    def register_dump_range(self, startreg=0, endreg=0):
        """
        Printout values from registers in _dump_range (_dump_range is set in driver). Incomplete
        range can be given with parameters.
        :param startreg: first register address to printout
        :param endreg:    last register address to printout
        """
        if (endreg == 0):
            startreg, endreg = self._dump_range
        reg_list = range(startreg, (endreg + 1))
        self.register_dump_listed(reg_list)
        return

    def register_dump_listed(self, reglist):
        """
        Printout values from registers in reglist.
        :param reglist: list of registers
        """
        k = list(self._registers.keys())
        v = list(self._registers.values())
        for reg in reglist:
            try:
                i = v.index(reg)
            except ValueError:
                continue
            name = k[i]
            name = name.ljust(20)
            d = self.read_register(reg)[0]
            #print ('0x{:02x}\t{:10s}\t0x{:02x}\t0b{:08b}\t{:03d}'.format(reg, name, d, d, d))
            print('{:03d}\t0x{:02x}\t{:10s}\t0x{:02x}\t0b{:08b}\t{:03d}'.format(reg, reg, name, d, d, d))


class AnalogSensorDriver(SensorDriver):
    def probe(self):
        self.connected = True
        return 1

    def set_default_on(self):
        return

    def read_drdy(self):
        return

    def release_interrupts(self):
        return

    def read_asic_event(self):
        raise FunctionalityNotInDevice

    def i2c_address(self):
        return 0

    def por(self):
        return

    def _read_data(self, channel=None):
        "Override this method on sensor spesific driver"
        raise NotImplementedError()
