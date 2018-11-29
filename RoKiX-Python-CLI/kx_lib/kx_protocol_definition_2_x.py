# 
# Copyright 2018 Kionix Inc.
#
# pylint: disable=bad-whitespace
#
# Protocol Definitions.
#
EVKIT_PROTOCOL_VERSION_MAJOR                            = 0x02
EVKIT_PROTOCOL_VERSION_MINOR                            = 0x00

# Status code
EVKIT_ERROR_BASE_NUM                                    = 0x00

EVKIT_SUCCESS                                           = (EVKIT_ERROR_BASE_NUM + 0)
EVKIT_ERR_BUS1                                          = (EVKIT_ERROR_BASE_NUM + 1)
EVKIT_ERR_BUS2                                          = (EVKIT_ERROR_BASE_NUM + 2)
EVKIT_ERR_HW_RESERVED                                   = (EVKIT_ERROR_BASE_NUM + 3)
EVKIT_ERR_FORBIDDEN                                     = (EVKIT_ERROR_BASE_NUM + 4)
EVKIT_ERR_GPIO                                          = (EVKIT_ERROR_BASE_NUM + 5)
EVKIT_ERR_TIMER                                         = (EVKIT_ERROR_BASE_NUM + 6)
EVKIT_ERR_INVALID_MSG                                   = (EVKIT_ERROR_BASE_NUM + 7)
EVKIT_ERR_INVALID_STATE                                 = (EVKIT_ERROR_BASE_NUM + 8)
EVKIT_ERR_INVALID_PARAM                                 = (EVKIT_ERROR_BASE_NUM + 9)
EVKIT_ERR_PARAM_OUT_OF_RANGE                            = (EVKIT_ERROR_BASE_NUM + 10)
EVKIT_ERR_FEAT_UNSUPPORTED                              = (EVKIT_ERROR_BASE_NUM + 11)
EVKIT_ERR_OUT_OF_MACROS                                 = (EVKIT_ERROR_BASE_NUM + 12)
EVKIT_ERR_OUT_OF_ACTIONS                                = (EVKIT_ERROR_BASE_NUM + 13)
EVKIT_ERR_BUF_OVERFLOW                                  = (EVKIT_ERROR_BASE_NUM + 14)

EVKIT_ERR_NAMES = {
    EVKIT_SUCCESS: "EVKIT_SUCCESS",
    EVKIT_ERR_BUS1: "EVKIT_ERR_BUS1",
    EVKIT_ERR_BUS2: "EVKIT_ERR_BUS2",
    EVKIT_ERR_HW_RESERVED: "EVKIT_ERR_HW_RESERVED",
    EVKIT_ERR_FORBIDDEN: "EVKIT_ERR_FORBIDDEN",
    EVKIT_ERR_GPIO: "EVKIT_ERR_GPIO",
    EVKIT_ERR_TIMER: "EVKIT_ERR_TIMER",
    EVKIT_ERR_INVALID_MSG: "EVKIT_ERR_INVALID_MSG",
    EVKIT_ERR_INVALID_STATE: "EVKIT_ERR_INVALID_STATE",
    EVKIT_ERR_INVALID_PARAM: "EVKIT_ERR_INVALID_PARAM",
    EVKIT_ERR_PARAM_OUT_OF_RANGE: "EVKIT_ERR_PARAM_OUT_OF_RANGE",
    EVKIT_ERR_FEAT_UNSUPPORTED: "EVKIT_ERR_FEAT_UNSUPPORTED",
    EVKIT_ERR_OUT_OF_MACROS: "EVKIT_ERR_OUT_OF_MACROS",
    EVKIT_ERR_OUT_OF_ACTIONS: "EVKIT_ERR_OUT_OF_ACTIONS",
    EVKIT_ERR_BUF_OVERFLOW: "EVKIT_ERR_BUF_OVERFLOW",
}

EVKIT_ERR_DESCS = {
    EVKIT_SUCCESS: "operation succeeded",
    EVKIT_ERR_BUS1: "sensor-bus operation failed",
    EVKIT_ERR_BUS2: "device-client bus operation failed",
    EVKIT_ERR_HW_RESERVED: "resource is already in use",
    EVKIT_ERR_FORBIDDEN: "operation is forbidden when a stream is active",
    EVKIT_ERR_GPIO: "GPIO pin does not support attempted operation",
    EVKIT_ERR_TIMER: "timer error",
    EVKIT_ERR_INVALID_MSG: "message header is invalid",
    EVKIT_ERR_INVALID_STATE: "cannot execute operation before version query",
    EVKIT_ERR_INVALID_PARAM: "message parameter is invalid",
    EVKIT_ERR_PARAM_OUT_OF_RANGE: "message parameter is out of range",
    EVKIT_ERR_FEAT_UNSUPPORTED: "attempted operation is not supported on this platform",
    EVKIT_ERR_OUT_OF_MACROS: "out of macros",
    EVKIT_ERR_OUT_OF_ACTIONS: "out of macro actions",
    EVKIT_ERR_BUF_OVERFLOW: "attempted operation would overflow the message buffer",
}

