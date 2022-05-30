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

'''Exercise 2.6'''

from argparse          import ArgumentParser
from matplotlib        import rc
from matplotlib.pyplot import figure, hist, savefig, show
from numpy             import array, reshape
from numpy.linalg      import norm
from os.path           import basename, splitext
from numpy.random      import random

def direct_disks(sigma = 0.25,
                 x0      = -1,
                 x1      = 1,
                 N       = 4,
                 NTrials = 25,
                 d       = 2):
    def is_overlapped(X):
        for i in range(N):
            for j in range(i+1,N):
                if norm(X[i,:]-X[j,:])<2*sigma:
                    return True
        return False

    for k in range(NTrials):
        X = x0 + (x1-x0) * random(size=(N,d))
        if not is_overlapped(X):
            return X

    raise Exception(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')

def sample(config):
    Xs = config[:,0]
    x=0


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
                        default =10000)
    parser.add_argument('--Disks',
                        type    = int,
                        default =4)
    parser.add_argument('--sigma',
                        type = float,
                        default=0.25)
    parser.add_argument('--d',
                        type    = int,
                        default =2)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()
    Xs   = reshape([direct_disks(sigma = args.sigma,
                                N       = args.Disks,
                                NTrials = 2000,
                                d       = args.d)[:,0] for _ in range(args.N)],
                   args.N*args.Disks)

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize=(12,12))
    hist(Xs, bins=100)
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
