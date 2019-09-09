# 
# Copyright 2018 Kionix Inc.
#
import inspect


class CfgSchema(dict):
    board = {
        "type": "string",
        "description": "Board configuration file",
        "title": "-b",
        "examples": [
            "rokix_board_rokix_sensor_node_i2c.json",
            "rokix_board_rokix_sensor_node_i2c_addon.json"
        ]
    }
    bus2 = {
        "type": "string",
        "description": "Bus2 connection",
        "default": "USB",
        "enum": [
            "USB",
            "BLE_PYGATT",
            "USB_SERIAL",
            "USB_AARDVARK",
            "BLE"
        ]
    }

    serial_port = {
        "type": "string",
        "description": "Serial COM port to use",
        "default": "auto"
    }

    socket_ip = {
        "type": "string",
        "description": "IP address for socket connection"
    }

    ble_mac = {
        "type": ["string", "null"],
        "description": "Mac address for bluetooth connection. Full address (or first bytes with windows)"
    }

    logging_level = {
        "type": "string",
        "description": "Global debug logging settings",
        "enum": [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL"
        ]
    }

    drdy_function_mode = {
        "type": "string",
        "description": "This setting defines how data ready function works in *_data_logger.py application",
        "default": "ADAPTER_GPIO1_INT",
        "enum": [
            "ADAPTER_GPIO1_INT",
            "ADAPTER_GPIO2_INT",
            "REG_POLL",
            "TIMER_POLL"
        ]
    }

    drdy_timer_interval = {
        "type": "number",
        "description": "Dataready poll interval in seconds if drdy_function_mode is TIMER_POLL",
        "default": 0.04,
    }

    other_function_mode = {
        "type": "string",
        "description": "This setting defines how asic feature event works in applications where the features is enabled",
        "default": "ADAPTER_GPIO1_INT",
        "enum": [
            "ADAPTER_GPIO1_INT",
            "ADAPTER_GPIO2_INT",
            "REG_POLL",
            "TIMER_POLL"
        ]
    }

    other_timer_interval = {
        "type": "number",
        "description": """Other function such as wakeup status poll interval in seconds
         if other_function_mode is TIMER_POLL""",
        "default": 0.04,
    }

    max_timeout_count = {
        "type": "integer",
        "description": "",
        "default": 1,
    }

    odr = {
        "type": "number",
        "description": "Output data rate",
        "title": "-o",
        "default": 25.0
    }

    loop = {
        "type": ["integer", "null"],
        "description": "Number of data samples",
        "title": "-l",
        "default": None
    }

    stream_mode = {
        "type": "boolean",
        "description": "Streaming mode on/off, 1/0, True/False",
        "title": "-s",
        "default": True
    }

    filename = {
        "type": ["string", "null"],
        "description": "File name with or without extension. If no extension is given .csv is used",
        "default": None,
    }

    def __init__(self, required=None):
        if required is None:
            required = []

        schema = {
            "$schema": "https://json-schema.org/draft-07/schema",
            "type": "object",
            "properties": {
                option[0]: option[1] for option in inspect.getmembers(
                    CfgSchema,
                    predicate=lambda x: isinstance(x, dict)
                )
            },
            "required": required
        }
        super(CfgSchema, self).__init__(schema)
