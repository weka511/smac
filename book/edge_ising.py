#!/usr/bin/env python

#   Copyright (C) 2024 Simon Crase

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

'''
    Algorithm 5.5 edge-ising.
    Gray code enumeration of the loop configurations in Figure 5.8
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from gray import gray_flip, generate_edges

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()

def get_file_name(figs):
    return join(figs,basename(splitext(__file__)[0]))

def edge_ising(shape=(4,4)):
    '''
    Algorithm 5.5 edge-ising. Gray code enumeration of the loop configurations in Figure 5.8

    Parameters:
        n   Number of edges
        m    Number of sites
    '''
    def create_edges():
        S1 = []
        S2 = []
        for s1,s2 in generate_edges(shape):
            S1.append(s1)
            S2.append(s2)
        return S1,S2

    M,N = shape
    n_sites = M*N
    S1,S2 = create_edges()
    n_edges = len(S1)
    n = np.zeros((n_edges),dtype=np.int64)
    o = np.zeros((n_sites),dtype=np.int64)
    yield n
    for i, (k,_) in enumerate(gray_flip(2**n_edges)):
        if i > 2**n_edges -2: return
        k -= 1              # k starts at 1 (following The Book), convert to 0-based
                            # so we can use as an array index
        n[k] = (n[k] + 1) % 2
        o[S1[k]] += 2*n[k]  - 1
        o[S2[k]] += 2*n[k]  - 1
        if np.all(o%2 ==0):
            yield i,n

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    for n in edge_ising(shape=(4,4)):
        print (n)
    # fig = figure(figsize=(12,12))

    # fig.savefig(get_file_name(args.figs))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
