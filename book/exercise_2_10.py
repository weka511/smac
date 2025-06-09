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
    from an earlier valid configuration using MCMC
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from markov_disks import markov_disks, Checkpointer
from geometry import Geometry, GeometryFactory
from md import get_L

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
    parser.add_argument('--bins', type = int, default = 100, help = 'Number of bins for histogram')
    parser.add_argument('--burn', type = int, default = 0, help = 'Used to skip over early steps without accumulating stats')
    parser.add_argument('--frequency', type = int, default = 1000,  help  = 'For reporting progress')
    parser.add_argument('--restart', action = 'store_true', help  = 'Restart from checkpoint')
    parser.add_argument('--eta', type = float, default = None, help = 'Used to specify density (override sigma)')
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

if __name__=='__main__':
    start  = time()
    args = parse_arguments()
    check = Checkpointer()
    rng = np.random.default_rng(args.seed)
    delta = np.array(args.delta if len(args.delta)==args.d else args.delta * args.d)
    geometry = GeometryFactory(periodic = True, L = get_L(args.L,args.d), sigma = args.sigma, d = args.d)
    if args.eta != None:
        geometry.set_sigma(eta = args.eta, N = args.Disks)
    eta = geometry.get_density(N = args.Disks)
    n_accepted = 0
    if args.restart:
        X,HistogramBins = check.np.load()
        histograms = geometry.create_Histograms(n = args.bins, HistogramBins = HistogramBins)
    else:
        X = geometry.create_configuration(N = args.Disks)
        histograms = geometry.create_Histograms(n=args.bins)

    for epoch in range(args.N):
        k,X = markov_disks(X, rng = rng, delta = delta, geometry = geometry)

        if epoch > args.burn:
            if k >- 1:
                n_accepted += 1
            for i in range(args.d):
                for x in np.array(X[:,i]):
                    histograms[i].add(x)

        if epoch%args.frequency ==0:
            print (f'Epoch {epoch:,} Accepted: {n_accepted:,}')
            check.save(X = X, geometry   = geometry)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)

    for j in range(args.d):
        h,bins = histograms[j].get_hist()
        ax1.bar([0.5*(bins[i]+bins[i+1]) for i in range(len(h))],h,
                width = [0.5*(bins[i+1]-bins[i]) for i in range(len(h))],
                label = f'{Geometry.get_coordinate_description(j)}',
                alpha = 0.5,
                color = Geometry.get_coordinate_colour(j))
        break
    ax1.set_title(fr'{args.Disks} Disks {geometry.get_description()}: $\sigma=${geometry.sigma:.3g}, $\eta=${eta:.3g}, $\delta=${max(args.delta):.2g}, acceptance = {100*n_accepted/(args.N-args.burn):.3g}%')
    ax1.legend()
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
