#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''Exercise 1.18 and Algorithm 1.25 from Krauth'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.stats import mode

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--theta',type=float,default = np.pi/4)
    parser.add_argument('--N',type=int,default = 1000, help = 'Number of iterations of binomial convolution')
    parser.add_argument('--M',type=int,default = 10000, help = 'Number of samples in one run of direct-pi')
    parser.add_argument('--m',type=int,default = 1000, help = 'Number of runs of direct-pi')
    parser.add_argument('--bins',default = 'sqrt', help = 'Binning strategy for histogram')
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


def binomial_convolution(theta = np.pi/4,N=9):
    '''
    Algorithm 1.25 from Krauth

    This function uses numpy's built-in convolution
    '''
    a = np.ones((1))
    thetas = np.array([1-theta,theta])
    for n in range(1,N):
        a = np.convolve(a,thetas)
    return a

def direct_pi(m,rng = np.random.default_rng()):
    n_hits = 0
    for i in range(m):
        x,y = rng.uniform(-1,1,2)
        if x**2 + y**2 < 1:
            n_hits += 1
    return n_hits/m

def get_frequence_from_direct_pi(M,m,rng = np.random.default_rng()):
    frequency = np.zeros((M))
    for i in range(M):
        frequency[i] = direct_pi(m,rng=rng)
    return frequency

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    fig = figure(figsize=(12,12))
    fig.suptitle('Exercise 1.18')

    P = binomial_convolution(theta = args.theta,N=args.N)
    imax = P.argmax()
    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(P,label=f'Peak: {imax/len(P)}')
    ax1.set_title(fr'Binomial convolution $\theta=${args.theta:.4}, {args.N:,} iterations')
    ax1.set_xlabel('$x$')
    ax1.set_ylabel(r'$\pi(x)$')
    ax1.legend()

    frequency = get_frequence_from_direct_pi(args.M,args.m,rng=rng)
    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(frequency,bins=args.bins,label=f'{mode(frequency).mode}')
    ax2.set_title(f'Direct pi: {args.m:,} runs of {args.M:,} samples.')
    ax2.set_xlabel('$x$')
    ax2.set_ylabel(r'$\pi(x)$')
    ax2.legend()

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(P/args.N,label=f'{imax/len(P)}')
    ax3.set_title(f'Scaled Binomial coefficients divided by {args.N:,}')
    ax3.set_xlabel('$x$')
    ax3.set_ylabel(r'$\pi(x)$')
    ax3.legend()

    rescaled = (frequency-np.pi/4)/np.sqrt((np.pi/4)*(1-np.pi/4))
    ax4 = fig.add_subplot(2,2,4)
    ax4.hist(rescaled,bins=args.bins,label=f'{mode(rescaled).mode}')
    ax4.legend()
    ax4.set_xlabel(r'$\frac{x-\frac{\pi}{4}}{\sigma}$')
    ax4.set_ylabel(r'$\pi(x)$')
    ax4.set_title('Direct pi--normalized')

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
