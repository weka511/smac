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
    Exercise 2.2/Algorithm 2.3 (pair collision). Verify that energy
    and momentum are both conserved in a collision.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import find_admissable_pair, get_pair_time, collide_pair, create_rng, get_L

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--seed', type = int, default = None, help = 'Seed for random number generator')
    parser.add_argument('--sigma', type    = float, default = 0.01, help    = 'Radius of spheres')
    parser.add_argument('--N', type = int, default = 10000000, help = 'Number of iterations')
    parser.add_argument('--L', type = float, nargs = '+', default = [1], help = 'Lengths of box walls')
    parser.add_argument('--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')
    parser.add_argument('--freq', type = int, default = 1000, help = 'Used to report progress')

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


def create_diffs(N,sigma=0.1,L=[1,1],d=2):
    '''
    Sample a number of collisions and compare the energies before
    and after each collision.

    Parameters:
        N       Number of collisions
        sigma   Radius of each sphere
        d       Dimension of space
        L       Lengths of sides

    Returns:
        A tuple of two arrays
            Energies  The difference in energy before and after a collision, divided by energy before
            Momenta   The difference in momentum before and after a collision, divided by norm of momentum before

    '''
    n = 0
    Energies = np.empty((args.N))
    Momenta = np.zeros((2,args.N))
    while n < args.N:
        x1, x2, v1, v2 = find_admissable_pair(sigma =sigma, L = L, d = d)
        DeltaT = get_pair_time(x1,x2,v1,v2,sigma = sigma)
        if DeltaT < float('inf'): # i.e. if the spheres will ever collide
            x1_prime = x1 + DeltaT*v1
            x2_prime = x2 + DeltaT*v2
            v1_prime, v2_prime = collide_pair(x1_prime, x2_prime, v1, v2)
            E_before = np.dot(v1,v1) + np.dot(v2,v2)
            E_after = np.dot(v1_prime,v1_prime) + np.dot(v2_prime,v2_prime)
            P_before = v1 + v2
            P_after = v1_prime + v2_prime
            Momenta[:,n] = (P_before - P_after)/np.linalg.norm(P_before)
            Energies[n] = (E_before-E_after)/E_before
            n += 1
            if n%args.freq ==0:
                print (f'Collided {n} times out of {args.N}')

    return Energies,Momenta.reshape(-1)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start = time()
    args = parse_arguments()
    rng,seed = create_rng(args.seed)
    L  = get_L(args.L, args.d)
    Energies,Momenta = create_diffs(args.N,sigma = args.sigma, L  = L, d = args.d)
    fig = figure(figsize=(12,12))
    fig.suptitle(fr'Exercise 2.2:  {args.N:,} trials, $\sigma=$ {args.sigma}, L={L}, d={args.d}')
    ax1 = fig.add_subplot(1,2,1)
    ax1.hist(Energies,bins='doane', color='blue',density=True)
    ax1.set_title (fr'Discrepancy in energies')

    ax2 = fig.add_subplot(1,2,2)
    ax2.hist(Momenta,bins='doane', color='blue',density=True)
    ax2.set_title (f'Discrepancy in momenta')

    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()

