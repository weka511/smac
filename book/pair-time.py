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

'''
    Exercise 2.1: Implement algorithm 2.2 (pair-time) and incorporate it into a test program
    generating 2 random positions with abs(delta_x) > 2 sigma. Propagate both disks up to t_pair
    if finite and verify that they touch, otherwise verify that delta_x.delta_v = 0.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
from matplotlib import rc
from matplotlib.pyplot import figure, show
import numpy as np
from md import get_pair_time, sample

def get_time_of_closest_approach(x1, x2, v1, v2):
    '''
    Calculate the time of closest approach for the centres of two spheres

    Parameters:
        x1         Centre of one sphere
        x2         Centre of the other sphere
        v1         Velocity of one sphere
        v2         Velocity of the other sphere

    Returns:
        The time at which the relative velocity is minimized
    '''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    return - np.dot(Delta_v,Delta_x)/np.dot(Delta_v,Delta_v)

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


def parse_arguments():
    '''
    Parse command line arguments
    '''
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--action', default = 'run', choices = ['test', 'run'],
                        help='''
                                Default value (run) performs as described above. Set to "test" instead
                                to propagte one pair of disks and show starting and final configurations.
                            ''')
    parser.add_argument('--d', type = int, default = 2, choices = [2,3], help    = 'Dimension of space')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--seed', type = int,  default = None, help = 'Seed for random number generator')
    parser.add_argument('--sigma', type    = float, default = 0.1, help = 'Radius of spheres')
    parser.add_argument('--N', type = int, default = 10000000,  help = 'Number of iterations')

    return parser.parse_args()

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start = time()
    args = parse_arguments()
    L = [1] * args.d
    rng = np.random.default_rng(args.seed)

    match args.action:
        case 'run':
            Distances = np.empty((args.N))
            N_Distances = 0
            Dots = np.empty((args.N))
            N_Dots = 0
            for _ in range(args.N):
                x1, x2, v1, v2 = sample(sigma=args.sigma, L=L, rng=rng)
                DeltaT = get_pair_time(x1,x2,v1,v2,sigma=args.sigma)
                if DeltaT < float('inf'): # Find distance between spheres when they touch (expert zero)
                    x1_prime = x1 + DeltaT *v1
                    x2_prime = x2 + DeltaT *v2
                    Distances[N_Distances] = (np.linalg.norm(x1_prime-x2_prime)-2*args.sigma)/2*args.sigma
                    N_Distances += 1
                else: # calculate delta_x.delta_v at closest approach
                    t0 = get_time_of_closest_approach(x1,x2,v1,v2)
                    if t0 > 0:
                        Delta_x = x1 - x2
                        Delta_v = v1 - v2
                        Delta_x_prime = Delta_x + t0*Delta_v
                        Dots[N_Dots] = np.dot(Delta_x_prime, Delta_v)
                        N_Dots += 1

            std  = np.std(Distances[0:N_Distances])

            fig = figure(figsize=(12,6))
            fig.suptitle(f'Exercise 2.1. Number of samples: {args.N:,}')
            ax1 = fig.add_subplot(1,2,1)
            ax2 = fig.add_subplot(1,2,2)
            ax1.hist(Distances[0:N_Distances], bins=250 if args.N>9999 else 25, color='b')
            ax1.set_xlim(-10*std, 10*std)
            ax1.set_title('Deviations of centres at $t=t_{pair}$.'f'\nStandard deviation = {std:.2g}, from {N_Distances:,} collisions')
            ax2.hist(Dots[0:N_Dots], bins = 250 if args.N > 9999 else 25, color='b')
            ax2.set_title(r'$\Delta_x\cdot\Delta_v$ for $t_{pair}=\infty$'f'\nStandard deviation = {np.std(Dots[0:N_Dots]):.2g} from {N_Dots:,} approaches')

        case 'test':
            for _ in range(1000):
                x1, x2, v1, v2 = sample(sigma = args.sigma, L = L,rng=rng)
                DeltaT = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
                print (DeltaT)
                if DeltaT<float('inf'): break

            x1_prime = x1 + DeltaT *v1
            x2_prime = x2 + DeltaT *v2
            distance = np.linalg.norm(x1_prime-x2_prime)
            print (2*args.sigma, distance, abs(2*args.sigma-distance)/2*args.sigma)

            fig = figure(figsize=(10,10))
            ax = fig.add_subplot(111)
            ax.axis([-L[0],  L[0], -L[1], L[1]])
            r_display_coordinates = ax.transData.transform([args.sigma,0])[0] - ax.transData.transform([0,0])[0] # https://stackoverflow.com/questions/65174418/how-to-adjust-the-marker-size-of-a-scatter-plot-so-that-it-matches-a-given-radi
            marker_size  = 0.5*(2*r_display_coordinates)**2 # fudge factor
            ax.scatter(x1[0],x1[1],label='x1',s=marker_size)
            ax.scatter(x2[0],x2[1],label='x2',s=marker_size)
            ax.arrow(x1[0],x1[1],0.25*DeltaT*v1[0],0.25*DeltaT*v1[1],head_width=0.0125)
            ax.arrow(x2[0],x2[1],0.25*DeltaT*v2[0],0.25*DeltaT*v2[1],head_width=0.0125)

            ax.scatter(x1_prime[0],x1_prime[1],label='x1"',s=marker_size)
            ax.scatter(x2_prime[0],x2_prime[1],label='x2"',s=marker_size)
            ax.grid()

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
