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
    Exercise 2.8 and Algorithm 2.9. Generating a hard disk configuration
    from an earlier valid configuration using MCMC
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext, exists
from os import replace
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from markov_disks import markov_disks
from geometry import Geometry, GeometryFactory
from smacfiletoken import Registry

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--N', type = int,  default = 10000, help = 'Number of iterations')
    parser.add_argument('--Disks', type = int, default = 4, help = 'Number of disks/spheres')
    parser.add_argument('--sigma', type = float, default = 0.125, help = 'Radius of disk/sphere')
    parser.add_argument('--d', type = int, choices = [2,3], default = 2, help = 'Number of dimensions for space')
    parser.add_argument('--L', type = float, nargs = '+', default = [1], help = 'Length of each side of box (just one value for square/cube)')
    parser.add_argument('--delta', type = float, nargs   = '+', default = [0.1], help    = 'Maximum distance for each step')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
    parser.add_argument('--burn', type = int, default = 0, help = 'Used to skip over early steps without accumulating stats')
    parser.add_argument('--frequency', type = int, default = 1000,  help  = 'For reporting progress')
    parser.add_argument('--restart', default = None, help  = 'Restart from checkpoint')
    parser.add_argument('--eta', type = float, default = None, help = 'Used to specify density (override sigma)')
    return parser.parse_args()

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
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    registry = Registry()
    registry.register_all("md%d.txt")
    if args.restart == None:
        Disks = args.Disks
        delta = np.array(args.delta if len(args.delta)==args.d else args.delta * args.d)
        L = Geometry.create_L(args.L,args.d)
        geometry = GeometryFactory(L = L, sigma = args.sigma, d = args.d)
        if args.eta != None:
            geometry.set_sigma(eta = args.eta, N = Disks)
        X = geometry.create_configuration(N = Disks)
        bins = get_bins(args.bins)
    else:
        npzfile = np.load(args.restart)
        X = npzfile['X']
        counts = npzfile['counts']
        bins =  npzfile['bins']
        L = npzfile['L']
        sigma = float(npzfile['sigma'])
        delta = npzfile['delta']
        Disks,d = X.shape
        geometry = GeometryFactory(L = L, sigma = sigma, d = d)

    eta = geometry.get_density(N = Disks)
    n_accepted = 0
    X_all_disks = np.empty((args.N,Disks))

    for _ in range(args.burn):
        _,X = markov_disks(X, rng = rng, delta = delta, geometry = geometry)
    for epoch in range(args.N):
        if registry.is_kill_token_present():
            X_all_disks = X_all_disks[0:epoch,:]
            break
        k,X = markov_disks(X, rng = rng, delta = delta, geometry = geometry)
        X_all_disks[epoch,:] = X[:,0]
        if k >- 1:
            n_accepted += 1

        if epoch%args.frequency ==0:
            print (f'Epoch {epoch:,} Accepted: {n_accepted:,}')

    n,bins = np.histogram(X_all_disks,bins=bins)
    if args.restart == None:
        counts = n
    else:
        counts += n

    save_file = get_file_name(args.out,default_ext='npz')
    if exists(save_file):
        backup_file = save_file + '~'
        replace(save_file,backup_file)

    np.savez(save_file,
             X=X,counts=counts,bins=bins,L=L,sigma=geometry.sigma,delta=delta)

    fig = figure(figsize=(12,12))

    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(0.5*(bins[0:-1]+bins[1:]),counts/counts.sum(),color='blue')
    ax1.set_title(fr'{Disks} Disks {geometry.get_description()}: '
                  fr'{counts.sum()//Disks:,} iterations, '
                  fr'$\sigma=${geometry.sigma:.3g}, '
                  fr'$\eta=${eta:.3g}, '
                  fr'$\delta=${max(args.delta):.2g}, '
                fr'acceptance = {100*n_accepted/(args.N-args.burn):.3g}%')
    ax1.axvline(x=geometry.sigma,color='red',linestyle='dashed')
    ax1.axvline(x=L[0]-geometry.sigma,color='red',linestyle='dashed')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Frequency')

    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
