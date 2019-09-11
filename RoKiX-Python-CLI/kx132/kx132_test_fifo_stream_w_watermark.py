# The MIT License (MIT)
#
# Copyright (c) 2018 Kionix Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
# Example app for fifo stream mode
# watermark is used to syncronize data read actions (flush)
###
# watermark uses interrupt int1
###

import imports  # pylint: disable=unused-import
import time
import sys
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_datalogger_config, get_drdy_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, POLARITY_DICT, CFG_POLARITY, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT, REG_POLL
from kx_lib.kx_board import ConnectionManager
from kx_lib.kx_data_logger import SensorDataLogger
from kx132.kx132_driver import KX132Driver, r, b, m, e

_CODE_FORMAT_VERSION = 2.0

# fifo storage level parameters
## select watermark level#
watermark = 60          # samples, relates 8/16b resolution selection
buffer_full = [170, 85]  # samples, relates 8/16b resolution selection

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)


class Parameter_set_1:
    LOW_POWER_MODE = True               # low power or full resolution mode
    odr_OSA = 25
    acc_range = '2G'
    lp_average = '16_SAMPLE_AVG'
    low_pass_filter = 'ODR_9'


def enable_test_fifo(sensor,
                     cfg=Parameter_set_1,
                     BUFFER_RESOLUTION=16,
                     power_off_on=True,
                     int_number=None):

    LOGGER.info('Fifo stream init start')

    assert BUFFER_RESOLUTION in [8, 16], \
        'Invalid BUFFER_RESOLUTION value "{}". Valid values are {}'.format(
            BUFFER_RESOLUTION, [8, 16])

    assert convert_to_enumkey(cfg.odr_OSA) in e.KX132_1211_ODCNTL_OSA.keys(),\
        'Invalid odr_OSA value "{}". Valid values are {}'.format(
            cfg.odr_OSA, e.KX132_1211_ODCNTL_OSA.keys())

    assert cfg.lp_average in e.KX132_1211_LP_CNTL1_AVC.keys(),\
        'Invalid lp_average value "{}". Valid values are {}'.format(
            cfg.lp_average, e.KX132_1211_LP_CNTL1_AVC.keys())

    assert cfg.LOW_POWER_MODE in [True, False],\
        'Invalid LOW_POWER_MODE value "{}". Valid values are {}'.format(
            cfg.LOW_POWER_MODE, [True, False])

    assert cfg.acc_range in e.KX132_1211_CNTL1_GSEL.keys(), \
        'Invalid acc_range value "{}". Valid values are {}'.format(
            cfg.acc_range, e.KX132_1211_CNTL1_GSEL.keys())

    assert cfg.low_pass_filter in ['BYPASS', 'ODR_9', 'ODR_2'], 'Invalid filter value "{}". Valid values are: BYPASS or {}'.format(
        cfg.low_pass_filter, ['BYPASS', 'ODR_9', 'ODR_2'])

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        time.sleep(0.1)
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # Select ODR
    sensor.set_odr(e.KX132_1211_ODCNTL_OSA[convert_to_enumkey(cfg.odr_OSA)])           # set ODR

    # select g-range
    sensor.set_range(e.KX132_1211_CNTL1_GSEL[cfg.acc_range])

    # Select power mode
    if cfg.LOW_POWER_MODE:
        sensor.reset_bit(r.KX132_1211_CNTL1, b.KX132_1211_CNTL1_RES)                          # low current
        sensor.set_average(e.KX132_1211_LP_CNTL1_AVC[cfg.lp_average])
    else:
        sensor.set_bit(r.KX132_1211_CNTL1, b.KX132_1211_CNTL1_RES)                            # high resolution

    # set bandwitdh
    if cfg.low_pass_filter != 'BYPASS':
        if cfg.low_pass_filter == 'ODR_9':
            sensor.set_BW(0, 0, CH_ACC)
        else:
            sensor.set_BW(b.KX132_1211_ODCNTL_LPRO, 0, CH_ACC)
        sensor.enable_iir()
    else:
        sensor.disable_iir()

    # fifo: mode and resolution
    if BUFFER_RESOLUTION == 16:
        sensor.enable_fifo(b.KX132_1211_BUF_CNTL2_BM_STREAM, b.KX132_1211_BUF_CNTL2_BRES)     # trigger and 16b
    else:
        sensor.enable_fifo(b.KX132_1211_BUF_CNTL2_BM_STREAM, 0)                         # trigger and 8b
    sensor.set_bit(r.KX132_1211_BUF_CNTL2, b.KX132_1211_BUF_CNTL2_BFIE)                       # enable buffer full function

    #
    # interrupt pin routings and settings
    #
    #print (r.KX132_1211_BUF_CNTL2)

    _intpin = 0
    if int_number is None:
        if evkit_config.drdy_function_mode == ADAPTER_GPIO1_INT:
            _intpin = 1

        elif evkit_config.drdy_function_mode == ADAPTER_GPIO2_INT:
            _intpin = 2

        elif evkit_config.drdy_function_mode == REG_POLL:
            # interrupt must be enabled to get register updates
            sensor.enable_drdy(intpin=1)

        else:
            pass  # TIMER_POLL no need to do anything

    else:
        _intpin = int_number

    if _intpin > 0:
        LOGGER.debug('Configuring interrupt pin {}'.format(_intpin))
        if _intpin == 1:
            # latched interrupt
            # set KX132_INC1_IEN1 , reset KX132_INC1_IEL1
            sensor.set_bit_pattern(r.KX132_1211_INC1, b.KX132_1211_INC1_IEN1, b.KX132_1211_INC1_IEN1 | b.KX132_1211_INC1_IEL1)
        else:
            # latched interrupt
            # set KX132_INC5_IEN2 , reset KX132_INC5_IEL2
            sensor.set_bit_pattern(r.KX132_1211_INC5, b.KX132_1211_INC5_IEN2, b.KX132_1211_INC5_IEN2 | b.KX132_1211_INC5_IEL2)

        polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
        LOGGER.debug('Configuring interrupt polarity {}'.format(
            sensor.resource[CFG_POLARITY]))
        sensor.set_interrupt_polarity(intpin=_intpin, polarity=polarity)

        # use acc data ready
        # sensor.enable_drdy(intpin=_intpin)

    # interrupt pin routings and settings
    # sensor.set_bit(r.KX132_1211_INC4, b.KX132_1211_INC4_WMI1)     # watermark to int 1
    # sensor.set_bit(r.KX132_1211_INC1, b.KX132_1211_INC1_IEN1)     # enable int1 pin

    #
    # Turn on operating mode (disables setup)
    #
    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump();sys.exit()

    LOGGER.info('\nFifo and watermark event initialized.')

    sensor.release_interrupts()                         # clear all internal function interrupts
    sensor.clear_buffer()


