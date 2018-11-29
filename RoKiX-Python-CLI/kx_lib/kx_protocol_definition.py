# 
# Copyright 2018 Kionix Inc.
#
# pylint: disable=bad-whitespace
#
# definitions for kionix evaluation kit protocol
#
EVKIT_ERROR_BASE_NUM                                    = 0x00

# Status code
EVKIT_SUCCESS                                           = (EVKIT_ERROR_BASE_NUM + 0)
EVKIT_BUS1_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 1)
EVKIT_BUS2_ERROR                                        = (EVKIT_ERROR_BASE_NUM + 2)
EVKIT_GPIO_INVALID                                      = (EVKIT_ERROR_BASE_NUM + 3)
EVKIT_GPIO_RESERVED                                     = (EVKIT_ERROR_BASE_NUM + 4)
EVKIT_MAX_GPIO_RESERVED                                 = (EVKIT_ERROR_BASE_NUM + 5)
EVKIT_MAX_EXE_PARAMS_ERROR                              = (EVKIT_ERROR_BASE_NUM + 6)
EVKIT_INTERRUPT_WAITING                                 = (EVKIT_ERROR_BASE_NUM + 7)
EVKIT_INTERRUPT_DETECTED                                = (EVKIT_ERROR_BASE_NUM + 8)
EVKIT_DATA_READ_ERROR                                   = (EVKIT_ERROR_BASE_NUM + 9)
EVKIT_DATA_STREAM_ACTIVE                                = (EVKIT_ERROR_BASE_NUM + 10)
EVKIT_GPIO_STATUS_READ_ERROR                            = (EVKIT_ERROR_BASE_NUM + 11)
EVKIT_MSG_LENGHT_ERROR                                  = (EVKIT_ERROR_BASE_NUM + 12)
EVKIT_BUS2_BUFFER_FULL                                  = (EVKIT_ERROR_BASE_NUM + 13)
EVKIT_INVALID_MESSAGE                                   = (EVKIT_ERROR_BASE_NUM + 14)
EVKIT_INVALID_STATE                                     = (EVKIT_ERROR_BASE_NUM + 15)

# constants
EVKIT_PROTOCOL_VERSION_MAJOR                            = 0x01
EVKIT_PROTOCOL_VERSION_MINOR                            = 0x01

# Input/Output pin settings: Pin direction.
EVKIT_MSG_GPIO_PIN_INPUT				     	        = 0x00
EVKIT_MSG_GPIO_PIN_OUTPUT			      		        = 0x01

# Input pin settings: Connect/Disconnect to input buffer.
EVKIT_MSG_GPIO_PIN_DISCONNECTED				     	    = 0x00
EVKIT_MSG_GPIO_PIN_CONNECTED			      		    = 0x01

# Input pin settings.
# TODO 2 REMOVE/CLEANUP synch with .h files
EVKIT_MSG_GPIO_PIN_NOSENSE                              = 0x00
EVKIT_MSG_GPIO_PIN_SENSE_LOW                            = 0x01
EVKIT_MSG_GPIO_PIN_SENSE_HIGH                           = 0x02

# TODO 2 REMOVE/CLEANUP synch with .h files
EVKIT_MSG_GPIO_PIN_NOPULL                               = 0x00
EVKIT_MSG_GPIO_PIN_PULLDOWN                             = 0x01
EVKIT_MSG_GPIO_PIN_PULLUP                               = 0x02

EVKIT_GPIO_PIN_NOSENSE                                  = 0x00
EVKIT_GPIO_PIN_SENSE_LOW                                = 0x01
EVKIT_GPIO_PIN_SENSE_HIGH                               = 0x02

EVKIT_GPIO_PIN_NOPULL                                   = 0x00
EVKIT_GPIO_PIN_PULLDOWN                                 = 0x01
EVKIT_GPIO_PIN_PULLUP                                   = 0x02

# Output pin settings: Pin to be float or drive Low/High.
EVKIT_GPIO_PIN_NODRIVE					     	        = 0x00
EVKIT_GPIO_PIN_DRIVELOW				      		        = 0x01
EVKIT_GPIO_PIN_DRIVEHIGH				     	        = 0x02

EVKIT_RESET_SOFT                                        = 0x00
EVKIT_RESET_HARD                                        = 0x01

# Note! curently ms is only supported 16bit unsigned value
# Time is 16bit usigned value, range 1-65536
EVKIT_TIME_SCALE_US                                     = 0x00 # Microseconds, in Nordic minimum value supported by the RTC timer is 153us(Low power timer).
EVKIT_TIME_SCALE_MS                                     = 0x01 # Default => Milliseconds
EVKIT_TIME_SCALE_S                                      = 0x02 # Seconds
EVKIT_TIME_SCALE_M                                      = 0x03 # Minutes

EVKIT_ACTION_READ_SENSOR_DATA                           = 0x00 # default

# protocol messages
EVKIT_MSG_READ_REQ                                      = 0x01
EVKIT_MSG_READ_RESP                                     = 0x02

EVKIT_MSG_WRITE_REQ                                     = 0x03
EVKIT_MSG_WRITE_RESP                                    = 0x04

EVKIT_MSG_VERSION_REQ                                   = 0x05
EVKIT_MSG_VERSION_RESP                                  = 0x06

EVKIT_MSG_ENABLE_INT_REQ                                = 0x07
EVKIT_MSG_ENABLE_INT_RESP                               = 0x08

EVKIT_MSG_DISABLE_INT_REQ                               = 0x09
EVKIT_MSG_DISABLE_INT_RESP                              = 0x10

EVKIT_MSG_GPIO_STATE_REQ                                = 0x0E
EVKIT_MSG_GPIO_STATE_RESP                               = 0x0F

EVKIT_MSG_ERROR_IND                                     = 0x11
EVKIT_MSG_RESET_REQ                                     = 0x12 # no response sent from this req

EVKIT_MSG_INTERRUPT_IND1                                = 0x0A
EVKIT_MSG_INTERRUPT_IND2                                = 0x0B
EVKIT_MSG_INTERRUPT_IND3                                = 0x0C
EVKIT_MSG_INTERRUPT_IND4                                = 0x0D

EVKIT_MSG_GPIO_CONFIG_REQ	    		                = 0x13
EVKIT_MSG_GPIO_CONFIG_RESP  					        = 0x14
