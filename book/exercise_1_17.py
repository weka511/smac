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

'''Exercise 1-17: Use a sample transformation to derive random numbers distributed as 0.5 sin(phi)'''

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
    parser.add_argument('-N', '--N', type=int, default=100, help='Number of iterations')
    return parser.parse_args()

def reject_continuous(x0,x1,pi, pi_max=1, rng = np.random.default_rng(),size=1,max_tries=100):
    X = np.zeros(size)
    for i in range(size):
        j = 0
        Upsilon = float('inf')
        while Upsilon > pi(X[i]):
            X[i] = rng.uniform(x0,x1)
            Upsilon = rng.uniform(0,pi_max)
            j += 1
            assert j < max_tries

    return X

def pi(x):
    return 0.5*np.sin(x)

def sample(x0,x1, rng = np.random.default_rng(),size=1):
    def scale(x):
        return 2*x/np.pi -1
    Y = rng.uniform(scale(x0),scale(x1),size=size)
    return np.arccos(Y)

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
    X0 = np.linspace(0,np.pi)
    X = reject_continuous(0,np.pi,pi, pi_max=0.5, rng = rng,size=args.N)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(2,1,1)
    ax1.hist(X,bins='sqrt',density=True,label='Sampled')
    ax1.plot(X0,pi(X0),label=r'$y=0.5\sin(x)$')
    ax1.legend()
    ax1.set_title('Rejection')

    ax2 = fig.add_subplot(2,1,2)
    XX = sample(0,np.pi, rng = rng,size=args.N)
    ax2.hist(XX,bins='sqrt',density=True,label='Sampled')
    ax2.plot(X0,pi(X0),label=r'$y=0.5\sin(x)$')
    ax2.legend()
    ax2.set_title('Direct')

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
