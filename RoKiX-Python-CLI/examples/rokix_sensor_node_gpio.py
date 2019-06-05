# 
# Copyright 2018 Kionix Inc.
#
import time
import imports  # pylint: disable=unused-import
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_configuration_enum import PULLDOWN, BUS1_ADC, SENSOR_TYPE_ANALOG_1D
from kx_lib.kx_sensor_base import AnalogSensorDriver
from kx_lib import kx_logger, kx_exception

from kx_lib.kx_configuration_enum import CH_BATT, CFG_ADC_RESOLUTION, CFG_ADC_REF_V, CFG_ADC_GAIN

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class RoKixSensorNode(object):
    # RGY LED GPIO lines
    LED_Y = 35
    LED_G = 36  # this LED is indicating BLE status
    LED_R = 37

    # 14 pin Rohm 5+ connector GPIO lines
    # C14_01 = VDD
    # C14_03 = GND

    C14_02 = 12
    C14_04 = 29  # ADC capable pin
    C14_05 = 19
    C14_06 = 21
    C14_07 = 24
    C14_08 = 20
    C14_09 = 33
    C14_10 = 44
    C14_11 = 22
    C14_12 = 14
    C14_13 = 15
    C14_14 = 23

    # other GPIOs
    PWC = 25 # Power button P.025


def rgy_led_test():
    """ Blink red and yellow LEDs ten times. Disable green BLE indicator LED"""

    cm = ConnectionManager('../cfg/rokix_board_rokix_sensor_node_i2c.json')

    # make pin as input then green LED will be turned off
    print('Blinking onboard LEDs 10 times.')

    cm.read_gpio_pin(RoKixSensorNode.LED_G)

    try:
        for _ in range(10):
            cm.write_gpio_pin(RoKixSensorNode.LED_Y, 1)
            cm.write_gpio_pin(RoKixSensorNode.LED_R, 0)
            time.sleep(0.5)
            cm.write_gpio_pin(RoKixSensorNode.LED_Y, 0)
            cm.write_gpio_pin(RoKixSensorNode.LED_R, 1)
            time.sleep(0.5)

    finally:
        # enable BLE indicator LED by making line as output
        # restore initial led states
        cm.write_gpio_pin(RoKixSensorNode.LED_Y, 1)
        cm.write_gpio_pin(RoKixSensorNode.LED_R, 0)
        cm.write_gpio_pin(RoKixSensorNode.LED_G, 1)

        cm.disconnect()


def gpio_write_test():
    """ Blink one GPIO line ten times"""
    cm = ConnectionManager('../cfg/rokix_board_rokix_sensor_node_i2c.json')

    gpio_output = RoKixSensorNode.C14_02
    print('Connect LED to GND and pad 2 of RoKiX No and see it blinks 10 times.')

    for _ in range(10):
        cm.write_gpio_pin(gpio_output, 1)
        time.sleep(0.2)
        cm.write_gpio_pin(gpio_output, 0)
        time.sleep(0.2)

    cm.disconnect()

def power_off_test():
    """ Turn nRf52840 SoC's LDO regulator. This will shut down the SoC."""
    cm = ConnectionManager('../cfg/rokix_board_rokix_sensor_node_i2c.json')

    # set LED GPIO lines to input e.g. LEDs goes off
    cm.read_gpio_pin(RoKixSensorNode.LED_R)
    cm.read_gpio_pin(RoKixSensorNode.LED_G)
    cm.read_gpio_pin(RoKixSensorNode.LED_Y)

    gpio_output = RoKixSensorNode.PWC
    print('Press enter to toggle RoKiX Sensor Node power button down')
    input()
    cm.write_gpio_pin(gpio_output, 0)
    print('Press enter to toggle RoKiX Sensor Node power button op')
    input()
    try:
        cm.write_gpio_pin(gpio_output, 1)
    except kx_exception.ProtocolTimeoutException:
        print('RoKiX Sensor Node powered off.')

    #cm.disconnect()


def gpio_test():
    """ Change GPIO output pin state according to GPIO input pin state"""
    cm = ConnectionManager('../cfg/rokix_board_rokix_sensor_node_i2c.json')

    # select used pins here
    gpio_input = RoKixSensorNode.C14_13
    gpio_output = RoKixSensorNode.C14_02

    print('Connect LED to GND and pad 2 and toggle Vdd to pad 13. CTRL+C to stop.')

    try:
        while True:
            cm.write_gpio_pin(gpio_output, cm.read_gpio_pin(gpio_input, pull=PULLDOWN))
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    finally:
        cm.disconnect()


def adc_test():
    """ Read ADC data"""
    class AnalogSensor1D(AnalogSensorDriver):

        def __init__(self):
            AnalogSensorDriver.__init__(self)
            self.supported_connectivity = [BUS1_ADC]
            self.int_pins = [1]
            self.name = 'AnalogSensor'
            self.sensor_type = SENSOR_TYPE_ANALOG_1D

        def probe(self):
            self.connected = True
            return 1

        def _read_data(self, channel=None):
            return self.connection_manager.read_adc(self)

        def set_power_off(self, channel=None):
            pass

        def set_power_on(self, channel=None):
            pass

    cm = ConnectionManager('../cfg/rokix_board_rokix_sensor_node_i2c.json')
    sensor = AnalogSensor1D()
    cm.add_sensor(sensor)

    print('Connect analog voltage to pad 4. CTRL+C to stop.')

    gain = sensor.resource[CFG_ADC_GAIN]
    vref = sensor.resource[CFG_ADC_REF_V]
    res = pow(2, sensor.resource[CFG_ADC_RESOLUTION])

    try:
        while True:
            # gains 1, 1/2, 1/4, 1/6
            # CONFIG.MODE=SE
            # Input range = (+- 0.6 V)/Gain
            # RESULT = [V(P)-V(N)] * GAIN / REFERENCE * 2^(RESOLUTION-m)

            # """
            #     V(P)
            #     is the voltage at input P
            #     V(N)
            #     is the voltage at input N
            #     GAIN
            #     is the selected gain setting
            #     REFERENCE
            #     is the selected reference voltage

            # """

            raw_value = sensor.read_data()[0]
            # print(raw_value)

            milli_volts = int(raw_value / ((gain / vref) * res) * 1000)
            print(milli_volts)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        cm.disconnect()


def app_main():
    """ Run the selected gpio tests"""
    # Select wanted test case

    #rgy_led_test()
    # gpio_write_test()
    # gpio_test()
    # adc_test()
    power_off_test()


if __name__ == '__main__':
    app_main()
