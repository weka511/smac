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

'''Exercise 2.1/algorithm 2.2 Pair Time. Pair collision time for two particles.'''

from argparse          import ArgumentParser
from matplotlib        import rc
from matplotlib.pyplot import arrow, axis, figure, grid, hist, legend, scatter, savefig, show, title, xlim
from md                import create_rng, get_pair_time, sample
from numpy             import dot, sqrt, std
from numpy.linalg      import norm
from os.path           import basename, splitext


def get_time_of_closest_approach(x1, x2, v1, v2):
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    return -dot(Delta_v,Delta_x)/dot(Delta_v,Delta_v)



def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot



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
    L      = [1]*args.d
    rng    = create_rng(args.seed)

    if args.action == 'run':
        Distances = []
        Dots      = []
        for _ in range(args.N):
            x1, x2, v1, v2 = sample(rng, sigma = args.sigma, L = L)
            DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
            if DeltaT<float('inf'):
                x1_prime = x1 + DeltaT *v1
                x2_prime = x2 + DeltaT *v2
                Distances.append((norm(x1_prime-x2_prime)-2*args.sigma)/2*args.sigma)
            else:
                t0            = min(get_time_of_closest_approach(x1,x2,v1,v2),0)
                Delta_x       = x1 - x2
                Delta_v       = v1 - v2
                Delta_x_prime = Delta_x + t0*Delta_v
                Dots.append(dot(Delta_x_prime, Delta_v))

        s   = std(Distances)
        fig = figure(figsize=(12,6))
        fig.suptitle(f'Number of samples: {args.N:,}')
        axs = fig.subplots(1,2)
        axs[0].hist(Distances,
                    bins=250 if args.N>9999 else 25)
        axs[0].set_xlim(-10*s, 10*s)
        axs[0].set_title(f'Deviations of centres. Standard deviation = {s:.2g}')
        axs[1].hist(Dots,
                    bins=250 if args.N>9999 else 25)
        axs[1].set_title(r'$\Delta_x\cdot\Delta_v$ for $t_{pair}=\infty$')
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
