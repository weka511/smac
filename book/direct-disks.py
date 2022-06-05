#!/usr/bin/env python

# Copyright (C) 2022 Simon Crase

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
    Exercise 2.6: directly sample the positions of 4 disks ina square box without
    periodic boundary conditions, for different covering densities.
'''

from argparse          import ArgumentParser
from matplotlib        import rc
from matplotlib.pyplot import figure, legend, plot, savefig, show, title, xlabel, ylabel, ylim
from numpy             import array, histogram, pi, reshape
from numpy.linalg      import norm
from os.path           import basename, splitext
from numpy.random      import random

def direct_disks(sigma = 0.25,
                 x0      = -1,
                 x1      = 1,
                 N       = 4,
                 NTrials = None,
                 d       = 2):
    '''Prepare one admissable configuration of disks'''
    def is_overlapped(X):
        for i in range(N):
            for j in range(i+1,N):
                if norm(X[i,:]-X[j,:])<2*sigma:
                    return True
        return False

    k = 0
    while True:
        X = x0 + sigma + (x1 - x0 - 2*sigma) * random(size=(N,d))
        if is_overlapped(X):
            k += 1
            if NTrials != None and k>=NTrials:
                break
        else:
            return X

    raise Exception(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')

def get_density(sigma=0.25,L=1,N=4):
    return N*pi*sigma**2/(4*L**2)

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--N',
                        type    = int,
                        default = 10000)
    parser.add_argument('--Disks',
                        type    = int,
                        default = 4)
    parser.add_argument('--sigma',
                        type    = float,
                        nargs   = '+',
                        default = [0.25])
    parser.add_argument('--d',
                        type    = int,
                        default =2)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    parser.add_argument('--bins',
                        type    = int,
                        default = 1000,
                        help    = 'Number of bins for histogram')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()

    figure(figsize=(12,12))
    for sigma in args.sigma:
        print (f'sigma={sigma}')
        hist,bin_edges = histogram(reshape([direct_disks( sigma   = sigma,
                                                          N       = args.Disks,
                                                          d       = args.d)[:,0] for _ in range(args.N)],
                                           args.N*args.Disks),
                                   bins    = args.bins,
                                   density = True)
        plot([0.5*(bin_edges[i] + bin_edges[i+1]) for i in range(len(bin_edges)-1)], hist,
             label = fr'$\sigma=${sigma}, $\eta=$ {get_density(sigma=sigma,L=1,N=4):.3}')

    title(fr'{args.N:,} Trials, {args.Disks} Disks')
    legend()
    ylim([0,1])
    xlabel('Position')
    ylabel('Frequency')
    savefig(get_plot_file_name(args.plot))

    if args.show:
        show()
