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
    Exercise 1.4: implement algorithm 1.6, markov-discrete-pebble, using a
    subroutine for the numbering scheme and neighbour table. Check that,
    during long runs, all sites are visited equally often.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.stats import chisquare
from nbr import NeighbourTable

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--m', default=51,type=int,help='Number of rows')
    parser.add_argument('--n', default=91,type=int,help='Number of columns')
    parser.add_argument('--N', default=1000,type=int,help='Number of steps for Markov process')
    return parser.parse_args()

def markov_discrete_pebble(k,Table,rng=np.random.default_rng()):
    '''
    Algorithm 1.6: discrete Markov Chain Monte Carlo for the pebble game

    Parameters:
        k       State
        Table   Transition table
        rng     Random number generator

       Returns:
          Next state
    '''
    return Table[k,rng.integers(4)]


def get_frequencies(m,n,N,rng=np.random.default_rng()):
    '''
    Use markov_discrete_pebble to explore the state space, and determine
    frequency with which each state is visited.

    Parameters:
        m        Number of rows
        n        Number of columns
        N        Number of steps for Markov process
        rng      Random number generator

    Returns:
        An array showing frequencies for each state
    '''
    nbt = NeighbourTable(m,n)
    Table = nbt.create_Table()
    Counts = np.zeros((m*n))
    k = rng.integers(m*n)
    log_errors = []
    log_iterations = []
    next_sample = 10
    log_next_sample = 1
    for i in range(N):
        k = markov_discrete_pebble(k,Table,rng=rng)
        Counts[k] += 1
        if i + 1 == next_sample:
            error = np.std(Counts[:i]/next_sample)
            if error > 0:
                log_error = np.log10(error)
                log_errors.append(log_error)
                log_iterations.append(log_next_sample)
            next_sample *= 10
            log_next_sample += 1
    while log_errors[0] == 0:
        log_errors.pop(0)
        log_iterations.pop(0)
    return Counts / args.N,log_iterations,log_errors

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

    Frequencies,log_iterations,log_errors = get_frequencies(args.m,args.n,args.N,rng=rng)

    statistic,pvalue = chisquare(Frequencies)
    mean = np.mean(Frequencies)
    std = np.std(Frequencies)

    fig = figure(figsize=(12,12))
    fig.suptitle(rf'N={args.N:,}, m={args.m}, n={args.n}')
    ax1 = fig.add_subplot(2,2,1)
    ax1.hist(Frequencies,bins='sqrt')
    ax1.set_title(rf'$\chi^2=${statistic:.3}, pvalue={pvalue:.3}, $\sigma=${std:.3}, CV={std/mean:.3}')
    ax1.axvline(mean+std,color='r',linestyle='dashed')
    ax1.axvline(mean+2*std,color='r',linestyle='dashdot')
    ax1.axvline(mean+3*std,color='r',linestyle='dotted')
    ax1.axvline(mean-std,color='r',linestyle='dashed')
    ax1.axvline(mean-2*std,color='r',linestyle='dashed')
    ax1.axvline(mean-3*std,color='r',linestyle='dotted')

    ax2 = fig.add_subplot(2,2,2)
    map2 = ax2.imshow(Frequencies.reshape(args.m,args.n),cmap='viridis')
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(log_iterations,log_errors)
    ax3.set_xlabel('Log N trials')
    ax3.set_ylabel('Log Error')
    ax3.set_title('Error vs iteration number')

    fig.colorbar(map2)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
