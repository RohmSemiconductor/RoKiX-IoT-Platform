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
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt

COLUMN_SEPARATOR = ';'
ROW_COMMENT = '#'

def get_header(fname):
    #
    # parse meta data from headers
    #
    header = None

    with open(fname) as infile:
        for line in infile:
            if not line.startswith(ROW_COMMENT):
                break
            if line.startswith('# timestamp'):
                header = [t.strip() for t in line.split(COLUMN_SEPARATOR)]
    return header

def get_duration(fname):
    timestamp = 0
    with open(fname) as infile:
        for line in infile:
            if not line.startswith(ROW_COMMENT):
                timestamp = float(line.split(COLUMN_SEPARATOR)[0])

    return timestamp

def loader(fname, dimensions=None, timestamps=False):
    header_offset = 2 # time, stamp, ...
    header = get_header(fname)[header_offset:]

    #
    # load the data to pd dataframe
    #

    # initial arguments for load()
    args = {
        'filepath_or_buffer':fname,
        'comment':ROW_COMMENT,
        'delimiter':';'
    }

    # populate column indexes and names
    columns = []
    if dimensions:
        dimensions = dimensions
    else:
        dimensions = header

    for t in dimensions:
        try:
            columns.append(header.index(t)+header_offset)
        except ValueError:
            print ('Error. Dimension "%s" does not exist in the log file "%s"' % (t, fname))
            print ('Existing dimensions are %s' % header)
            return

    args['usecols'] = columns
    args['names'] = dimensions

    if timestamps:
        # add timestamp channel
        args['usecols'] = [0] + args['usecols']
        args['names'] = ['time'] + args['names']

    # read data to dataframe
    data = pd.read_csv(**args)
    return data

def plotter(fname, dimensions=None, timestamps=False):

    data = loader(fname, dimensions, timestamps)
    dimensions = data.axes[1]

    # by default no data for x axis
    x = None

    if timestamps:
        x = 'time' # timestamp column is x axis
        dimensions = dimensions[1:]

    #
    # view the data
    #

    data.plot(x, dimensions, title=fname)
    plt.grid()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='RoKiX log visualizer. Example: %(prog)s log.csv -d ax ay az')
    parser.add_argument('-d', '--dimensions', nargs='*', type=str, help='Dimensions to plot.')
    parser.add_argument('-t', '--timestamps', action='store_true', help='1st column is timestamps')
    parser.add_argument('-l', '--list_dimensions', action='store_true', help='Lists channels and dimensions.')
    parser.add_argument('-g', '--log_length', action='store_true', help='Show last timestamp from the log.')
    parser.add_argument('fname', type=str, help='log file name')
    args = parser.parse_args()

    if args.list_dimensions:
        print (get_header(args.fname))

    elif args.log_length:
        print ('Last Time stamp is %f' % get_duration(args.fname))

    else:
        plotter(args.fname, args.dimensions, args.timestamps)

if __name__ == '__main__':
    main()