def read_with_polling(sensor, loop):
    bufres = sensor.get_fifo_resolution()                   # buffer 8/16b
    assert(watermark <= buffer_full[bufres])
    sensor.set_fifo_watermark_level(watermark)

    count = 0
    dl = SensorDataLogger()
    dl.add_channel('ch!ax!ay!az')
    dl.start()

    int_polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
    try:
        sensor.clear_buffer()                               # clear buffer values
        cc = 0
        while (loop is None) or (count < loop):
            count += 1
            buf_storage = []
            # print ".",
            # sys.exit()

            if cc == 1:
                sss = 0
                # if evkit_config.get('generic','use_adapter_int_pins') == 'TRUE':

                #    status = sensor.bus.poll_gpio(1, int_polarity)
                #    if status == pin_condition:
                #        bytes_in_buffer = sensor.get_fifo_level()                   # buffer level
                #        for i in range(bytes_in_buffer):
                #            buf_storage.append(sensor.read_register(r.KX132_1211_BUF_READ, 6)) # fetch data from buffer and print status
                #        print 'samples got %d / %d' % (bytes_in_buffer / 6,  len(buf_storage)/6)
            else:
                aa = sensor.read_register(r.KX132_1211_INS2)[0]

                # if aa & b.KX132_1211_INS2_WMI > 0:
                if aa & b.KX132_1211_INS2_BFI > 0:
                    # print sensor.read_register(r.KX132_1211_INS2)[0] & b.KX132_1211_INS2_WMI, "WMI1"
                    #print (sensor.read_register(r.KX132_1211_INS2)[0] & b.KX132_1211_INS2_BFI, "BFI1")

                    bytes_in_buffer = sensor.get_fifo_level()                       # buffer level
                    # print bytes_in_buffer, aa, "#"
                    for i in range(bytes_in_buffer):
                        buf_storage.append(sensor.read_register(r.KX132_1211_BUF_READ, 6))  # fetch data from buffer and print status
                        # print i, "e",sensor.get_fifo_level(),"g",
                        # sensor.read_register(r.KX132_1211_INS2)[0]& b.KX132_1211_INS2_WMI,
                        # "WMI2"

                    print('samples got %d / %d' % (bytes_in_buffer / 6, len(buf_storage) / 6))

                    # print "a",sensor.get_fifo_level(),"g", sensor.read_register(r.KX132_1211_INS2)[0]& b.KX132_1211_INS2_BFI, "BFI2"
                    sensor.release_interrupts()
                    # sensor.clear_buffer()
                    print("b", sensor.get_fifo_level(), "g", sensor.read_register(r.KX132_1211_INS2)[0] & b.KX132_1211_INS2_BFI, "BFI2")

                    # for y in range(0, bytes_in_buffer/6):
                    #    print y, buf_storage[y]

    except KeyboardInterrupt:
        dl.stop()


def app_main():
    global sensor
    args = get_datalogger_config()

    sensor = KX132Driver()

    connection_manager = ConnectionManager()
    connection_manager.add_sensor(sensor)

    sensor.register_dump()
    enable_test_fifo(sensor)
    read_with_polling(sensor, args.loop)

    sensor.clear_buffer()
    sensor.disable_fifo()

    LOGGER.info('bye')

    sensor.set_power_off()


if __name__ == '__main__':
    app_main()
