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

'''Exercise 1.4 '''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from markovdiscretepebble import step, markov_discrete_pebble, neighbour_table

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--N', default=100000, type=int)
    parser.add_argument('--m', default=200, type=int)
    parser.add_argument('--n', default=100, type=int)
    return parser.parse_args()

def explore_space(m,n,max_iterations,rng=np.random.default_rng()):
    def getK(i,j):
        def helper(j,values):
            if j < 1:
                return values[0]
            elif j < n-1:
                return values[1]
            else:
                return values[2]
        if i < 1:
            return helper(j,[1,2,3])
        elif i < m-1:
            return helper(j,[4,5,6])
        else:
            return helper(j,[7,8,9])

    Counts = np.zeros((m*n))

    i = 0
    j = 0
    for iteration in range(max_iterations):
        k = getK(i,j)
        k_new = markov_discrete_pebble(k,neighbour_table,rng=rng)
        (i_step,j_step) = step(k,k_new)
        i += i_step
        j += j_step
        Counts[n*i+j] += 1

    mean = 1.0/(m*n)
    sum_sq = 0.0

    Diffs = Counts/float(max_iterations) - mean
    sum_sq =(Diffs**2).sum()

    return Counts, sum_sq, mean

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

    Counts, sum_sq, mean = explore_space(args.m,args.n,args.N,rng=rng)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.hist(Counts)
    ax1.set_title(f'N={args.N:,}: sum_sq={sum_sq:.3}')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
