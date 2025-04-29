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

'''
   Exercise 1.9
   (a) Sample permutations using algoritm 1.11 and check that this algorithm generates all 120
   permutations of 5 elements equally often.
   (b) Determine the cycle representation of each permutation that is generated.
'''

from argparse import ArgumentParser
from collections import defaultdict
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.stats import chisquare

def ran_perm(K,rng=np.random.default_rng()):
    '''
    Sample permutations using algoritm 1.11
    '''
    P = np.array(range(K))
    for k in range(K):
        l = rng.integers(k,K)
        P[k],P[l] = P[l],P[k]
    return P

def get_frequencies(N,K=5,rng=np.random.default_rng()):
    '''
    Find frequencies of each permutation and each cyele
    '''
    Freqs = defaultdict(lambda:0)
    Cycles = np.zeros((K+1))
    for _ in range(N):
        P = ran_perm(K,rng=rng)
        Product = factorize(P)
        for cycle in Product:
            Cycles[len(cycle)] += 1
        Freqs[str(P)] += 1
    return Freqs, Cycles

def factorize(P):
    '''Factorize a permutation into a product of non-trivial cycles'''
    closed = []
    Product = []
    for i in range(len(P)):
        if i in closed: continue
        closed.append(i)
        cycle = [i]
        j = i
        while P[j] not in cycle:
            cycle.append(P[j])
            j = P[j]
            closed.append(j)
        if len(cycle) > 1:
            Product.append(cycle)

    return Product

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-N','--N',type=int,default=1024)
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
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
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    Freqs,Cycles = get_frequencies(args.N,rng=rng)
    chi2 = chisquare([v for v in Freqs.values()])
    n = len(Freqs.keys())

    fig = figure(figsize=(12,12))
    fig.suptitle(f'Number of permutations={args.N:,}')
    ax1 = fig.add_subplot(2,2,1)
    ax1.bar(range(n),Freqs.values(),color='r')
    ax1.set_title(fr'n={n}, $\chi^2=${chi2.statistic:.2f}, pvalue={chi2.pvalue:.4f}')

    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(Freqs.values(),color='g')
    ax2.set_title('Histogram of frequencies')

    ax3 = fig.add_subplot(2,2,3)
    ax3.bar(range(0,len(Cycles)),Cycles,color='b')
    ax3.set_title('Cycles')
    ax3.set_xlabel('Length')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