# Input/Output pin settings: Pin direction.
# Input pin settings.
# This is only used in interrupt request messages
# TODO 2 REMOVE/CLEANUP synch with .h files
EVKIT_MSG_GPIO_PIN_NOSENSE                              = 0x00
EVKIT_MSG_GPIO_PIN_SENSE_LOW                            = 0x01
EVKIT_MSG_GPIO_PIN_SENSE_HIGH                           = 0x02
EVKIT_GPIO_PIN_NOSENSE                                  = 0x00
EVKIT_GPIO_PIN_SENSE_LOW                                = 0x01
EVKIT_GPIO_PIN_SENSE_HIGH                               = 0x02

# TODO 2 rename EVKIT_GPIO_PIN_INPUT ...
EVKIT_MSG_GPIO_PIN_INPUT				     	        = 0x00
EVKIT_MSG_GPIO_PIN_OUTPUT			      		        = 0x01


# TODO 2 rename EVKIT_GPIO_PIN_NOPULL ...
# TODO 2 REMOVE/CLEANUP synch with .h files
EVKIT_MSG_GPIO_PIN_NOPULL                               = 0x00
EVKIT_MSG_GPIO_PIN_PULLDOWN                             = 0x01
EVKIT_MSG_GPIO_PIN_PULLUP                               = 0x02

# Input pin settings: Connect/Disconnect to input buffer.
# TODO 2 rename EVKIT_GPIO_PIN_DISCONNECTED ...
EVKIT_MSG_GPIO_PIN_DISCONNECTED				     	    = 0x00
EVKIT_MSG_GPIO_PIN_CONNECTED			      		    = 0x01

EVKIT_GPIO_PIN_NOPULL                                   = 0x00
EVKIT_GPIO_PIN_PULLDOWN                                 = 0x01
EVKIT_GPIO_PIN_PULLUP                                   = 0x02

# Output pin settings: Pin to be float or drive Low/High.
EVKIT_GPIO_PIN_NODRIVE                                  = 0x00
EVKIT_GPIO_PIN_DRIVELOW                                 = 0x01
EVKIT_GPIO_PIN_DRIVEHIGH                                = 0x02

EVKIT_RESET_SOFT                                        = 0x00
EVKIT_RESET_HARD                                        = 0x01

EVKIT_SELFTEST_RSSI                                     = 0x00
EVKIT_SELFTEST_MEM                                      = 0x01
EVKIT_SELFTEST_DISABLE_SD                               = 0x02

EVKIT_CPU_SLEEP_DISABLE                                 = 0x00
EVKIT_CPU_SLEEP_ENABLE                                  = 0x01

EVKIT_SPI_MODE_0                                        = 0x00
EVKIT_SPI_MODE_1                                        = 0x01
EVKIT_SPI_MODE_2                                        = 0x02
EVKIT_SPI_MODE_3                                        = 0x03

EVKIT_BUS1_TARGET_NONE                                  = 0x00
EVKIT_BUS1_TARGET_SPI0                                  = 0x01
EVKIT_BUS1_TARGET_SPI1                                  = 0x02
EVKIT_BUS1_TARGET_SPI2                                  = 0x03
EVKIT_BUS1_TARGET_TWI0                                  = 0x04
EVKIT_BUS1_TARGET_TWI1                                  = 0x05
EVKIT_BUS1_TARGET_TWI2                                  = 0x06
EVKIT_BUS1_TARGET_FW                                    = 0x07
EVKIT_BUS1_TARGET_ADC0                                  = 0x08

EVKIT_MACRO_ACTION_NONE                                 = 0x00 # default
EVKIT_MACRO_ACTION_READ                                 = 0x01
EVKIT_MACRO_ACTION_WRITE                                = 0x02
EVKIT_MACRO_ACTION_SPI_RW                               = 0x03
EVKIT_MACRO_ACTION_PKT_COUNT                            = 0x04
EVKIT_MACRO_ACTION_TIMESTAMP                            = 0x05
EVKIT_MACRO_ACTION_ADC_READ                             = 0x06
EVKIT_MACRO_ACTION_GPIO_READ                            = 0x07
EVKIT_MACRO_ACTION_GPIO_WRITE                           = 0x08

# Macro types
EVKIT_MACRO_TYPE_INTR                                   = 0x00
EVKIT_MACRO_TYPE_POLL                                   = 0x01

