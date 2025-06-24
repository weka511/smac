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

'''Exercise 1.3: find a rejection-free algorithm'''

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

def global_balance():
    c =- np.zeros((24))
    c[1] = 1
    A_ub = -np.ones((1,24))
    b_ub = -9*np.ones(1)
    A_eq = np.zeros((9,24))
    A_eq[0,0] = 1
    A_eq[0,1] = 1
    A_eq[0,9] = -1
    A_eq[0,2] = -1

    A_eq[1,2] = 1
    A_eq[1,3] = 1
    A_eq[1,4] = 1
    A_eq[1,1] = -1
    A_eq[1,13] = -1
    A_eq[1,5] = -1

    A_eq[2,5] = 1
    A_eq[2,6] = 1
    A_eq[2,4] = -1
    A_eq[2,16] = -1

    A_eq[3,7] = 1
    A_eq[3,8] = 1
    A_eq[3,9] = 1
    A_eq[3,17] = -1
    A_eq[3,10] = -1
    A_eq[3,0] = -1

    A_eq[4,10] = 1
    A_eq[4,11] = 1
    A_eq[4,12] = 1
    A_eq[4,13] = 1
    A_eq[4,8] = -1
    A_eq[4,20] = -1
    A_eq[4,15] = -1
    A_eq[4,3] = -1

    A_eq[5,14] = 1
    A_eq[5,15] = 1
    A_eq[5,16] = 1
    A_eq[5,23] = -1
    A_eq[5,12] = -1
    A_eq[5,6] = -1

    A_eq[6,17] = 1
    A_eq[6,18] = 1
    A_eq[6,7] = -1
    A_eq[6,19] = -1

    A_eq[7,19] = 1
    A_eq[7,20] = 1
    A_eq[7,21] = 1
    A_eq[7,18] = -1
    A_eq[7,11] = -1
    A_eq[7,22] = -1

    A_eq[8,22] = 1
    A_eq[8,23] = 1
    A_eq[8,21] = -1
    A_eq[8,14] = -1

    b_eq = np.zeros((9))
    res = linprog(c, A_eq=A_eq, A_ub=A_ub, b_eq=b_eq, b_ub=b_ub,bounds=(0,1),method='simplex')
    print (res)
    print (res.x)
    print (np.dot(A_eq,res.x))

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

def markov( T = [[3],
                 [4,2],
                 [1,5],
                 [6,4,0],
                 [3,7,5,1],
                 [8,4,2],
                 [3,7],
                 [6,4,8],
                 [7,5],
                 ],
            rng = np.random.default_rng()):

    k = rng.integers(9)
    Counts = np.zeros(9)
    for i in range (100000):
        k = T[k][rng.integers(len(T[k]))]
        Counts[k] += 1
    print (max(Counts)/min(Counts))

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    global_balance()
    markov(rng=rng)
    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
