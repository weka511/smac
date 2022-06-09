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

'''Exercise 2.8 and Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC'''

from argparse          import ArgumentParser
from geometry          import GeometryFactory
from matplotlib        import rc
from matplotlib.pyplot import figure, legend, plot, savefig, show, title
from numpy             import any, array, copy
from numpy.random      import default_rng
from os.path           import basename, splitext

def markov_disks(X,
                 rng      = default_rng(),
                 delta    = array([0.01,0.01]),
                 geometry = GeometryFactory(),
                 sigma    = 0.125):
    '''Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC'''

    def can_move(k):
        '''
            Verify that proposed new position is within the geometry,
            and that the resulting new configuration will be acceptable.
        '''
        if any(X[k,:] < geometry.LowerBound): return False
        if any(geometry.UpperBound < X[k,:]): return False

        for i in range(N):
            if i!=k and geometry.get_distance(X[i,:],X[k,:])<2*sigma:
                return False

        return True

    N,d     = X.shape
    k       = rng.integers(0,high=N)
    Delta   = -delta * 2* delta*rng.random(size=d)
    x_save  = copy(X[k,:]) # https://stackoverflow.com/questions/47181092/numpy-views-vs-copy-by-slicing
    X[k,:]  = geometry.move_to(X[k,:]+Delta)   # Provisional move

    if can_move(k):
        return k,X
    else:
        X[k,:] = x_save
        return -1,X

def get_coordinate_description(coordinate):
    if coordinate==0:
        return 'X'
    elif coordinate==1:
        return 'Y'
    else:
        return 'Z'

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

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
                        help    = 'Name of plot file')
    parser.add_argument('--Disks',
                        type    = int,
                        default = 4)
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.125)
    parser.add_argument('--d',
                        type    = int,
                        default = 2)
    parser.add_argument('--periodic',
                        action = 'store_true',
                        default = False)
    parser.add_argument('--L',
                        type    = float,
                        nargs   = '+',
                        default = [1])
    parser.add_argument('--delta',
                        type    = float,
                        nargs   = '+',
                        default = [0.01])
    parser.add_argument('--bins',
                        type    = int,
                        default = 100,
                        help    = 'Number of bins for histogram')
    parser.add_argument('--burn',
                        type    = int,
                        default = 1000)
    parser.add_argument('--frequency',
                        type    = int,
                        default = 1000)
    return parser.parse_args()

if __name__=='__main__':
    args       = parse_arguments()
    rng        = default_rng()
    delta      = array(args.delta if len(args.delta)==args.d else args.delta * args.d)
    geometry   = GeometryFactory(periodic = args.periodic,
                               L        = array(args.L if len(args.L)==args.d else args.L * args.d),
                               sigma    = args.sigma,
                               d        = args.d)
    eta        = geometry.get_density(N = args.Disks)
    X          = geometry.create_configuration(N=args.Disks)
    n_accepted = 0
    histograms = geometry.create_Histograms(n=args.bins)

    for epoch in range(args.N):
        k,X = markov_disks(X,
                           rng      = rng,
                           delta    = delta,
                           geometry = geometry,
                           sigma    = args.sigma)

        if epoch>args.burn:
            if k>-1:
                n_accepted += 1
            for i in range(args.d):
                for x in array(X[:,i]):
                    histograms[i].add(x)
        if epoch%args.frequency ==0:
            print (f'Epoch {epoch:,}')

    figure(figsize=(12,12))

    for j in range(args.d):
        h,bins = histograms[j].get_hist()
        plot([0.5*(bins[i]+bins[i+1]) for i in range(len(h))],h,
             label =f'{get_coordinate_description(j)}')
    title(f'{geometry.get_description()} sigma = {args.sigma}, eta = {eta:.3f}, delta = {max(args.delta):.2g}, acceptance = {100*n_accepted/(args.N-args.burn):.3g}%')
    legend()
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
