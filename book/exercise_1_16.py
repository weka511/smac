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
    Exercise 1.16. Compare sampling efficiencies of Algoritms 1.13 (reject-finite)
    and 1.14 (tower-sampling).
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def reject_finite(pi,rng = np.random.default_rng(None)):
    '''Algorithm 1.13 Sample a finite distribution with a rejection algorithm'''
    pi_max = pi.max()
    K = len(pi)
    while True:
        k = rng.integers(K)
        if rng.uniform(0,pi_max) < pi[k]: yield k


def tower_sample(pi,rng = np.random.default_rng(None)):
    '''Algorithm 1.14 Sample without rejection'''
    Pi = pi.cumsum()
    while True:
        upsilon = rng.uniform(0,Pi[-1])
        yield np.searchsorted(Pi,upsilon)

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-K','--K',type=int,default=10000)
    parser.add_argument('-N','--N',type=int,default=1000)
    parser.add_argument('-n','--n',type=int,default=100)
    parser.add_argument('--alpha',type=float,default=1.5)
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

    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    pi = np.fromfunction(np.vectorize(lambda k:(k+1)**(-args.alpha)),(args.K,))
    pi /= pi.sum()

    start  = time()
    samples1 = np.zeros((args.N),dtype=int)
    rf = reject_finite(pi,rng=rng)
    for i in range(args.N):
        samples1[i] = next(rf)
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    et1 = f'Sampling with Rejection: Elapsed Time {minutes} m {seconds:.2f} s'
    print (et1)

    start = time()
    samples2 = np.zeros((args.N),dtype=int)
    ts = tower_sample(pi,rng=rng)
    for i in range(args.N):
        samples2[i] = next(ts)
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    et2 = f'Sampling without Rejection: Elapsed Time {minutes} m {seconds:.2f} s'
    print (et2)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,2,1)
    ax1.hist(samples1,bins=args.n,color='blue')
    ax1.set_title(et1)

    ax2 = fig.add_subplot(1,2,2)
    ax2.hist(samples2,bins=args.n,color='red')
    ax2.set_title(et2)

    fig.savefig(get_file_name(args.out))


    if args.show:
        show()
