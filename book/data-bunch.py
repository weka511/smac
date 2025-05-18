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

def data_bunch(x):
    '''
    Algorithm 1.23 Computing the apparent error for an even number of data points,
    and bunching them into pairs.
    '''
    N = len(x)
    assert N%2 == 0
    x1 = np.empty((N//2))

    for i in range(len(x1)):
        x1[i] = 0.5*(x[2*i] + x[2*i+1])

    return x1.mean(), x1.std(), x1

def perform_markov(n_trials=maxsize,delta=1,start=np.array([1.0,0.0]), rng = np.random.default_rng()):
    '''
    Algorithm 1.2 Markov chain Monte Carlo, modified to return result of each trial
    so it can be used with data_bunch.
    '''
    pos = start

    n_hits = 0
    n_reject = 0

    for i in range(1,n_trials+1):
        proposed = pos + rng.uniform(-delta, delta,2)
        if np.all(np.abs(proposed) < 1):
            pos = proposed
        else:
            n_reject += 1

        if pos.dot(pos) < 1:
            n_hits += 1

        yield 4.0*n_hits/i,n_reject/i


def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-n', '--n', type=int, default = 16)
    parser.add_argument('--delta', type=float, default = [0.03,0.1,0.3,0.4,0.5,1.0], nargs='+')
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

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    for delta in args.delta:
        N = 2**args.n
        X = np.empty((N))
        Rejection = np.empty((N))
        for i,(X[i],Rejection[i]) in enumerate(perform_markov(n_trials=N,delta=delta, rng = rng)):
            pass

        errors = np.empty((args.n-1))
        for i in range(args.n-1):
            mean,errors[i],X = data_bunch(X)
        ax1.plot(errors,label=fr'$\delta=${delta},rejection={Rejection.mean():.3},error={abs(mean-np.pi):.6}')

    ax1.legend()
    _,ymax = ax1.get_ylim()
    ax1.set_ylim(0,ymax)
    ax1.set_ylabel('Estimated Error')
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
