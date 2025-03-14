#!/usr/bin/env python

# Copyright (C) 2018-20225Greenweaves Software Limited

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

from enumerate_ising import enumerate_ising
from argparse import ArgumentParser

parser = ArgumentParser(description='Compute statistics for Ising model')
parser.add_argument('-o', '--output', default = 'ising.csv', help = 'File to record results')
parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
parser.add_argument('--trace', default=False, action='store_true', help='Display output on console also')
args = parser.parse_args()

energy,magnetization = enumerate_ising((args.m, args.n))
with open(args.output,'w') as f:
    f.write('E,M,N\n')
    for EM,N in magnetization:
        E,M = EM
        if args.trace:
            print (f'{E},{M},{N}')
        f.write(f'{E},{M},{N}\n')
