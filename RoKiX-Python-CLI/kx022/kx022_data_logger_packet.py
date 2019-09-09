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
"""
KX022 data logger application, with packet counter and fw time stamp
"""
# pylint: disable=duplicate-code
import imports  # pylint: disable=unused-import
from kx_lib import kx_logger
from kx_lib.kx_data_stream import StreamConfig
from kx_lib.kx_util import get_drdy_pin_index, evkit_config, convert_to_enumkey
from kx_lib.kx_configuration_enum import CH_ACC, POLARITY_DICT, CFG_POLARITY, CFG_SAD
from kx_lib.kx_data_logger import DataloggerBase
from kx022.kx022_driver import KX022Driver, r, b, m, e, r122, b122, m122, e122

from kx_lib.kx_data_stream import RequestMessageDefinition
from kx_lib.kx_configuration_enum import CFG_TARGET, CFG_PULLUP, BUS1_SPI, CFG_SPI_PROTOCOL, CFG_CS, ADAPTER_GPIO1_INT, ADAPTER_GPIO2_INT, REG_POLL

LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.DEBUG)

_CODE_FORMAT_VERSION = 3.0


class KX022DataStream(StreamConfig):
    fmt = "<Bhhh"
    hdr = 'ch!ax!ay!az'
    reg = r.KX022_XOUT_L

    def __init__(self, sensors, pin_index=None, timer=None):
        "Drdy data stream"
        assert not timer, 'timer not supported'
        sensor = sensors[0]
        StreamConfig.__init__(self, sensor)

        if pin_index is None:
            pin_index = get_drdy_pin_index()

        protocol = self.adapter.protocol
        message = RequestMessageDefinition(
            sensor=sensor,
            fmt=self.fmt,
            hdr=self.hdr,
            reg=self.reg,
            pin_index=pin_index)

        # Create macro handler for interrupt
        req = protocol.create_macro_req(
            trigger_type=protocol.EVKIT_MACRO_TYPE_INTR,
            gpio_pin=message.gpio_pin,
            gpio_sense=self.sense_dict[sensor.resource[CFG_POLARITY]],
            gpio_pullup=self.pullup_dict[sensor.resource[CFG_PULLUP]]
        )
        self.adapter.send_message(req)
        _, macro_id = self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_CREATE_MACRO_RESP)  # message_type, macro_id
        self.macro_id_list.append(macro_id)
        self.msg_ind_dict[macro_id] = message
        message.msg_req.append(req)
        LOGGER.debug('Macro created with id %d', macro_id)

        # read KX122 SPI
        # assert sensor.selected_connectivity == BUS1_SPI
        # assert sensor.resource[CFG_SPI_PROTOCOL] in [0, 1]

        # if sensor.resource[CFG_SPI_PROTOCOL] == 1:
        #     # With Kionix components, MSB must be set 1 to indicate reading
        #     message.reg = message.reg | 1 << 7

        # req = protocol.add_macro_action_req(
        #     macro_id,
        #     action=protocol.EVKIT_MACRO_ACTION_READ,
        #     target=sensor.resource[CFG_TARGET],
        #     identifier=sensor.resource[CFG_CS],
        #     append=True,
        #     start_register=message.reg,
        #     bytes_to_read=message.msg_size - 1)

        # LOGGER.debug(req)
        # self.adapter.send_message(req)
        # message.msg_req.append(req)
        # self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)

        # create macro action for reading KX122 over I2C
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_READ,
            target=sensor.resource[CFG_TARGET],
            identifier=sensor.resource[CFG_SAD],
            append=True,
            start_register=message.reg,
            bytes_to_read=message.msg_size - 1)

        self.adapter.send_message(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        message.msg_req.append(req)
        LOGGER.debug(req)

        # creat another macro action for packet counter
        req = protocol.add_macro_action_req(
            macro_id,
            action=protocol.EVKIT_MACRO_ACTION_PKT_COUNT,
            target=protocol.EVKIT_BUS1_TARGET_FW,
            identifier=protocol.EVKIT_BITWIDTH_8,
            append=True)

        self.adapter.send_message(req)
        message.msg_req.append(req)
        self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        LOGGER.debug(req)

        # packet counter respose will increase the message size.
        # update message size and other properties so response of both macro actions can be interpreted
        message.msg_size = 8
        message.msg_fmt = "<BhhhB"
        message.msg_hdr = 'ch!ax!ay!az!ind'

        # # FW time stamp
        # req = protocol.add_macro_action_req(
        #     macro_id,
        #     action=protocol.EVKIT_MACRO_ACTION_TIMESTAMP,
        #     target=protocol.EVKIT_BUS1_TARGET_FW,
        #     identifier=protocol.EVKIT_TIME_SCALE_NATIVE)

        # LOGGER.debug(req)
        # self.adapter.send_message(req)
        # message.msg_req.append(req)
        # self.adapter.receive_message(wait_for_message=protocol.EVKIT_MSG_ADD_MACRO_ACTION_RESP)
        # message.msg_size = 12
        # message.msg_fmt = "<BhhhBL"
        # message.msg_hdr='ch!ax!ay!az!ind'


def enable_data_logging(sensor,
                        odr=25,
                        max_range='2G',
                        lp_mode=False,
                        low_pass_filter='ODR_9',
                        power_off_on=True,          # set to False if this function is part of other configuration
                        int_number=None):
    LOGGER.info('enable_data_logging start')

    #
    # parameter validation
    #

    if sensor.name == 'KX122':
        valid_odrs = e122.KX122_ODCNTL_OSA.keys()
    else:
        valid_odrs = e.KX022_ODCNTL_OSA.keys()

    assert convert_to_enumkey(odr) in valid_odrs, 'Invalid odr value "{}". Valid values are {}'.format(
        odr, valid_odrs)

    assert max_range in e.KX022_CNTL1_GSEL.keys(), 'Invalid max_range value "{}". Valid values are {}'.format(
        max_range, e.KX022_CNTL1_GSEL.keys())

    assert (lp_mode in list(e.KX022_LP_CNTL_AVC.keys()) +
            [False]), 'Invalid lp_mode value "{}". Valid values are: False or {}'.format(
                lp_mode, e.KX022_LP_CNTL_AVC.keys())

    assert low_pass_filter in list(e.KX022_ODCNTL_LPRO.keys()) + \
        ['BYPASS'], 'Invalid filter value "{}". Valid values are: BYPASS or {}'.format(
            filter, e.KX022_ODCNTL_LPRO.keys())

    # Set sensor to stand-by to enable setup change
    if power_off_on:
        sensor.set_power_off()

    #
    # Configure sensor
    #

    # odr setting for data logging
    if sensor.WHOAMI in sensor._WAIS122:
        sensor.set_odr(e122.KX122_ODCNTL_OSA[convert_to_enumkey(odr)])
    else:
        sensor.set_odr(e.KX022_ODCNTL_OSA[convert_to_enumkey(odr)])

    # select g-range
    sensor.set_range(e.KX022_CNTL1_GSEL[max_range])

    # resolution / power mode selection

    if lp_mode is not False:
        # enable low current mode
        sensor.reset_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)
        # define averaging value
        sensor.set_average(e.KX022_LP_CNTL_AVC[lp_mode])
    else:
        # full resolution
        sensor.set_bit(r.KX022_CNTL1, b.KX022_CNTL1_RES)

    # set bandwitdh
    if low_pass_filter != 'BYPASS':
        sensor.set_BW(low_pass_filter, 0, CH_ACC)
        sensor.enable_iir()
    else:
        sensor.disable_iir()
    #
    # interrupt pin routings and settings
    #

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
            sensor.reset_bit(r.KX022_INC1, b.KX022_INC1_IEL1)  # latched interrupt
            sensor.set_bit(r.KX022_INC1, b.KX022_INC1_IEN1)  # enable interrupt
        else:
            sensor.reset_bit(r.KX022_INC5, b.KX022_INC5_IEL2)  # latched interrupt
            sensor.set_bit(r.KX022_INC5, b.KX022_INC5_IEN2)  # enable interrupt

        polarity = POLARITY_DICT[sensor.resource[CFG_POLARITY]]
        LOGGER.debug('Configuring interrupt polarity {}'.format(
            sensor.resource[CFG_POLARITY]))
        sensor.set_interrupt_polarity(intpin=_intpin, polarity=polarity)

        # use acc data ready
        sensor.enable_drdy(intpin=_intpin)

    #
    # Turn on operating mode (disables setup)
    #

    if power_off_on:
        sensor.set_power_on()

    # sensor.register_dump()#;sys.exit()

    LOGGER.info('enable_data_logging done')


class KX022PacketDataLogger(DataloggerBase):
    def __init__(self):
        DataloggerBase.__init__(self)
        self.sensor = KX022Driver()
        self.connection_manager.add_sensor(self.sensor)

    def enable_data_logging(self, **kwargs):
        enable_data_logging(self.sensor, **kwargs)


def main():
    l = KX022PacketDataLogger()
    l.enable_data_logging(odr=evkit_config.odr)
    l.run(KX022DataStream)


if __name__ == '__main__':
    main()
