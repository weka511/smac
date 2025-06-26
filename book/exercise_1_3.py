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
from bidict import bidict

mapping = bidict({(0,  (3,0)),
                  (1,  (1,0)),
                  (2,  (0,1)),
                  (3,  (4,1)),
                  (4,  (2,1)),
                  (5,  (1,2)),
                  (6,  (5,2)),
                  (7,  (6,3)),
                  (8,  (4,3)),
                  (9,  (0,3)),
                  (10, (3,4)),
                  (11, (7,4)),
                  (12, (5,4)),
                  (13, (1,4)),
                  (14, (8,5)),
                  (15, (4,5)),
                  (16, (2,5)),
                  (17, (3,6)),
                  (18, (7,6)),
                  (19, (6,7)),
                  (20, (4,7)),
                  (21, (8,7)),
                  (22, (7,8)),
                  (23, (5,8))
              })

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N', '--N', type=int,default=100000)
    return parser.parse_args()

def transform_all(rules = [ [(3,0), (1,0)],
                            [(0,1),(4,1),(2,1)],
                            [(1,2), (5,2)],
                            [(6,3),(4,3),(0,3)],
                            [(3,4),(7,4),(5,4),(1,4)],
                            [(8,5),(4,5),(2,5)],
                            [(3,6), (7,6)],
                            [(6,7), (4,7),(8,7)],
                            [(7,8), (5,8)] ]):
    return [transform(boundaries) for boundaries in rules]

def transform(boundaries = [(3,0), (1,0)]):
    plus = []
    minus = []
    for a,b in boundaries:
        plus.append(mapping.inverse[(a,b)])
        minus.append(mapping.inverse[(b,a)])
    return plus,minus

def global_balance():

    c = np.ones((24))
    c[1] = 1
    A_ub = -np.ones((1,24))
    b_ub = -9*np.ones(1)
    A_eq = np.zeros((9,24))
    for i,(plus,minus) in enumerate(transform_all()):
        print (i,plus,minus)
        for j in plus:
            A_eq[i,j] = +1
        for j in minus:
            A_eq[i,j] = -1

    # A_eq[0,0] = 1
    # A_eq[0,1] = 1
    # A_eq[0,9] = -1
    # A_eq[0,2] = -1

    # A_eq[1,2] = 1
    # A_eq[1,3] = 1
    # A_eq[1,4] = 1
    # A_eq[1,1] = -1
    # A_eq[1,13] = -1
    # A_eq[1,5] = -1

    # A_eq[2,5] = 1
    # A_eq[2,6] = 1
    # A_eq[2,4] = -1
    # A_eq[2,16] = -1

    # A_eq[3,7] = 1
    # A_eq[3,8] = 1
    # A_eq[3,9] = 1
    # A_eq[3,17] = -1
    # A_eq[3,10] = -1
    # A_eq[3,0] = -1

    # A_eq[4,10] = 1
    # A_eq[4,11] = 1
    # A_eq[4,12] = 1
    # A_eq[4,13] = 1
    # A_eq[4,8] = -1
    # A_eq[4,20] = -1
    # A_eq[4,15] = -1
    # A_eq[4,3] = -1

    # A_eq[5,14] = 1
    # A_eq[5,15] = 1
    # A_eq[5,16] = 1
    # A_eq[5,23] = -1
    # A_eq[5,12] = -1
    # A_eq[5,6] = -1

    # A_eq[6,17] = 1
    # A_eq[6,18] = 1
    # A_eq[6,7] = -1
    # A_eq[6,19] = -1

    # A_eq[7,19] = 1
    # A_eq[7,20] = 1
    # A_eq[7,21] = 1
    # A_eq[7,18] = -1
    # A_eq[7,11] = -1
    # A_eq[7,22] = -1

    # A_eq[8,22] = 1
    # A_eq[8,23] = 1
    # A_eq[8,21] = -1
    # A_eq[8,14] = -1

    b_eq = np.zeros((9))
    return linprog(c, A_eq=A_eq, A_ub=A_ub, b_eq=b_eq, b_ub=b_ub,bounds=(0,1),method='simplex'),A_eq


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

    k = rng.integers(len(T))
    Counts = np.zeros(len(T))
    for i in range (args.N):
        k = T[k][rng.integers(len(T[k]))]
        Counts[k] += 1
    return Counts/Counts.sum()


if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    result,A_eq = global_balance()
    print (result.message)
    if result.success:
        print (result.x)
        print (np.dot(A_eq,result.x))
    Counts = markov(rng=rng)
    print (Counts)
    print (max(Counts)/min(Counts))
    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
