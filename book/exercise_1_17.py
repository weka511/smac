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
    parser.add_argument('-N', '--N', type=int, default=100000, help='Number of iterations for rejestion sampling')
    parser.add_argument('-n', '--n', type=int, default=1000, help='Number of steps for direct sampling')
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

def sample_sin(x0,x1, rng = np.random.default_rng(),size=1):
    def scale(x):
        return 2*x/np.pi -1
    Y = rng.uniform(scale(x0),scale(x1),size=size)
    return np.arccos(Y)

def sample_cos(x0,x1, rng = np.random.default_rng(),size=1):
    def scale(x):
        return x/np.pi
    Y = rng.uniform(scale(x0),scale(x1),size=size)
    return np.arcsin(Y)

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
    fig.suptitle(f'Exercise 1.17')
    # Plot rejection sampling of sin

    Rejection_Samples_sin = reject_continuous(0,np.pi,pi, pi_max=0.5, rng = rng,size=args.N)
    X0 = np.linspace(0,np.pi,num=args.n)
    ax1 = fig.add_subplot(2,2,1)
    ax1.hist(Rejection_Samples_sin,bins='sqrt',density=True,label='Sampled')
    ax1.plot(X0,pi(X0),label=r'$y=0.5\sin(x)$')
    ax1.legend()
    ax1.set_title(f'Rejection {args.N:,} iterations')
    ax1.set_xlabel('$x$')
    ax1.set_ylabel(r'$\pi(x)$')

    # Plot direct sampling of sin

    Direct_Samples = sample_sin(0,np.pi, rng = rng,size=args.N)
    ax3 = fig.add_subplot(2,2,3)
    ax3.hist(Direct_Samples,bins='sqrt',density=True,label='Sampled')
    ax3.plot(X0,pi(X0),label=r'$y=0.5\sin(x)$')
    ax3.legend()
    ax3.set_title(f'Direct: {args.n:,} points')
    ax3.set_xlabel('$x$')
    ax3.set_ylabel(r'$\pi(x)$')

    # Plot rejection sampling of cos

    X0_cos = np.linspace(0,0.5*np.pi,num=args.n)
    Rejection_Samples_cos = reject_continuous(0,0.5*np.pi, np.cos, rng = rng,size=args.N)
    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(Rejection_Samples_cos,bins='sqrt',density=True,label='Sampled')
    ax2.plot(X0_cos,np.cos(X0_cos),label=r'$y=\cos(x)$')
    ax2.legend()
    ax2.set_title(f'Rejection {args.N:,} iterations')
    ax2.set_xlabel('$x$')
    ax2.set_ylabel(r'$\pi(x)$')

    # Plot direct sampling of cos

    Direct_Samples_cos = sample_cos(0,np.pi, rng = rng,size=args.N)
    ax4 = fig.add_subplot(2,2,4)
    ax4.hist(Direct_Samples_cos,bins='sqrt',density=True,label='Sampled')
    ax4.plot(X0_cos,np.cos(X0_cos),label=r'$y=\cos(x)$')
    ax4.legend()
    ax4.set_title(f'Direct: {args.n:,} points')
    ax4.set_xlabel('$x$')
    ax4.set_ylabel(r'$\pi(x)$')

    fig.tight_layout(pad=3)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
