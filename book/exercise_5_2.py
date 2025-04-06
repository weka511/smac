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

''' Exercise 5.2 Generare list of configurations'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np



def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--periodic', default=False, action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('-f', '--frequency',type = int, default = 100, help = 'How often to report progress')
    return parser.parse_args()


def generate_spins(N):
    Spins = np.zeros((N))
    for i in range(2**N):
        j = i
        k = 0
        while j > 0:
            k -= 1
            j,Spins[k] = divmod(j,2)
        yield Spins

if __name__=='__main__':
    start  = time()
    args = parse_arguments()

    N = args.m*args.n
    print (2**N)
    for i,s in enumerate(generate_spins(N)):
        if i%args.frequency == 0:
            print (f'{i/(2**N)} {time() - start:2}')

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')
