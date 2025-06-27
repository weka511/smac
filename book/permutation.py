#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

from argparse import ArgumentParser
from collections import Counter
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.special import factorial

'''
    Algorithm 1.11: generate random permutations, and
    Algorithm 1.12: generate random combinations
'''

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-M','--M', type=int,default=10)
    parser.add_argument('-N','--N', type=int,default=1000)
    parser.add_argument('-K','--K', type=int,default=5)
    return parser.parse_args()

def ran_perm(K,rng = np.random.default_rng()):
    '''
        Algorithm 1.11: generate random permutations
    '''
    perm = list(range(K))
    for k in range(K):
        l = rng.integers(k,K)
        perm[k],perm[l] = perm[l],perm[k]
    return perm

def ran_combination(K,M,rng = np.random.default_rng()):
    '''
    Algorithm 1.12: generate random combinations
    '''
    perm = range(K)
    for k in range(M):
        l = rng.integera(k,K)
        perm[k],perm[l] = perm[l],perm[k]
    return perm[0:2]

def permutation2str(perm):
    '''
    Convert a permutation to a string representation, so
    we can use it as a key in a dictionary
    '''
    result = ''
    for el in perm:
        result += str(el)
    return result

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
    start = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    for _ in range(args.M):
        permutation_counts = Counter()

        for _ in range(factorial(args.K,exact=True)*args.N):
            permutation_counts[permutation2str(ran_perm(args.K,rng=rng))] += 1

        count= len(permutation_counts.keys())
        average = len(list(permutation_counts.elements()))/count

        chi_squared = 0
        for kk in permutation_counts.keys():
            chi_squared += ((permutation_counts[kk]-average)*(permutation_counts[kk]-average))

        ss = np.sqrt(2*chi_squared)
        print (count, average, chi_squared, ss, np.sqrt(2*count-1))

    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()

