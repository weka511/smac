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

'''Exercise 2.8 and Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC'''

from argparse import ArgumentParser
from os.path import basename, exists, splitext
from shutil import copyfile
from time import time
from matplotlib import rc
from matplotlib.pyplot import figure, show
import numpy as np
from numpy.random import default_rng
from geometry import GeometryFactory

def markov_disks(X,
                 rng = default_rng(),
                 delta = np.array([0.01,0.01]),
                 geometry = GeometryFactory()):
    '''Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC'''

    def can_move(k,X_proposed):
        '''
            Verify that proposed new position is within the geometry,
            and that the resulting new configuration will be acceptable.
        '''
        if not geometry.is_within_bounds(X_proposed): return False

        for i in range(N):
            if i != k and geometry.get_distance(X[i,:],X_proposed) < 2*geometry.sigma:
                return False

        return True

    N,d = X.shape
    k = rng.integers(0,high=N)
    Delta = -delta + 2* delta*rng.random(size=d)
    X_proposed = geometry.move_to(X[k,:]+Delta)
    if can_move(k,X_proposed):
        X[k,:] = X_proposed
        return k,X
    else:
        return -1,X

def get_coordinate_description(coordinate):
    '''Used to display the name of a oordinate'''
    if coordinate == 0:
        return 'X'
    elif coordinate == 1:
        return 'Y'
    else:
        return 'Z'

def get_coordinate_colour(coordinate):
    'xkcd:red' if coordinate==0 else 'xkcd:blue' if coordinate==1 else 'xkcd:green'

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot == None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext) == 0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    parser.add_argument('--N',
                        type    = int,
                        default = 10000,
                        help    = 'Number of iterations')
    parser.add_argument('--Disks',
                        type    = int,
                        default = 4,
                        help    = 'Number of disks/spheres')
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.125,
                        help    = 'Radius of disk/sphere')
    parser.add_argument('--d',
                        type    = int,
                        choices = [2,3],
                        default = 2,
                        help    = 'Number of dumensions for space')
    parser.add_argument('--periodic',
                        action = 'store_true',
                        default = False,
                        help    = 'Used to specifiy periodic boundary conditions')
    parser.add_argument('--L',
                        type    = float,
                        nargs   = '+',
                        default = [1],
                        help    = 'Length of each side of box (just one value for square/cube)')
    parser.add_argument('--delta',
                        type    = float,
                        nargs   = '+',
                        default = [0.1],
                        help    = 'Maximum distance for each step')
    parser.add_argument('--bins',
                        type    = int,
                        default = 100,
                        help    = 'Number of bins for histogram')
    parser.add_argument('--burn',
                        type    = int,
                        default = 0,
                        help    = 'Used to skip over early steps without accumulating stats')
    parser.add_argument('--frequency',
                        type    = int,
                        default = 1000,
                        help    = 'For reporting progress')
    parser.add_argument('--restart',
                        action = 'store_true',
                        help   = 'Restart from checkpoint')
    parser.add_argument('--eta',
                        type    = float,
                        default = None,
                        help    = 'Used to specify density (override sigma)')
    return parser.parse_args()


class Checkpointer:
    '''Used to save a configuration to a checkpoint, and restore from saved checkpoint'''
    def __init__(self,file='check'):
        self.path = f'{file}.npz'
        self.backup = f'{self.path}~'

    def load(self):
        with load(self.path) as data:
            X = data['X']
            HistogramBins = data['HistogramBins']
            return X,HistogramBins

    def save(self, X = [], geometry = None):

        if exists(self.path):
            copyfile(self.path,self.backup)

        np.savez(self.path,
              X = X, HistogramBins = geometry.HistogramBins)

if __name__=='__main__':
    start  = time()
    args = parse_arguments()
    check = Checkpointer()
    rng = default_rng()
    delta = np.array(args.delta if len(args.delta)==args.d else args.delta * args.d)
    L  = np.array(args.L if len(args.L)==args.d else args.L * args.d)
    geometry = GeometryFactory(periodic = args.periodic, L = L, sigma = args.sigma, d = args.d)
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
                label = f'{get_coordinate_description(j)}',
                alpha = 0.5,
                color = get_coordinate_colour(j))
    ax1.set_title(f'{args.Disks} Disks {geometry.get_description()}: sigma = {geometry.sigma:.3g}, eta = {eta:.3g}, delta = {max(args.delta):.2g}, acceptance = {100*n_accepted/(args.N-args.burn):.3g}%')
    ax1.legend()
    fig.savefig(get_plot_file_name(args.plot))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
