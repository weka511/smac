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
from matplotlib.pyplot import arrow, axis, figure, grid, legend, scatter, savefig,show
from numpy             import dot, sqrt
from numpy.random      import default_rng
from os.path           import basename, splitext

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

if __name__=='__main__':
    L      = 1

    parser = ArgumentParser(description = __doc__)
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
                        default = 42,
                        help    = 'Seed for random number generator')
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.1,
                        help    = 'Radius of spheres')
    args   = parser.parse_args()

    rng    = default_rng(seed = args.seed)
    for _ in range(1000):
        x1, x2, v1, v2 = sample(rng, sigma = args.sigma, L = L)
        DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
        print (DeltaT)
        if DeltaT<float('inf'): break

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
    x1_prime = x1 + DeltaT *v1
    x2_prime = x2 + DeltaT *v2
    scatter(x1_prime[0],x1_prime[1],label='x1"',s=marker_size)
    scatter(x2_prime[0],x2_prime[1],label='x2"',s=marker_size)
    grid()

    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
