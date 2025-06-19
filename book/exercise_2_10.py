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
    Exercise 2.10 and Algorithm 2.9. Generating a hard disk configuration
    from an earlier valid configuration using MCMC. Compare with algorithm
    2.7 - direct-disks.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import maxsize
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from geometry import Geometry, GeometryFactory
from md import get_L
from markov_disks import markov_disks

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

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--N', type = int, default = 1000, help='Number of configurations to be tried')
    parser.add_argument('--NTrials', type = int, default = maxsize, help='Number of attempts to create configuration')
    parser.add_argument('--Disks', type = int, default = 4, help='Number of disks in each configuration')
    parser.add_argument('--sigma', type = float,  default = 0.125,  help='Radius of a disk')
    parser.add_argument('--d', type = int, default =2,  help='Dimensionality of space')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
    parser.add_argument('--L', type = float, default = 1, help='Lengths of walls')
    parser.add_argument('--frequency', type = int, default = 1000,  help  = 'For reporting progress')
    parser.add_argument('--delta', type = float,  default = 0.375, help    = 'Maximum distance for each step')
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

def get_actual_bins(bin_edges):
    return  np.array([0.5*(bin_edges[i] + bin_edges[i+1]) for i in range(len(bin_edges)-1)])

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    geometry = GeometryFactory(periodic=True,L=get_L(args.L, args.d),sigma = args.sigma,d = args.d)
    eta = geometry.get_density(N = args.Disks)
    print (f'sigma = {args.sigma}, eta = {eta:.3}')
    x_coordinates = np.empty((args.N,args.Disks))
    ndisk_pairs = (args.Disks-1)*args.Disks//2
    distances = np.empty((args.N,ndisk_pairs))
    for i in range(args.N):
        configuration = geometry.direct_disks(N=args.Disks,NTrials=args.NTrials)
        x_coordinates[i,:] = configuration[:,0]
        l = 0
        for j in range(args.Disks):
            for k in range(j):
                distances[i,l] = geometry.get_distance(configuration[j,:], configuration[k,:])
                l += 1
    hist,bin_edges = np.histogram( np.reshape(x_coordinates, args.N*args.Disks), bins = args.bins, density = True)


    X = np.zeros((args.N,args.Disks,args.d))
    X[0,:,:] = geometry.create_configuration(N = args.Disks)
    distances_markov = np.zeros((args.N-1,ndisk_pairs))
    n_accepted = 0
    for i in range(1,args.N):
        k,X[i,:,:] = markov_disks(X[i-1,:,:], rng = rng, delta = args.delta, geometry = geometry)
        l = 0
        for j in range(args.Disks):
            for kk in range(j):
                distances_markov[i-1,l] = geometry.get_distance(X[i,j,:], X[i,kk,:])
                l += 1
        if k > -1:
            n_accepted += 1
        if i%args.frequency ==0:
            print (f'Epoch {i:,} Accepted: {n_accepted/i:.1}')

    hist_markov,bin_edges_markov = np.histogram( np.reshape(X[:,:,0], args.N*args.Disks), bins = args.bins, density = True)

    fig = figure(figsize = (12,12))
    fig.suptitle(fr'Comparison between direct disks and MCMC: {args.N:,} Trials, {args.Disks} Disks')

    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(get_actual_bins(bin_edges), hist,label = fr'$\sigma=${args.sigma}, $\eta=${eta:.3}')
    ax1.legend(title='Direct Disks')
    ax1.set_xlabel('x')
    ax1.set_ylabel('Frequency')

    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(distances.ravel(),bins=args.bins,color='xkcd:blue',density=True,label='Histogram')
    ax2.axvline(x=2*args.sigma,color='xkcd:red',label=r'$2\sigma$')
    ax2.set_xlabel(r'$\Delta$')
    ax2.set_ylabel('Frequency')
    ax2.legend()

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(get_actual_bins(bin_edges_markov), hist_markov,label = fr'$\sigma=${args.sigma}, $\eta=${eta:.3}')
    ax3.legend(title='MCMC')
    ax3.set_xlabel('x')
    ax3.set_ylabel('Frequency')

    ax4 = fig.add_subplot(2,2,4)
    ax4.hist(distances_markov.ravel(),bins=args.bins,color='xkcd:blue',density=True,label='Histogram')
    ax4.axvline(x=2*args.sigma,color='xkcd:red',label=r'$2\sigma$')
    ax4.set_xlabel(r'$\Delta$')
    ax4.set_ylabel('Frequency')
    ax4.legend()

    fig.tight_layout(h_pad=0.3)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
