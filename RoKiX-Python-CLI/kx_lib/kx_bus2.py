# 
# Copyright 2018 Kionix Inc.
#
import os
import subprocess
import signal
import time
import serial
import serial.tools.list_ports as list_ports
from kx_lib.kx_exception import ProtocolException, ProtocolTimeoutException, EvaluationKitException

from kx_lib import kx_logger
LOGGER = kx_logger.get_logger(__name__)
# LOGGER.setLevel(kx_logger.ERROR)
# LOGGER.setLevel(kx_logger.INFO)
# LOGGER.setLevel(kx_logger.DEBUG)


class KxConnection(object):
    "Base class of all kionix communication protocol (bus2)"
    bus2_configuration = None # bus configuration blob
    def flush(self):
        """Discard any data from input buffers."""
        raise NotImplementedError()

    def read(self, length):
        """Read data.

        Args:
            length (int): Amount of bytes to read.

        Raises:
            ProtocolTimeoutException: The read timed out.

        Returns:
            array.array: Read bytes.
        """
        raise NotImplementedError()

    def write(self, data):
        """Write data.

        Args:
            data (array.array): Array of bytes to send.
        """
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class KxPySerial(KxConnection):
    "Base class of all protocol communication through pyserial"

    def __init__(self, bus2_configuration=None):
        "bus2_configuration json blob from board configuration json file"
        if bus2_configuration is None:
            return  # for debugging

        self._conn = None  # pyserial connection instance
        self.bus2_configuration = bus2_configuration

    def read(self, length=1):
        """Read data from the pyserial connection."""
        data = self._conn.read(length)
        if not data:
            raise ProtocolTimeoutException('No data received.')

        return data

    def flush(self):
        """Flush data from the pyserial connection."""
        # Flush incoming data
        if self._conn.in_waiting:
            self._conn.reset_input_buffer()

    def write(self, data):
        """Write data to the pyserial connection."""
        LOGGER.debug(data)
        self._conn.write(data)

    def close(self):
        """Close the pyserial connection."""
        self._conn.close()


class KxSocket(KxConnection):
    pass


class KxWinBLE(KxPySerial):
    def __init__(self, bus2_configuration=None):
        KxPySerial.__init__(self, bus2_configuration)
        self._p = None  # B2S subprocess instance

    def _start_child_process(self, port, mac_address):
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx
        # CREATE_NEW_PROCESS_GROUP=0x00000200 -> If this flag is specified, CTRL+C signals will be disabled
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        thispath, thisfile = os.path.split(__file__)
        del thisfile
        B2S_path1 = os.path.join(thispath, 'B2S.exe')
        B2S_path2 = 'B2S.exe'
        B2S_path = ""

        if os.path.isfile(B2S_path1):
            B2S_path = B2S_path1
        elif os.path.isfile(B2S_path2):
            B2S_path = B2S_path2
        else:
            raise ProtocolException('B2S.exe not found.')

        if mac_address != "":
            self._p = subprocess.Popen(
                B2S_path + ' -p %s -m %s' % (port,
                                             mac_address),
                startupinfo=startupinfo,
                creationflags=0x00000200,
                universal_newlines=True,
                stdout=subprocess.PIPE)  # pipe stdout to see only errors in console
        else:
            self._p = subprocess.Popen(
                B2S_path + ' -p %s' % port,
                startupinfo=startupinfo,
                creationflags=0x00000200,
                universal_newlines=True,
                stdout=subprocess.PIPE)  # pipe stdout to see only errors in console

        if self._p is not None:
            # check that b2s has established socket connection
            while True:
                line = self._p.stdout.readline()
                if line != '':
                    if line.rstrip().startswith('Waiting for a connection'):
                        break
                else:
                    time.sleep(1)
                    break

    def _stop_child_process(self):
        # NOTE: Must use CTLR + BREAK event instead of CTRL + C, which has been disabled
        os.kill(self._p.pid, signal.CTRL_BREAK_EVENT)

    def initialize(self, socket_port=8100, mac_address='', timeout=2):
        """Initialize the B2S connection. (Windows BLE to socket streamer)

        Args:
            socket_port (int): Socket port number (e.g. 8100).
            mac_address      : Mac address of BLE device (if empty, the first found device is connected)
            timeout (float, optional): Read timeout in seconds.
        """
        self._start_child_process(socket_port, mac_address)
        self._conn = serial.serial_for_url('socket://localhost:%d' % socket_port)

    def close(self):
        """Close the socket connection."""
        self._stop_child_process()
        super(KxWinBLE, self).close()  # call parent class close()


class KxLinuxBLE(KxConnection):
    pass


class KxLinuxI2C(KxConnection):
    pass


class KxComPort(KxPySerial):
    """Serial port connection.

    Attributes:
        bus2_configuration (?): ?
        baudrate (int): Baud rate.
    """

    def __init__(self, bus2_configuration=None):
        KxPySerial.__init__(self, bus2_configuration)
        self.baudrate = self.bus2_configuration['baud_rate']

    def initialize(self, comport, timeout=2):
        """Initialize the serial connection.

        Args:
            comport (str): Name of the serial device (e.g. 'COM9', '/dev/ttyACM0').
            timeout (float, optional): Read timeout in seconds.
        """
        self._conn = serial.Serial(
            port=comport,
            baudrate=self.bus2_configuration['baud_rate'],
            timeout=timeout,
            rtscts=self.bus2_configuration['rtscts'],
            xonxoff=self.bus2_configuration['xonxoff'])

        delay = self.bus2_configuration['start_up_delay_ms']
        if delay > 0:
            LOGGER.info('Waiting start up delay {}(ms).'.format(delay))
            time.sleep(delay / 1000.0)
            LOGGER.info('Waiting start up delay done.')

        # DEFAULT VALUES IN PYSERIAL
        # port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE,
        # stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False,
        # write_timeout=None, dsrdtr=False, inter_byte_timeout=None,
        # exclusive=None

    def get_com_port(self):
        """Autodetect a connected serial device and return the device's name.

        Raises:
            EvaluationKitException: Autodetection found no devices.

        Returns:
            str: The name of the detected serial device (e.g. 'COM2').
        """
        # TODO 3 check also pid and vid 
        matching_ports = []
        LOGGER.debug('Listing serial ports.')
        for port in list_ports.comports():
            LOGGER.debug(port.name)
            LOGGER.debug(port.description)
            LOGGER.debug(port.vid)
            LOGGER.debug(port.pid)

            # matcing port found based in vid and pid?
            if self.bus2_configuration['vid'] == port.vid and self.bus2_configuration['pid'] == port.pid:
                matching_ports.append(port.device)
                continue 

        if not matching_ports:
            raise EvaluationKitException('Automatic search found no devices')

        return matching_ports
