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
    Exercise 1.20. Implemement algorithm 1.28 (data-bunch).
    Second part: test it also with the output of Alg 1.6,
    markov-discrete-pebble.py.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import maxsize
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

 # Transfer matrix - (1.14)

T = np.array([[0.5,  0.25, 0,    0.25, 0,    0,    0,    0,    0],
              [0.25, 0.25, 0.25, 0,    0.25, 0,    0,    0,    0],
              [0,    0.25, 0.5,  0,    0,    0.25, 0,    0,    0],
              [0.25, 0,    0,    0.25, 0.25, 0,    0.25, 0,    0],
              [0,    0.25, 0,    0.25, 0,    0.25, 0,    0.25, 0],
              [0,    0,    0.25, 0,    0.25, 0.25, 0,    0,    0.25],
              [0,    0,    0,    0.25, 0,    0,    0.5,  0.25, 0],
              [0,    0,    0,    0,    0.25, 0,    0.25, 0.25, 0.25],
              [0,    0,    0,    0,    0,    0.25, 0,    0.25, 0.5]
              ])


def markov_discrete_pebble(start=0,
                           N=maxsize,
                           neighbour_table=np.array([[ 1,  3, -1, -1], # Checked against table 1-3
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
    parser.add_argument('--N',type=int,default=6)
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

def get_correlation_times(CorrelationTime):
    correlation_times = [0]
    while correlation_times[-1] < 2**args.N-1:
        correlation_times.append( correlation_times[-1] + CorrelationTime)
    return correlation_times

def get_ev2(T,n):
    eigenvalues,_ = np.linalg.eig(T)
    ev_2 = np.sort(eigenvalues)[-2]
    Ev2_n = np.ones((n))
    for i in range(1,n):
        Ev2_n[i] = ev_2 * Ev2_n[i-1]
    return ev_2,Ev2_n

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

    Bunched = Counts[0,:]
    error = np.zeros((args.N))
    for i in range(args.N):
        _,error[i],Bunched = data_bunch(Bunched)

    ev_2,Ev2_n = get_ev2(T,2**args.N)

    correlation_times = get_correlation_times(CorrelationTime = -1/np.log(ev_2))

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    steps = np.array(range(2**args.N))

    ax1.scatter(steps,np.abs(Frequency[0,:] - 1/9),label='Deviation from expected frequency',s=5,c='r')
    ax1.scatter(steps,Ev2_n,label='Powers of second eigenvalue',s=5,c='b')
    for i in range(0,len(correlation_times)-1):
        ax1.axvspan(correlation_times[i],correlation_times[i+1],
                    color='lightgrey' if i%2==0 else 'white',
                    hatch='/' if i%2==0 else '-',
                    zorder=-1,
                    label='Correlation Times' if i==0 else None)
    ax1.set_xlabel('Step')
    _,x1 = ax1.get_xlim()
    ax1.set_xlim(0,x1)
    ax1.legend()

    ax2.plot(error,label=f'Standard deviation after bunching {error[-2]:.6}')
    ax2.set_xlabel('Fold')
    ax2.set_ylabel('Error')
    ax2.legend()

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
