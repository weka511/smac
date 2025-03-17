#!/usr/bin/env python

#   Copyright (C) 2024-2025 Simon Crase

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''Exercise 5.7. Compute Partition functions'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from re import split
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-i', '--input', default = basename(splitext(__file__)[0]),help='Name of parameters file')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


def get_file_name(args,default_ext='.csv'):
    base,ext = splitext(args.input)
    if len(ext)==0:
        ext = default_ext
    return f'{base}{ext}'

def read_coefficients(args):
    with open(get_file_name(args)) as parameter_file:
        for line in parameter_file:
            params = line.strip()
    return np.array([float(x) for x in split(r',\s*',params)])

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    C = read_coefficients(args)
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