# Time is 16bit usigned value, range 1-65536
EVKIT_TIME_SCALE_US                                     = 0x01 # Microseconds, in Nordic minimum value supported by the RTC timer is 153us(Low power timer).
EVKIT_TIME_SCALE_MS                                     = 0x02 # Default => Milliseconds
EVKIT_TIME_SCALE_S                                      = 0x03 # Seconds
EVKIT_TIME_SCALE_M                                      = 0x04 # Minutes
EVKIT_TIME_SCALE_NATIVE                                 = 0x05  # platform-specific (e.g. systicks)

EVKIT_BITWIDTH_8                                        = 0x00
EVKIT_BITWIDTH_16                                       = 0x01
EVKIT_BITWIDTH_32                                       = 0x02
EVKIT_ADC_GAIN_NONE                                     = 0x00
EVKIT_ADC_GAIN_A                                        = 0x01
EVKIT_ADC_GAIN_B                                        = 0x02
EVKIT_ADC_GAIN_C                                        = 0x03
EVKIT_ADC_GAIN_D                                        = 0x04
EVKIT_ADC_GAIN_E                                        = 0x05
EVKIT_ADC_GAIN_F                                        = 0x06
EVKIT_ADC_GAIN_G                                        = 0x07
EVKIT_ADC_GAIN_H                                        = 0x08

EVKIT_ADC_OVERSAMPLE_NONE                               = 0x00
EVKIT_ADC_OVERSAMPLE_2X                                 = 0x01
EVKIT_ADC_OVERSAMPLE_4X                                 = 0x02
EVKIT_ADC_OVERSAMPLE_8X                                 = 0x03
EVKIT_ADC_OVERSAMPLE_16X                                = 0x04

#  Device information types
EVKIT_DEV_ID                                            = 0x00
EVKIT_FW_SW_VER                                         = 0x01

EVKIT_MACRO_APPLY_ACTION_ALL                            = 0xff

# protocol messages
EVKIT_MSG_VERSION_REQ                                   = 0x05
EVKIT_MSG_VERSION_RESP                                  = 0x06


EVKIT_MSG_READ_REQ                                      = 0x03
EVKIT_MSG_READ_RESP                                     = 0x04

EVKIT_MSG_WRITE_REQ                                     = 0x01
EVKIT_MSG_WRITE_RESP                                    = 0x02

EVKIT_MSG_GPIO_STATE_REQ                                = 0x07
EVKIT_MSG_GPIO_STATE_RESP                               = 0x08

EVKIT_MSG_GPIO_CONFIG_REQ	    		                = 0x09
EVKIT_MSG_GPIO_CONFIG_RESP  					        = 0x0a

EVKIT_MSG_CREATE_MACRO_REQ                              = 0x0b
EVKIT_MSG_CREATE_MACRO_RESP                             = 0x0c

EVKIT_MSG_REMOVE_MACRO_REQ                              = 0x0d
EVKIT_MSG_REMOVE_MACRO_RESP                             = 0x0e

EVKIT_MSG_ADD_MACRO_ACTION_REQ                          = 0x0f
EVKIT_MSG_ADD_MACRO_ACTION_RESP                         = 0x10

EVKIT_MSG_START_MACRO_REQ                               = 0x11
EVKIT_MSG_START_MACRO_RESP                              = 0x12

EVKIT_MSG_STOP_MACRO_REQ                                = 0x13
EVKIT_MSG_STOP_MACRO_RESP                               = 0x14

EVKIT_MSG_RESET_REQ                                     = 0x15 # no response sent from this req
EVKIT_MSG_ERROR_IND                                     = 0x16
EVKIT_MSG_SELFTEST_REQ                                  = 0x17
EVKIT_MSG_SELFTEST_RESP                                 = 0x18
EVKIT_MSG_SPI_RW_REQ                                    = 0x19
EVKIT_MSG_SPI_RW_RESP                                   = 0x1a
EVKIT_MSG_DEV_INFO_REQ                                  = 0x1b
EVKIT_MSG_DEV_INFO_RESP                                 = 0x1c

EVKIT_MSG_ADC_READ_REQ                                  = 0x1d
EVKIT_MSG_ADC_READ_RESP                                 = 0x1e

EVKIT_MSG_CONFIGURE_REQ                                 = 0x1F
EVKIT_MSG_CONFIGURE_RESP                                = 0x20


# parameter for EVKIT_MACRO_TYPE_POLL
EVKIT_TIME_SCALE_US                                     = 0x01
EVKIT_TIME_SCALE_MS                                     = 0x02
EVKIT_TIME_SCALE_S                                      = 0x03
EVKIT_TIME_SCALE_M                                      = 0x04

EVKIT_MSG_MACRO_IND_BASE                                = 0x30
