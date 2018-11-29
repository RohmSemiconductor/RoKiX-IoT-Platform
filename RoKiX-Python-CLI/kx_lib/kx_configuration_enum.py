# 
# Copyright 2018 Kionix Inc.
#
# constant definitions without dependencies to other modules.

# board config related definitions
from collections import OrderedDict
[SENSOR_TYPE_DIGITAL_1D, \
SENSOR_TYPE_DIGITAL_2D, \
SENSOR_TYPE_DIGITAL_3D, \
SENSOR_TYPE_DIGITAL_6D, \
SENSOR_TYPE_ANALOG_1D, \
SENSOR_TYPE_ANALOG_3D] = range(6)

BUS1 = 'bus1'
BUS1_I2C = 'i2c'
BUS1_SPI = 'spi'
BUS1_ADC = 'adc'
BUS1_GPIO = 'gpio'

INT1_GPIO = 'gpio1'
INT2_GPIO = 'gpio2'
INT3_GPIO = 'gpio3'
INT4_GPIO = 'gpio4'

INT_GPIO_DICT = OrderedDict((
    (1, INT1_GPIO),
    (2, INT2_GPIO),
    (3, INT3_GPIO),
    (4, INT4_GPIO)
))

ADC1_GPIO = 'gpio1'
ADC2_GPIO = 'gpio2'
ADC3_GPIO = 'gpio3'

ADC_GPIO_DICT = OrderedDict((
    (1, ADC1_GPIO),
    (2, ADC2_GPIO),
    (3, ADC3_GPIO)
))

BUS2_BLE = 'BLE'
BUS2_USB = 'USB'
BUS2_SOCKET = 'SOCKET'
BUS2_USB_SERIAL = 'USB_SERIAL'
BUS2_USB_AARDVARK = 'USB_AARDVARK'

CFG_SAD = 'SAD'
CFG_CS = 'cs'
CFG_NAME = 'name'
CFG_CONFIGURATION = 'configuration'
CFG_CONNECTION = 'connection'
CFG_TARGET = 'target'
CFG_ADC_RESOLUTION = 'adc_msg_resolution_int'
CFG_ADC_REF_V = 'adc_ref_v'
CFG_ADC_GAIN = 'adc_gain'
CFG_SPI_PROTOCOL = 'protocol'
CFG_POLARITY = 'polarity'
CFG_PULLUP = 'pullup'
CFG_AXIS_MAP = 'axis_map'
CFG_FREQ = 'freq'
CFG_SPI_MODE = 'spi_mode'

# textual version of protocol emums
EVKIT_GPIO_PIN_SENSE_HIGH = 'EVKIT_GPIO_PIN_SENSE_HIGH'
EVKIT_GPIO_PIN_SENSE_LOW = 'EVKIT_GPIO_PIN_SENSE_LOW'

EVKIT_GPIO_PIN_NOPULL = 'EVKIT_GPIO_PIN_NOPULL'
EVKIT_GPIO_PIN_PULLDOWN = 'EVKIT_GPIO_PIN_PULLDOWN'
EVKIT_GPIO_PIN_PULLUP = 'EVKIT_GPIO_PIN_PULLUP'

# definitions for sensor channels
CH_ACC, CH_MAG, CH_GYRO, CH_TEMP, CH_SLAVE1, CH_SLAVE2, CH_BATT = [2**t for t in range(7)]
# interrut signal polarity definition
ACTIVE_LOW, ACTIVE_HIGH = range(2)


# dictionaries to map board config keys to integers
POLARITY_DICT = {
    EVKIT_GPIO_PIN_SENSE_HIGH:ACTIVE_HIGH,
    EVKIT_GPIO_PIN_SENSE_LOW:ACTIVE_LOW,
    }

# protocol message independent pin pullup definition
NOPULL, PULLDOWN, PULLUP = range(3)
PULL_DICT = {
    EVKIT_GPIO_PIN_NOPULL:NOPULL,
    EVKIT_GPIO_PIN_PULLDOWN:PULLDOWN,
    EVKIT_GPIO_PIN_PULLUP:PULLUP
    }

DRIVELOW, DRIVEHIGH, NODRIVE = (0, 1, 2)

# version number for board configuration json file
SUPPORTED_BOARD_CONFIGURATION_VERSIONS = ["2.0"]
SUPPORTED_FIRMWARE_PROTOCOL_VERSIONS = ["2.0", "1.1", "1.2"]

# protocol message max size
MAX_PACKET_SIZE = 20
