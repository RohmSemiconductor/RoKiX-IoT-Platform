# 
# Copyright 2018 Kionix Inc.
#
import time
from kx_lib.kx_exception import EvaluationKitException
from kx_lib.kx_configuration_enum import CFG_POLARITY, EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW, SENSOR_TYPE_DIGITAL_3D, CH_ACC, CFG_AXIS_MAP
from kx_lib.kx_util import evkit_config
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
        if  not axis_map: # empty list or None etc...
            self.axis_map = None
            return

        # find dimension indexes holding xyz data
        self.xyz_ind = [ind for ind, label in enumerate(channel_header.split('!')) if label[-1] in ['x', 'y', 'z']]
        self.axis_map = axis_map

    def map_xyz_axis(self, measurement):
        """ Conver measurement to match wanted sensor axis directions.

        This methods goes through channel_header and check if dimension ends with [xyz] then
        maps these dimensions based on axis_map.

        Args:
            measurement (list) : full data from channel

        """
        # FIXME 1 move this functionality to data logger and improve the logic
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
    def __init__(self):

        # TODO 2 find a way to check this which works on both py2 and py3
        #assert self.read_data.__func__ == SensorDriver.read_data.__func__,\
        #'read_data() must not be overriden. Implement sensor spesific data reading to __read_data().'

        self.connected = False
        self.connection_manager = None
        self.resource = None
        self.supported_connectivity = None
        self.name = 'undefined'
        self.channel_header = 'ax!ay!az'
        self._registers = {}
        self._dump_range = [0, 2]
        self.WHOAMI = None
        self.poll_delay_s = evkit_config.getint('generic', 'drdy_poll_interval') / 1000.
        self.sensor_type = SENSOR_TYPE_DIGITAL_3D
        self.axis_mapper = None
        self.selected_connectivity = None

        self._drdy_LUT = {
            'INTERVAL_READ':self._poll_delay,
            'DRDY_REG_POLL':self._poll_drdy_register,
            'ADAPTER_GPIO1_INT':self._poll_gpio_line1,
            'ADAPTER_GPIO2_INT':self._poll_gpio_line2
            }
        try:
            drdy_operation = evkit_config.get('generic', 'drdy_operation')
            LOGGER.debug('Using "{}" for data ready.'.format(drdy_operation))
            self.drdy_function = self._drdy_LUT[evkit_config.get('generic', 'drdy_operation')]
        except KeyError:
            raise EvaluationKitException('Missing or invalid "drdy_operation" definition in settings.cfg')

    def _read_data(self, channel=CH_ACC):
        "Override this method on sensor spesific driver"
        raise NotImplementedError()

    def read_data(self, channel=CH_ACC):
        "Read sensor data and rotate 3d sensor coordinates"

        data = self._read_data(channel)

        if self.axis_mapper is not None:
            data = self.axis_mapper.map_xyz_axis(data)

        return data

    def probe(self):
        return False

    def drdy_function(self):  # pylint: disable=method-hidden
        "Wait until sensor signals data ready"
        #This will be overwritten in __init__()
        pass

    def assign_connection_manager(self, connection_manager):

        self.connection_manager = connection_manager

        # self.resource is set when this method is called
        # FIXME 2 channel_header should come from stream configuration. Add also channel_header to each driver.
        self.axis_mapper = AxisMapper(
            channel_header=self.channel_header,
            axis_map=self.resource[CFG_AXIS_MAP])
        
    def write_register(self, register, data):
        assert self.connected
        self.connection_manager.write_sensor_register(self, register, data)

    def set_bit(self, register, bit):
        """Set the specified bits in a register."""
        value = self.read_register(register)[0]
        value = value | bit
        assert value == value & 0xff # overflow test
        self.write_register(register, value)

    def reset_bit(self, register, bit):
        """Clear the specified bits in a register."""
        value = self.read_register(register)[0]
        value = value & ~bit
        self.write_register(register, value)

    def read_register(self, register, length=1):
        assert self.connected
        return self.connection_manager.read_sensor_register(self, register, length)

    def set_power_on(self, channel=CH_ACC):
        raise NotImplementedError()

    def set_power_off(self, channel=CH_ACC):
        raise NotImplementedError()

    def set_default_on(self):
        raise NotImplementedError()

    def _poll_delay(self):
        time.sleep(self.poll_delay_s)
        return 0

    def read_drdy(self):
        raise NotImplementedError()

    def _poll_drdy_register(self, timeout=5000):
        """Wait for data ready register value change.

            Returns
                0  if successfully seend gpio line change
                -1 if no gpio line change not seen
        """
        count = 0
        while not self.read_drdy():
            count += 1
            if timeout and count > timeout:
                LOGGER.error('DRDY not detected. Please check sensor configuration.')
                return -1

        if count == 0:
            LOGGER.warning('Possible data overflow. ODR may be too high for host adapter or GPIO lines may not be connected.')
            return -1
        return 0

    def _poll_gpio_line1(self):
        assert self.resource[CFG_POLARITY] in [EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW]

        if self.resource[CFG_POLARITY] == EVKIT_GPIO_PIN_SENSE_HIGH:
            polarity = 1
        else:
            polarity = 0

        return self.bus_poll_gpio(1, polarity=polarity)

    def _poll_gpio_line2(self):
        assert self.resource[CFG_POLARITY] in [EVKIT_GPIO_PIN_SENSE_HIGH, EVKIT_GPIO_PIN_SENSE_LOW]
        return self.bus_poll_gpio(
            2, self.resource[CFG_POLARITY] == EVKIT_GPIO_PIN_SENSE_HIGH)

    def bus_poll_gpio(self, pin, polarity, timeout=5.0):
        """Wait for GPIO line change.

        Args:
            pin (int): Logical sensor pin to poll.
            polarity (int): 0 is active low, 1 is active high.
            timeout (float): Timeout in seconds.

        Returns:
            bool: True if the active state was detected. Otherwise False.
        """
        assert polarity in [0, 1]
        t_start = time.time()
        count = 0
        while self.connection_manager.read_sensor_gpio(self, pin) != polarity:
            count += 1
            if timeout and time.time() > t_start + timeout:
                assert 0, 'No interrupts received. Please check interrupt line connections and sensor configuration.'
        # XXX: This will cause a false positive if the pin happens to be in
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
        assert value == value & 0xff # overflow test
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
        k = self._registers.keys()
        v = self._registers.values()
        for reg in reglist:
            try:
                i = v.index(reg) # FIXME 2 this fails on python 3
            except ValueError:
                continue
            name = k[i]
            name = name.ljust(20)
            d = self.read_register(reg)[0]
            # TODO 3 return instead of print
            print('0x%02x %s\t0x%02x\t%s' % (reg, name, d, '0b{0:08b}'.format(d)))

class AnalogSensorDriver(SensorDriver):
    def probe(self):
        self.connected = True
        return 1

    def set_default_on(self):
        return

    def read_drdy(self):
        return
