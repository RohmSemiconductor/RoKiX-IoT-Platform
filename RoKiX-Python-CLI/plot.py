# 
# Copyright 2018 Kionix Inc.
#
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from logging import INFO, DEBUG, WARNING, ERROR  # pylint: disable=unused-import


def get_logger(name):
    logging.basicConfig(format='%(asctime)s %(levelname)s :\t%(filename)s (%(lineno)d) :\t%(funcName)s :\t%(message)s')
    logger = logging.getLogger(name)
    return logger


LOGGER = get_logger(__name__)

# try to import modules needed for FFT.
# If not installed then error is given only if FFT plot is requested
try:
    from scipy import fftpack
except ImportError:
    fftpack = None

COLUMN_SEPARATOR = ';'
ROW_COMMENT = '#'
kwargs = None


class PlotterException(Exception):
    pass


def get_header(fname):
    #
    # parse meta data from headers
    #
    global kwargs  # pylint: disable=global-statement
    header = None

    with open(fname) as infile:
        for line in infile:
            if not line.startswith(ROW_COMMENT):
                break
            if line.startswith('# timestamp'):
                header = [t.strip() for t in line.split(kwargs.column_separator)]
                return header

    LOGGER.error('No header found from log file. Defining channel names with --column_header keyword argument could fix the problem.')
    raise PlotterException('No header found from log file.')


def get_duration(fname):
    global kwargs
    timestamp = 0
    with open(fname) as infile:
        for line in infile:
            if not line.startswith(ROW_COMMENT):
                timestamp = float(line.split(kwargs.column_separator)[0])

    return timestamp


def loader(fname, dimensions=None, timestamps=False):
    global kwargs  # pylint: disable=global-statement
    if not kwargs.column_header:
        header = get_header(fname)
        header_offset = 2  # time, stamp, ...
        header = header[header_offset:]
    else:
        header = kwargs.column_header.split(kwargs.column_separator)
        header_offset = 0

    #
    # load the data to pd dataframe
    #

    # initial arguments for load()
    pdargs = {
        'filepath_or_buffer': fname,
        'comment': ROW_COMMENT,
        'delimiter': kwargs.column_separator
    }

    # populate column indexes and names
    columns = []
    if dimensions is None:
        dimensions = header

    for t in dimensions:
        try:
            columns.append(header.index(t) + header_offset)
        except ValueError:

            LOGGER.error('Dimension "%s" does not exist in the log file "%s"' % (t, fname))
            LOGGER.error('Existing dimensions are %s' % header)
            raise PlotterException()

    pdargs['usecols'] = columns
    pdargs['names'] = dimensions

    if timestamps:
        # add timestamp channel
        pdargs['usecols'] = [0] + pdargs['usecols']
        pdargs['names'] = ['time'] + pdargs['names']

    if isinstance(header, str):
        LOGGER.warning('Column separator character not found from header.')
        LOGGER.warning('Log has only one column or column separator is incorrectly defined. ')
        LOGGER.warning('Column separator can be defined with keyword argument --column_separator')
    # read data to dataframe
    try:
        data = pd.read_csv(**pdargs)

        test_value = data[pdargs['names'][-1]][0]
        if not (isinstance(test_value, np.int64)):
            LOGGER.error('Header or column separator may not be properly configured.')
            LOGGER.error('Header is defined as "%s".' % dimensions)
            LOGGER.error('Column separator as "%s".' % pdargs['delimiter'])
            LOGGER.error('Keyword argument --column_separator can be used to redefine it.')
            LOGGER.error('This value should contain single integer value: "%s"' % test_value)

            raise PlotterException()

    except pd.errors.ParserError:
        LOGGER.error('Log file may not use default column separator. Use keyword argument --column_separator to define it.')
        raise
    return data


def plotter(fname, dimensions=None, timestamps=False):

    data = loader(fname, dimensions, timestamps)
    dimensions = data.axes[1]

    # by default no data for x axis
    x = None

    if timestamps:
        x = 'time'  # timestamp column is x axis
        dimensions = dimensions[1:]

    #
    # view the data
    #

    data.plot(x, dimensions, title=fname, marker=kwargs.tick_marker)
    plt.grid()
    plt.show()


def fftplotter(fname, dimensions=None, timestamps=False):

    assert fftpack and np, 'scipy.fftpack and/or numpy modules must be installed.'

    data = loader(fname, dimensions, timestamps)
    dimensions = data.axes[1]

    if timestamps:
        dimensions = dimensions[1:]

    # calculate FFT
    fft_data = 10 * np.log10(np.abs(fftpack.fft(data, axis=0)**2))
    fft_freq = fftpack.fftfreq(len(fft_data), 1)
    positive_freq = fft_freq > 0

    #
    # view the data
    #
    plt.plot(fft_freq[positive_freq], fft_data[positive_freq])
    plt.xlabel('x/ODR')
    plt.ylabel('dB')
    plt.legend(dimensions)
    plt.title(fname)
    plt.grid()
    plt.show()


def main():
    # examples:

    # plot log file which does not have column headers and column separator is ,
    # >python plot.py  test_fft.csv -c ax,ay,az -s,

    # plot fft from log file which does not have column headers and column separator is ,
    # >python plot.py  test_fft.csv -c ax,ay,az -s, -f

    # plot fft from ax axis of log file which does not have column headers and column separator is ,
    # >python plot.py  test_fft.csv -c ax,ay,az -s, -f -d ax

    # plot x,y,z from tab separated log file having t,x,y,z channels
    # >python plot.py -s \t -c t\tx\ty\tz -d x y z  -- filename

    # same as above but timestamps to x axis
    # >python plot.py -t -s \t -c t\tx\ty\tz -d x y z -- filename

    global kwargs  # pylint: disable=global-statement
    parser = argparse.ArgumentParser(description='RoKiX log visualizer. Example: %(prog)s log.csv -d ax ay az')
    parser.add_argument('-d', '--dimensions', nargs='*', type=str, help='Dimensions to plot.')
    parser.add_argument('-t', '--timestamps', action='store_true', help='1st column is timestamps')
    parser.add_argument('-l', '--list_dimensions', action='store_true', help='Lists channels and dimensions.')
    parser.add_argument('-g', '--log_length', action='store_true', help='Show last timestamp from the log.')
    parser.add_argument('-s', '--column_separator', default=COLUMN_SEPARATOR, help='Clolumn separator (default ;)')
    parser.add_argument('-c', '--column_header', default=None, help='Column header definition in case log file does not have it.')
    parser.add_argument('-f', '--fft', action='store_true', help='FFT plot instead of time domain plot')
    parser.add_argument(
        '-m',
        '--tick_marker',
        default=None,
        help='Tick marker for data points (see https://matplotlib.org/3.1.0/api/markers_api.html#module-matplotlib.markers)')

    parser.add_argument('fname', type=str, help='log file name')
    kwargs = parser.parse_args()

    # special handling for tab separated values
    if kwargs.column_separator == '\\t':
        kwargs.column_separator = '\t'
        if kwargs.column_header:
            kwargs.column_header = kwargs.column_header.replace('\\t', '\t')

    if kwargs.list_dimensions:
        print(get_header(kwargs.fname))

    elif kwargs.log_length:
        print('Last Time stamp is %f' % get_duration(kwargs.fname))

    elif not kwargs.fft:
        plotter(kwargs.fname, kwargs.dimensions, kwargs.timestamps)
        return
    else:
        fftplotter(kwargs.fname, kwargs.dimensions, kwargs.timestamps)
        return
    assert 0


if __name__ == '__main__':
    main()
