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
    Exercise 2.3. Implement algorithm 2.1 (event disks) for disks in a square
    box without periodic boundary conditions. Start from a legal configuration,
    allowing restart as discussed in exercise 1.3. Generate histograms of position
    and velocity.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import create_config, get_next_pair, get_next_wall, collide_pair, get_L, Collision

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--sigma', type    = float, default = 0.125, help = 'Radius of spheres')
    parser.add_argument('-N','--N', type = int, default = 1000, help = 'Number of iterations')
    parser.add_argument('-n','--n', type = int, default = 4, help = 'Number of spheres')
    parser.add_argument('-M','--M', type = int, default = 1000, help = 'Number of attempts to create configuration')
    parser.add_argument('-L','--L', type = float, nargs = '+', default = [1], help = 'Lengths of box walls')
    parser.add_argument('-d','--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')
    parser.add_argument('--freq', type = int, default = 250, help = 'For reporting')
    parser.add_argument('--DeltaT', type = float, default = 1.0, help = 'For sampleing')
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
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    T = np.zeros((3))
    x_coordinates = np.zeros((args.N,args.n))
    L  = get_L(args.L, args.d)
    Xs,Vs = create_config(n = args.n, d = args.d, L = np.array(L), sigma = args.sigma, rng = rng, M = args.M)
    for i in range(args.N):
        t = args.DeltaT* i
        if i%args.freq == 0:
            print (f'Epoch={i:,},t={t}')
        T[Collision.SAMPLE] = args.DeltaT + t
        sampled = False
        while not sampled:
            dt_wall,wall,j = get_next_wall(Xs, Vs, sigma = args.sigma, d = args.d, L = L)
            dt_pair, k, l = get_next_pair(Xs,Vs,sigma=args.sigma)
            T[Collision.WALL] = t + dt_wall
            T[Collision.PAIR] = t + dt_pair
            match np.argmin(T):
                case Collision.WALL:
                    Xs += dt_wall * Vs
                    Vs[j][wall] = - Vs[j][wall]
                    t += dt_wall
                case Collision.PAIR:
                    Xs += dt_pair * Vs
                    Vs[k], Vs[l] = collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
                    t += dt_pair
                case Collision.SAMPLE:
                    dt = (T[2] - t)
                    Xs += dt * Vs
                    x_coordinates[i,:] = Xs[:,0]
                    sampled = True

    n,bins =np.histogram(x_coordinates)
    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args.out))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(0.5*(bins[0:-1]+bins[1:]),n/n.sum())
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
