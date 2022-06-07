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
    Exercise 2.6: directly sample the positions of 4 disks in a square box without
    periodic boundary conditions, for different covering densities.
    Exercise 2.7: directly sample the positions of 4 disks in a square box with
    periodic boundary conditions
'''

from argparse          import ArgumentParser
from geometry          import GeometryFactory
from matplotlib        import rc
from matplotlib.pyplot import figure, legend, plot, savefig, show, title, xlabel, ylabel, ylim
from numpy             import array, histogram, reshape
from os.path           import basename, splitext
from numpy.random      import default_rng

def direct_disks(sigma    = 0.25,
                 N        = 4,
                 NTrials  = float('inf'),
                 d        = 2,
                 geometry = None,
                 rng      = default_rng()):
    '''Prepare one admissable configuration of disks'''

    def is_overlapped(X):
        '''Determine whether spheres overlap'''
        for i in range(N):
            for j in range(i+1,N):
                if geometry.get_distance(X[i,:],X[j,:])<2*sigma:
                    return True
        return False

    k = 0
    while True:
        X = geometry.LowerBound + geometry.UpperBound * rng.random(size=(N,d))
        if is_overlapped(X):
            if k>NTrials:
                raise Exception(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')
            else:
                k += 1
        else:
            return X



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
                        default = 100,
                        help    = 'Number of bins for histogram')
    parser.add_argument('--periodic',
                        action = 'store_true',
                        default = False)
    parser.add_argument('--L',
                        type    = float,
                        nargs   = '+',
                        default = [1])
    return parser.parse_args()

if __name__=='__main__':
    args           = parse_arguments()
    upper_limit    = -float('inf')
    rng            = default_rng()
    figure(figsize = (12,12))
    for sigma in args.sigma:
        geometry = GeometryFactory(periodic = args.periodic,
                                   L        = array(args.L if len(args.L)==args.d else args.L * args.d),
                                   sigma    = sigma,
                                   d        = args.d)
        eta      = geometry.get_density(N = args.Disks)
        print (f'sigma = {sigma}, eta = {eta}')
        configurations = [direct_disks( sigma    = sigma,
                                        N        = args.Disks,
                                        d        = args.d,
                                        geometry = geometry)[:,0] for _ in range(args.N)]
        positions      = reshape(configurations, args.N*args.Disks)
        hist,bin_edges = histogram(positions,
                                   bins    = args.bins,
                                   density = True)

        plot([0.5*(bin_edges[i] + bin_edges[i+1]) for i in range(len(bin_edges)-1)], hist,
             label = fr'$\sigma=${sigma}, $\eta=$ {eta:.3}')

        upper_limit = max(max(hist),upper_limit)

    title(fr'{args.N:,} Trials, {args.Disks} Disks {geometry.get_description()}')
    legend()
    ylim([0,upper_limit])
    xlabel('Position')
    ylabel('Frequency')
    savefig(get_plot_file_name(args.plot))

    if args.show:
        show()
