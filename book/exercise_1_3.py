#!/usr/bin/env python

#   Copyright (C) 2025 Simon Crase

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

''' Template for Python programs'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.optimize import linprog

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


def get_file_name(name,default_ext='png',seq=None):
    '''
    Used to create file names

    Parameters:
        name          Basis for file name
        default_ext   Extension if non specified
        seq           Used if there are multiple files
    '''
    base,ext = splitext(name)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    qualified_name = f'{base}.{ext}'
    if ext == 'png':
        return join(args.figs,qualified_name)
    else:
        return qualified_name

if __name__=='__main__':
    c =- np.ones((24))
    # c[1] = 1
    A = np.zeros((18,24))
    A[0,0] = 1
    A[0,1] = 1
    A[1,2] = 1
    A[1,3] = 1
    A[1,4] = 1
    A[2,5] = 1
    A[2,6] = 1
    A[3,7] = 1
    A[3,8] = 1
    A[3,9] = 1
    A[4,10] = 1
    A[4,11] = 1
    A[4,12] = 1
    A[4,13] = 1
    A[5,14] = 1
    A[5,15] = 1
    A[5,16] = 1
    A[6,17] = 1
    A[6,18] = 1
    A[7,19] = 1
    A[7,20] = 1
    A[7,21] = 1
    A[8,22] = 1
    A[8,23] = 1

    A[9,9] = 1
    A[9,2] = 1
    A[10,1] = 1
    A[10,13] = 1
    A[10,5] = 1
    A[11,4] = 1
    A[11,16] = 1
    A[12,17] = 1
    A[12,10] = 1
    A[12,0] = 1
    A[13,8] = 1
    A[13,20] = 1
    A[13,15] = 1
    A[13,3] = 1
    A[14,23] = 1
    A[14,12] = 1
    A[14,6] = 1
    A[15,7] = 1
    A[15,19] = 1
    A[16,18] = 1
    A[16,11] = 1
    A[16,22] = 1
    A[17,21] = 1
    A[17,14] = 1
    b = np.ones((18))
    res = linprog(c, A_eq=A, b_eq=b, bounds=(0.1,1),method='revised simplex',options={'rr':False})
    print (res)
    print (res.x)
    T = np.zeros((9,9))

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
