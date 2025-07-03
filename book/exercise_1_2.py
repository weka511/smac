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

'''
    Problem 1.2 from Werner Krauth, Statistical Mechanics, Algorithms & Computations
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show


def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N', '--N', type=int, default=400000, help='Number of steps for one Markov run')
    parser.add_argument('-n', '--n', type=int, default=25, help='Number of iterations')
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


def perform_markov(n_trials,delta=0.1,rng = np.random.default_rng()):
    '''
    Algorithm 1.2 from Werner Krauth, Statistical Mechanics, Algorithms & Computations
    '''
    x, y = rng.uniform(-1, 1,size=(2))
    n_hits = 0
    n_reject = 0

    for i in range(n_trials):
        del_x, del_y = rng.uniform(-delta, delta,size=(2))
        if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
        else:
            n_reject+=1
        if x*x + y*y < 1.0: n_hits += 1

    return (4.0 * n_hits / float(n_trials), n_reject/ float(n_trials))

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    deltas = np.arange(0.1,3,step=0.1)
    errors = np.zeros((len(deltas)))
    rejections = np.zeros((len(deltas)))

    for i in range(len(deltas)):
        sum_sq_error = 0
        sum_reject = 0
        for _ in range(args.n):
            (result,reject) = perform_markov(args.N,delta=deltas[i],rng=rng)
            sum_sq_error += (result - np.pi)**2
            sum_reject += reject

        errors[i] = sum_sq_error/args.n
        rejections[i] = sum_reject/args.n

    fig = figure(figsize=(12,12))

    ax1 = fig.add_subplot(2,1,1)
    ax1a = ax1.twinx()
    plot1 = ax1.plot(deltas, errors, color='xkcd:red', label='Errors')
    plot1a = ax1a.plot(deltas, rejections,color='xkcd:blue', label='Rejections')
    ax1.set_xlabel(r'$\delta$')
    ax1.set_ylabel(r'$Error$')
    ax1a.set_ylabel(r'$Rejection$')
    ax1.set_title(r'Error and rejection rate vs step size')
    plots = plot1 + plot1a
    ax1.legend(plots,[p.get_label() for p in plots])

    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(rejections[1:], errors[1:])
    ax2.set_xlabel('Rejection')
    ax2.set_ylabel('Error')
    ax2.set_title('Error vs rejection rate')

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
