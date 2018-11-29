# 
# Copyright 2018 Kionix Inc.
#
from array import array
from kx_lib.kx_exception import ProtocolBus1Exception, EvaluationKitException
from kx_lib import kx_logger
from kx_lib.kx_base_class import KxAdapterBase
from kx_lib.kx_configuration_enum import BUS1_I2C, BUS1_SPI
LOGGER = kx_logger.get_logger(__name__)
#LOGGER.setLevel(kx_logger.DEBUG)

AARDVARK_FOUND = False
try:
    from kx_lib import aardvark_py as aa
    AARDVARK_FOUND = True
except (ImportError, SyntaxError):
    # TODO 3 try to import linux aardvark if running in Linux environment
    LOGGER.debug('Aadvark found {}'.format(AARDVARK_FOUND))

class KxAdapterAardvark(KxAdapterBase):
    # TODO 3 demonstarte how to put sensor to hs mode

    def __init__(self, bus1config):
        LOGGER.debug('>init')
        if not AARDVARK_FOUND:
            raise EvaluationKitException('Aardvark libraries not found/installed.')

        KxAdapterBase.__init__(self)
        self.fw_protocol_version = "2.0"
        self.bus1config = bus1config
        self._adapter_configured = None # None / BUS1_I2C / BUS1_SPI

        self.bus_gpio_list = [1, 2]
        self._has_gpio = True
        self._handle = None
        self._bitrate = None

        # I2C related settings
        self._aa_target_power = {
            'AA_TARGET_POWER_BOTH': aa.AA_TARGET_POWER_BOTH,
            'AA_TARGET_POWER_NONE': aa.AA_TARGET_POWER_NONE
        }
        self._aa_i2c_pullup = {
            'AA_I2C_PULLUP_BOTH': aa.AA_I2C_PULLUP_BOTH,
            'AA_I2C_PULLUP_NONE': aa.AA_I2C_PULLUP_NONE,
        }

        # SPI related settings
        self._polarity = {'RISING_FALLING': aa.AA_SPI_POL_RISING_FALLING,
                          'FALLING_RISING': aa.AA_SPI_POL_FALLING_RISING}

        self._phase = {'SETUP_SAMPLE': aa.AA_SPI_PHASE_SETUP_SAMPLE,
                       'SAMPLE_SETUP': aa.AA_SPI_PHASE_SAMPLE_SETUP}

        self._ss_polarity = {'ACTIVE_HIGH': aa.AA_SPI_SS_ACTIVE_HIGH,
                             'ACTIVE_LOW': aa.AA_SPI_SS_ACTIVE_LOW}

        self._bitorder = {'MSB': aa.AA_SPI_BITORDER_MSB,
                          'LSB': aa.AA_SPI_BITORDER_LSB}

        self.adapter_connect()
        LOGGER.debug('<init')

    def adapter_connect(self):
        LOGGER.debug('<')
        (num, ports, unique_ids) = aa.aa_find_devices_ext(16, 16)
        del unique_ids
        if num == 0:
            raise EvaluationKitException('Aardvark i2c/spi host adapter not connected.')
        elif num == -2:
            raise EvaluationKitException('Aardvark i2c/spi host adapter never connected.')
        else:
            self._ports = ports[0]
            if num > 1:
                LOGGER.warning('More that 1 Aardvark ports found. Selecting 1st one.')

        # with "port_index" it is possible to support multiple simultanously connected Aardvarks
        self._handle = aa.aa_open(self.bus1config['port_index'])
        if self._handle < 0:
            if self._handle == -7:
                raise EvaluationKitException(
                    'bus_aadvark_i2c.open failed with error code %d (Aardvark disconnected)' % self._handle)
            else:
                raise EvaluationKitException('bus_aadvark_i2c.open failed with error code %d' % self._handle)

    def adapter_read_gpio(self, gpio_pin):
        LOGGER.debug('<')
        # TODO 3 more logic needed to read int pins with aardvark
        assert self._adapter_configured is not None
        assert gpio_pin in self.bus_gpio_list

        if self._adapter_configured == BUS1_SPI:
            if gpio_pin == 1: # int1
                return 0 if (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SCL) == 0 else 1
            else: # int2
                return 0 if (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SDA) == 0 else 1
        else:
            # i2c
            if gpio_pin == 1: # int1
                return 0 if (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_SCK) == 0 else 1
            else: # int2
                return 0 if (aa.aa_gpio_get(self._handle) & aa.AA_GPIO_MOSI) == 0 else 1

    def configure_i2c(self):
        LOGGER.debug('<')
        assert self._adapter_configured is None
        # IO direction now all input, do this before AA_CONFIG_GPIO_I2C
        aa.aa_gpio_direction(self._handle, self.bus1config['aa_gpio_direction'])

        # select pullup or floating
        # aa.aa_gpio_pullup(self._handle, aa.AA_GPIO_SCK | aa.AA_GPIO_MOSI) # pullup for gpio lines
        aa.aa_gpio_pullup(self._handle, self.bus1config['aa_gpio_pullup'])

        # TODO 3 slave address selection GPIO to output. this can be hadled with 'gpio_conf'

        # Ensure that the I2C subsystem is enabled
        aa.aa_configure(self._handle, aa.AA_CONFIG_GPIO_I2C)

        # Enable the I2C bus pullup resistors (2.2k resistors).
        # This command is only effective on v2.0 hardware or greater.
        # The pullup resistors on the v1.02 hardware are enabled by default.
        aa.aa_i2c_pullup(self._handle, self._aa_i2c_pullup[self.bus1config['aa_i2c_pullup']])

        # Power the board using the Aardvark adapter's power supply.
        # This command is only effective on v2.0 hardware or greater.
        # The power pins on the v1.02 hardware are not enabled by default.
        aa.aa_target_power(self._handle, self._aa_target_power[self.bus1config['aa_target_power']])

        # Set the bitrate
        self._bitrate = self.bus1config['bitrate_i2c'] # TODO 3 change to 'freq'
        requested = self._bitrate
        self._bitrate = aa.aa_i2c_bitrate(self._handle, self._bitrate)
        if requested != self._bitrate:
            LOGGER.warning('Bitrate set to %d kHz. Wanted to set %d kHz' % (self._bitrate, requested))

        self._adapter_configured = BUS1_I2C

    def configure_spi(self):
        LOGGER.debug('<')
        assert self._adapter_configured is None

        LOGGER.debug('aa_gpio_direction %d' % self.bus1config['aa_gpio_direction'])
        aa.aa_gpio_direction(self._handle, self.bus1config['aa_gpio_direction'])  # IO direction

        LOGGER.debug('aa_gpio_pullup %d' % self.bus1config['aa_gpio_pullup'])
        aa.aa_gpio_pullup(self._handle, self.bus1config['aa_gpio_pullup'])

        aa.aa_configure(self._handle, aa.AA_CONFIG_SPI_GPIO)  # SPI subsystem is enabled

        LOGGER.debug('aa_target_power %d' % self._aa_target_power[self.bus1config['aa_target_power']])
        aa.aa_target_power(self._handle, self._aa_target_power[self.bus1config['aa_target_power']])

        LOGGER.debug('polarity %d' % self._polarity[self.bus1config['polarity']])
        LOGGER.debug('phase %d' % self._phase[self.bus1config['phase']])
        LOGGER.debug('bitorder %d' % self._bitorder[self.bus1config['bitorder']])

        aa.aa_spi_configure(
            self._handle,
            self._polarity[self.bus1config['polarity']],
            self._phase[self.bus1config['phase']],
            self._bitorder[self.bus1config['bitorder']])

        LOGGER.debug('ss_polarity %d' % self._ss_polarity[self.bus1config['ss_polarity']])
        aa.aa_spi_master_ss_polarity(self._handle,
                                     self._ss_polarity[self.bus1config['ss_polarity']])


        # Set the bitrate
        LOGGER.debug('bitrate_spi %d' % self.bus1config['bitrate_spi'])
        self._bitrate = self.bus1config['bitrate_spi']  # TODO 3 change to 'freq'

        requested = self._bitrate
        self._bitrate = aa.aa_spi_bitrate(self._handle, self._bitrate)
        if requested != self._bitrate:
            LOGGER.warning('Bitrate set to %d kHz. Wanted to set %d kHz' % (self._bitrate, requested))

        self._adapter_configured = BUS1_SPI
        LOGGER.debug('>')

    def adapter_disconnect(self):
        LOGGER.debug('>disconnect')
        assert self._handle > 0, 'Connection is already close.'
        aa.aa_close(self._handle)
        self._handle = None
        LOGGER.debug('<disconnect')

    def adapter_write_sensor_register_i2c(self, _, sad, register, values):
        LOGGER.debug('<')

        if isinstance(values, int):
            length = 2
            data_out = array('B', [register, values])
        elif isinstance(values, (list, tuple)):
            values = list(values)
            length = 1 + len(values)
            data_out = array('B', [register] + values)

        # TODO 3 test below option
        elif register is None:
            # special case : write without dedicated register address
            length = len(values)
            data_out = array('B', [values])
        else:
            raise EvaluationKitException('Datatype "%s" not supported.' % type(values))

        res = aa.aa_i2c_write(self._handle, sad, aa.AA_I2C_NO_FLAGS, data_out)
        if res != length:
            # TODO 3 add sensor name to error message
            raise EvaluationKitException('Unable write to I2C slave at address 0x%x' % sad)

    def adapter_read_sensor_register_i2c(self, _, sad, register, length=1):
        if self._adapter_configured is None:
            self.configure_i2c()
        assert self._adapter_configured == BUS1_I2C

        aa.aa_i2c_write(self._handle, sad, aa.AA_I2C_NO_STOP, array('B', [register]))  # write address
        (count, data_in) = aa.aa_i2c_read(self._handle, sad, aa.AA_I2C_NO_FLAGS, length)  # read data
        if count != length:
            raise ProtocolBus1Exception('No response from I2C slave at address 0x%x' % sad)

        return data_in

    def adapter_read_sensor_register_spi(self, _, chip_select, register, length=1):
        if self._adapter_configured is None:
            self.configure_spi()
        assert self._adapter_configured == BUS1_SPI

        # TODO 3 how to handle chip select
        # TODO 3 "target" can be used for selecting between i2c and spi but currently no needs for it.
        data_in = aa.array_u08(1 + length)
        data_out = array('B', [register] + [0] * length)

        try:
            (count, data_in) = aa.aa_spi_write(self._handle, data_out, data_in)  # write address
        except TypeError:
            raise EvaluationKitException('Cannot read sensor from SPI bus.')

        #LOGGER.debug( 'count,length %d %d ' %(count,length))
        assert count == length + 1
        return data_in[1:]

    def adapter_write_sensor_register_spi(self, _, chip_select, register, values):

        # TODO 3 how to handle chip select
        # TODO 3 "target" is not in use
        LOGGER.debug('<')
        if register is None:  # Pure SPI command write without address
            # TODO 3 test this
            data_out = array('B', [values])
            length = 1  ## TODO 3 support for multi byte write?

        elif isinstance(values, int):
            length = 2
            data_out = array('B', [register, values])

        elif isinstance(values, (list, tuple)):
            values = list(values)
            length = 1 + len(values)
            data_out = array('B', [register] + values)
        else:
            raise ProtocolBus1Exception("unsupported value")

        res, dummy_data = aa.aa_spi_write(self._handle, data_out, 0)  # write the reg.address and data
        if res != length:
            raise EvaluationKitException('Unable write to SPI slave')
        LOGGER.debug('>')

    def configure_pin_as_input(self, gpio_pin, drivemode):
        # TODO 3 configure_pin_as_input(). 
        # Pins are set input in configure_i2c() and configure_spi() no need to do anything here
        # unless there is need to use pins also for output
        pass
