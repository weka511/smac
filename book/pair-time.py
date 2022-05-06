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

'''Exercise 2.1/algorithm 2.2 Pair Time. Pair collision timne for two particles.'''

from argparse          import ArgumentParser
from matplotlib        import rc
from matplotlib.pyplot import arrow, axis, figure, grid, hist, legend, scatter, savefig, show, title
from numpy             import dot, sqrt
from numpy.linalg      import norm
from numpy.random      import default_rng
from os.path           import basename, splitext
from sys               import maxsize

def get_pair_time(x1, x2, v1, v2, sigma=0.01):
    '''Algorithm 2.2 Pair Time. Pair collision timne for two particles'''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    Upsilon = dot(Delta_x,Delta_v)**2 - dot(Delta_v,Delta_v)*(dot(Delta_x,Delta_x)-4*sigma**2)
    return - (dot(Delta_x,Delta_v)+sqrt(Upsilon))/dot(Delta_v,Delta_v) if Upsilon>0 and dot(Delta_x,Delta_v) <0 else float('inf')

def sample(rng,
           L      = 1,
           V      = 1,
           sigma  = 0.1):
    '''Find one sample where points admissable'''
    while True:
        x1 = -L + 2 * L * rng.random((args.d,))
        x2 = -L + 2 * L * rng.random((args.d,))
        v1 = -V + 2 * V * rng.random((args.d,))
        v2 = -V + 2 * V * rng.random((args.d,))
        if dot(x1-x2,x1-x2) > 4 * sigma**2 and dot(x1 - x2,v1 - v2)<0:
            return x1,x2, v1, v2

def get_plot_file_name(plot):
    '''Determine plot file name'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def create_rng(seed0):
    '''Make sure run is reproducible by displaying seed'''
    rng    = default_rng(seed = seed0)
    if seed0==None:
        seed = rng.integers(0,maxsize)
        print (f'Setting seed to {seed}')
        return default_rng(seed = seed)
    else:
        print (f'seed={seed0}')
        return rng

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--action',
                        default = 'run',
                        choices = ['test', 'run'])
    parser.add_argument('--d',
                        type    = int,
                        default = 2,
                        choices = [2,3],
                        help    = 'Dimension of space')
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    parser.add_argument('--seed',
                        type    = int,
                        default = None,
                        help    = 'Seed for random number generator')
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.1,
                        help    = 'Radius of spheres')
    parser.add_argument('--N',
                        type = int,
                        default = 10000000,
                        help = 'Number of iterations')

    return parser.parse_args()

if __name__=='__main__':
    args   = parse_arguments()
    L      = 1
    rng    = create_rng(args.seed)

    if args.action == 'run':
        Distances = []
        for _ in range(args.N):
            x1, x2, v1, v2 = sample(rng, sigma = args.sigma, L = L)
            DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
            if DeltaT<float('inf'):
                x1_prime = x1 + DeltaT *v1
                x2_prime = x2 + DeltaT *v2
                Distances.append((norm(x1_prime-x2_prime)-2*args.sigma)/2*args.sigma)
            else:
                pass
        figure(figsize=(10,10))
        hist(Distances,bins=250)
        title(f'Distances of centres compared to $2\\sigma$ for N={args.N}')

    if args.action=='test':
        for _ in range(1000):
            x1, x2, v1, v2 = sample(rng, sigma = args.sigma, L = L)
            DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
            print (DeltaT)
            if DeltaT<float('inf'): break

        x1_prime = x1 + DeltaT *v1
        x2_prime = x2 + DeltaT *v2
        distance = norm(x1_prime-x2_prime)
        print (2*args.sigma, distance, abs(2*args.sigma-distance)/2*args.sigma)
        rc('font',**{'family':'serif','serif':['Palatino']})
        rc('text', usetex=True)
        fig = figure(figsize=(10,10))
        ax  = fig.add_subplot(111)
        ax.axis([-L,  L, -L, L])
        r_display_coordinates = ax.transData.transform([args.sigma,0])[0] - ax.transData.transform([0,0])[0] # https://stackoverflow.com/questions/65174418/how-to-adjust-the-marker-size-of-a-scatter-plot-so-that-it-matches-a-given-radi
        marker_size            = 0.5*(2*r_display_coordinates)**2 # fudge factor
        scatter(x1[0],x1[1],label='x1',s=marker_size)
        scatter(x2[0],x2[1],label='x2',s=marker_size)
        arrow(x1[0],x1[1],0.25*DeltaT*v1[0],0.25*DeltaT*v1[1],head_width=0.0125)
        arrow(x2[0],x2[1],0.25*DeltaT*v2[0],0.25*DeltaT*v2[1],head_width=0.0125)

        scatter(x1_prime[0],x1_prime[1],label='x1"',s=marker_size)
        scatter(x2_prime[0],x2_prime[1],label='x2"',s=marker_size)
        grid()

    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
