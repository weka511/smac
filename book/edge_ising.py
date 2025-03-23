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
from ising import gray_flip, generate_edges

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('-m',default=4,type=int, help='Number of rows')
    parser.add_argument('-n',default=4,type=int, help='Number of columns')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    return parser.parse_args()

def get_file_name(arg,default_ext = '.csv'):
    base,ext = splitext(arg)
    if len(ext)==0:
        ext = default_ext
    return f'{base}{ext}'

def edge_ising(shape=(4,4)):
    '''
    Algorithm 5.5 edge-ising. Gray code enumeration of the loop configurations in Figure 5.8

    Parameters:
        shape

    '''
    M,N = shape
    n_sites = M*N
    n_edges = (M-1)*N + M*(N-1)

    # Construct end points of all edges
    S1 = np.zeros((n_edges),dtype=int)
    S2 = np.zeros((n_edges),dtype=int)
    for i,(s1,s2) in enumerate(generate_edges(shape)):
        S1[i] = s1
        S2[i] = s2
    assert all(S1<S2)

    n = np.zeros((n_edges),dtype=np.int64) # Contribution from each edge {0,1}
    o = np.zeros((n_sites),dtype=np.int64) # Count number of times each site is present
    yield n

    for i, (k,_) in enumerate(gray_flip(2**n_edges)):
        if i > 2**n_edges - 2: return
        k -= 1              # k starts at 1 (following The Book), convert to array index
        n[k] = (n[k] + 1) % 2
        o[S1[k]] += 2*n[k]  - 1
        o[S2[k]] += 2*n[k]  - 1
        if np.all(o%2 ==0):
            yield n

def expand(A):
    '''
    Convert a list to a form suitable for printing, without the parentheses

    E.g. A = [1, 2, 3, 4] becomes '1, 2, 3, 4'
    '''
    return ', '.join([str(a) for a in A])

def strip_trailing_zeros(N):
    '''
    Eliminate trailing zeros from an array
    '''
    n = len(N)
    while N[n-1] == 0:
        n -= 1
    return N[:n]

if __name__=='__main__':
    start  = time()
    args = parse_arguments()

    with open(get_file_name(args.out),'w') as out:
        N = np.zeros((25),dtype=int)
        out.write(f'{args.m},{args.n}\n')
        for i,n in enumerate(edge_ising(shape=(args.m,args.n))):
            out.write(f'{expand(n)}\n')
            N[n.sum()] += 1

        out.write(f'{expand(strip_trailing_zeros(N))}\n')

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')
