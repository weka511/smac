#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

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
    Exercise 2.6: directly sample the positions of 4 disks in a square box without
    periodic boundary conditions, for different covering densities.
    Exercise 2.7: directly sample the positions of 4 disks in a square box with
    periodic boundary conditions
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import maxsize
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from geometry import GeometryFactory

def direct_disks(sigma = 0.25, N = 4, NTrials = maxsize, d = 2, geometry = None, rng = np.random.default_rng()):
    '''
    Prepare one admissable configuration of disks

    Parameters:
        sigma
        N
        NTrials
        d
        geometry
        rng

    Returns:
        X, an array containing the coordinates of N points such that we can position N
        disks of radius sigma, with the centre of each disk at the corresponding point
        of X.
    '''

    def is_overlapped(X):
        '''Determine whether spheres overlap'''
        for i in range(N):
            for j in range(i+1,N):
                if geometry.get_distance(X[i,:],X[j,:]) < 2*sigma:
                    return True
        return False

    for k in range(NTrials):
        X = geometry.LowerBound + geometry.UpperBound * rng.random(size=(N,d))
        if not is_overlapped(X): return X

    raise RuntimeError(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')

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

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--N', type = int, default = 10000, help='Number of configurations to be tried')
    parser.add_argument('--NTrials', type = int, default = maxsize, help='Number of attempts to create configuration')
    parser.add_argument('--Disks', type = int, default = 4, help='Number of disks in each configuration')
    parser.add_argument('--sigma', type = float,  nargs   = '+',  default = [0.25],  help='Radius of a disk')
    parser.add_argument('--d', type = int, default =2,  help='Dimensionality of space')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('--bins', type = int, default = 100, help = 'Number of bins for histogram')
    parser.add_argument('--periodic', action = 'store_true', default = False, help='Use periodic boundary conditions')
    parser.add_argument('--L', type = float, nargs   = '+', default = [1], help='Lenghts of walls')
    return parser.parse_args()

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    upper_limit = -float('inf')
    rng = np.random.default_rng(args.seed)
    sides  = np.array(args.L if len(args.L)==args.d else args.L * args.d)
    fig = figure(figsize = (12,12))
    ax1 = fig.add_subplot(1,1,1)
    for sigma in args.sigma:
        try:
            geometry = GeometryFactory(periodic = args.periodic, L = sides, sigma = sigma, d = args.d)
            eta = geometry.get_density(N = args.Disks)
            print (f'sigma = {sigma}, eta = {eta}')
            configurations = [direct_disks(sigma=sigma,N=args.Disks,d=args.d,geometry=geometry,NTrials=args.NTrials)[:,0]
                              for _ in range(args.N)]
            positions = np.reshape(configurations, args.N*args.Disks)
            hist,bin_edges = np.histogram(positions, bins = args.bins, density = True)
            xs = [0.5*(bin_edges[i] + bin_edges[i+1]) for i in range(len(bin_edges)-1)]
            ax1.plot(xs, hist,label = fr'$\sigma=${sigma}, $\eta=$ {eta:.3}')
            upper_limit = max(max(hist),upper_limit)
        except RuntimeError as e:
            print (e)

    ax1.set_title(fr'{args.N:,} Trials, {args.Disks} Disks {geometry.get_description()}')
    ax1.legend()
    ax1.set_ylim([0,upper_limit])
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Frequency')

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
