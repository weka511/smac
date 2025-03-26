#!/usr/bin/env python

# Copyright (C) 2018-2025 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''Algorithm 5.3: Single spin-slip enumeration for Ising model'''


from argparse import ArgumentParser
from os.path import  splitext
from enumerate_ising import enumerate_ising

def parse_args():
    parser = ArgumentParser(description='Compute statistics for Ising model')
    parser.add_argument('-o', '--output', default = 'ising.csv', help = 'File to record results')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--trace', default=False, action='store_true', help='Display output on console also')
    parser.add_argument('--bounded', default=False, action='store_true', help='Use this for bounded (not periodic) boundary conditions')
    parser.add_argument('--frequency', type = int, default = 100000, help = 'For reporting')
    return parser.parse_args()

def get_file_name(arg,default_ext = '.csv'):
    base,ext = splitext(arg)
    if len(ext)==0:
        ext = default_ext
    return f'{base}{ext}'

if __name__ == '__main__':
    args = parse_args()

    energy,magnetization = enumerate_ising((args.m, args.n),periodic = not args.bounded,frequency=args.frequency)

    with open(get_file_name(args.output),'w') as output_file:
        output_file.write('E,M,N\n')
        for EM,N in magnetization:
            E,M = EM
            if args.trace:
                print (f'{E},{M},{N}')
            output_file.write(f'{E},{M},{N}\n')
