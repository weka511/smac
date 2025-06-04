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
Compare molecular dynamics with direct disks monte carlo

'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import create_config, event_disks
from geometry import Box

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N','--N', type = int, default = 1000, help = 'Number of iterations')
    parser.add_argument('-n','--n', type = int, default = 4, help = 'Number of spheres')
    parser.add_argument('-m','--m', type = int, default = 100, help = 'Number of attempts')
    parser.add_argument('--sigma', type = float, default = [0.1], nargs='+', help = 'Radius of spheres')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
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

def create_md(N=1000,sigma=0.1,n=4,rng = np.random.default_rng(),M=25):
    Positions = np.empty((n,N))
    Xs, Vs = create_config(n=n,rng=rng, sigma=sigma,M=M,verbose=False)
    for i in range(N):
        event_disks(Xs,Vs, sigma=sigma)
        Positions[:,i] = Xs[:,0]
    return Positions

def create_mc(N=1000,sigma=0.1,n=4,rng = np.random.default_rng(),m=100):
    def sample():
        for _ in range(m):
            proposed = geometry.propose(n,rng =rng)
            if geometry.admissable(proposed): return proposed
        raise RuntimeError(f'Failed to create admissable sample after {m} attempts')
    Positions = np.empty((n,N))
    geometry = Box(sigma = sigma)
    for i in range(N):
        proposed = sample()
        Positions[:,i] = proposed[:,0]
    return Positions

def get_bins(bins):
    '''
    Used to parse args.bins: either a number of bins, or the name of a binning strategy.
    '''
    try:
        return int(bins)
    except ValueError:
        if bins in ['auto', 'fd', 'doane', 'scott', 'sturges', 'sqrt', 'stone', 'rice']:
            return bins
        raise ArgumentTypeError(f'Invalid binning strategy "{bins}"')

def get_rows_cols(k):
    r = int(np.sqrt(k))
    c = k // r
    while r*c < k:
        r +=1
        if  r*c < k:
            c += 1
    return r,c

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    r,c = get_rows_cols(len(args.sigma))

    fig = figure(figsize=(12,12))
    fig.suptitle(f'A comparison of Molecular Dynamics and Acceptance/Rejection sampling')

    for i,sigma in enumerate(args.sigma):
        n_md,bins = np.histogram(create_md(N=args.N,sigma=sigma,n=args.n,rng=rng,M=args.m),bins=args.bins)
        n_mc,_ = np.histogram(create_mc(N=args.N,sigma=sigma,n=args.n,rng=rng,m=args.m),bins=bins)
        x = (bins[1:] + bins[:-1]) / 2
        ax1 = fig.add_subplot(r,c,i+1)
        ax1.set_title(fr'$\sigma=${sigma}, N={args.N:,}, n={args.n}')
        ax1.plot(x,n_md,label='Molecular Dynamics')
        ax1.plot(x,n_mc,label='Acceptance/Rejection')
        ax1.legend()

    fig.tight_layout(h_pad=3,pad=2)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
