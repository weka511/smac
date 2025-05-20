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

'''Exercise 1.20. Implemement algorithm 1.28 (data-bunch).'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import maxsize
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def markov_discrete_pebble(start=0,
                           N=maxsize,
                           neighbour_table=np.array([[ 1,  3, -1, -1],
                                                     [ 2,  4,  0, -1],
                                                     [-1,  5,  1, -1],
                                                     [ 4,  6, -1,  0],
                                                     [ 5,  7,  3,  1],
                                                     [-1,  8,  4,  2],
                                                     [ 7, -1, -1,  3],
                                                     [ 8, -1,  6,  4],
                                                     [-1, -1,  7,  5]]),
                           rng=np.random.default_rng()):
    _,n = neighbour_table.shape
    state = start
    for i in range(N):
        j = rng.integers(0,n)
        if neighbour_table[state,j] != -1:
            state = neighbour_table[state,j]
        yield i,state

def data_bunch(X):
    '''
    Algorithm 1.23 Computing the apparent error for an even number of data points,
    by bunching them into pairs.
    '''
    assert len(X) % 2 == 0
    X_bunched = X.reshape(-1,2).mean(axis=1)
    return X_bunched.mean(), X_bunched.std(), X_bunched

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--N',type=int,default=10)
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
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    Counts = np.zeros((9,2**args.N))
    for i,k in markov_discrete_pebble(N=2**args.N,rng=rng):
        Counts[k,i] += 1

    Frequency = np.divide(np.cumsum(Counts,axis=1),list(range(1,2**args.N+1)))

    X = Counts[0,:]
    error = np.zeros((args.N))
    for i in range(args.N):
        _,error[i],X = data_bunch(X)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    ax1.plot(abs(Frequency[:,-1] - 1/9))
    ax2.plot(error)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
