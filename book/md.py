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

'''Algorithm 2.3 Pair collision'''

from argparse import ArgumentParser
from glob import glob
from re import search
from os import remove
from os.path import basename, join, splitext
from sys import maxsize
from time import time
from matplotlib import rc
from matplotlib.pyplot import figure, show
import numpy as np
from smacfiletoken import Registry

# Constants used to distinguish the two types of collisions

WALL_COLLISION = 0
PAIR_COLLISION = 1

def get_pair_time(x1, x2, v1, v2, sigma = 0.01):
    '''
    Algorithm 2.2 Pair Time. Pair collision time for two spheres

    Parameters:
        x1         Centre of one sphere
        x2         Centre of the other sphere
        v1         Velocity of one sphere
        v2         Velocity of the other sphere
        sigma      Radius of sphere

    Returns:
        The time at which two spheres will collide: may be np.inf
    '''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    Upsilon = np.dot(Delta_x,Delta_v)**2 - np.dot(Delta_v,Delta_v) * (np.dot(Delta_x,Delta_x) - 4*sigma**2)
    if Upsilon > 0 and np.dot(Delta_x,Delta_v)  < 0 :
        return - (np.dot(Delta_x,Delta_v)+np.sqrt(Upsilon))/np.dot(Delta_v,Delta_v)
    else:
        return float('inf')

def get_wall_time(x, v, sigma = 0.01, d = 2, L = [1,1]):
    '''
        Fig 2.3 Calculate the time for the first collision of a sphere with a wall

        Parameters:
            x       Position of sphere
            v       Velocity of sphere
            sigma   Radius of sphere
            d       Dimension of space
            L       Lengths of sides
        '''
    collision_times = [(np.sign(v[i])*(L[i]-sigma)-x[i]) / v[i] for i in range(d)]
    assert ([abs(abs(x[i]+collision_times[i] * v[i])-sigma)==0 for i in range(d)])
    wall  = np.argmin(collision_times)
    return wall, collision_times[wall]

def collide_pair(x1, x2, v1, v2):
    '''
        Algorithm 2.3 Pair collision

        Parameters:
        x1         Centre of one sphere
        x2         Centre of the other sphere
        v1         Velocity of one sphere
        v2         Velocity of the other sphere
        '''
    Delta_x = x1 - x2
    e_hat_perp = Delta_x/np.linalg.norm(Delta_x)
    Delta_v = v1 - v2
    Delta_v_perp = np.dot(Delta_v,e_hat_perp)
    return (v1 - Delta_v_perp*e_hat_perp, v2 + Delta_v_perp*e_hat_perp)

def event_disks(Xs, Vs, sigma = 0.01, d = 2, L = [1,1,1], tolerance=1e-15):
    '''
    Algorithm 2.1: event driven molecular dynamics for particles in a box.
    Calculate time to next collision of a sphere with another sphere or
    with a wall, run time forward until collision, then adjust velocities
    to immediately after.

    Parameters:
        Xs        Centres of all spheres
        Vs        Velocities of all spheres
        sigma     Radius of sphere spheres
        d         Dimension of space
        L         Lengths of sides
        tolerance Used in a wall collision to verify updated position is close to wall
    '''

    def get_next_pair():
        '''
        Calculate time to next pair collision

        Returns:
           t_pair   Time to next pair collision
           k        Index of one sphere
           l        Index of the other sphere: k < l
        '''
        next_pair = (float('inf'), None, None)
        for k in range(len(Xs)):
            for l in range(k+1,len(Xs)):
                t = get_pair_time(Xs[k], Xs[l], Vs[k], Vs[l],sigma = sigma)
                if t < next_pair[0]:
                    next_pair = (t,k,l)
        return next_pair

    def get_next_wall():
        '''
        Calculate time to next wall collision

        Returns:
            t_wall   Time to next wall collision
            wall     Index of wall
            j        Index of sphere
        '''
        next_wall = (float('inf'), None, None)
        for j in range(len(Xs)):
            wall,t = get_wall_time(Xs[j], Vs[j], sigma = sigma, d = d, L = L)
            if t < next_wall[0]:
                next_wall = (t,wall,j)
        return next_wall

    # Work out which collision is next, wall or pair
    t_wall,wall,j = get_next_wall()
    t_pair, k, l  = get_next_pair()

    if t_wall < t_pair:
        Xs += t_wall * Vs     # Update to new position
        assert abs(abs(Xs[j,wall])-(L[wall]-sigma)) < tolerance
        Vs[j][wall] = - Vs[j][wall]
        return WALL_COLLISION, j, wall
    else:
        Xs += t_pair * Vs
        E_before = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
        E_after = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        assert E_before==E_after
        return PAIR_COLLISION, k, l

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

def create_rng(seed0):
    '''
    Make sure run is reproducible by displaying seed

    Parameters:
         seed0 is seed supplied by user

    Returns: Default random number generator, seedes with seed0 or newly generated seed
    If seed0 is not None, use it

    If seed0 is None (no seed supplied),
    generate a new seed using random number generator and print it so user can reuse.

    '''
    rng = np.random.default_rng(seed=seed0)
    if seed0 == None:
        seed = rng.integers(0,maxsize)
        print (f'Setting seed to {seed}')
        return np.random.default_rng(seed = seed),seed
    else:
        return rng,seed0

def sample(L = 1, V = 1, sigma = 0.1, d = 2, rng=np.random.default_rng()):
    '''
    Find one sample where points admissable

    Parameters:
        L       Lengths of all sides
        V       Limiting velocity: we aim for velocities to be in range (-V,V)
        sigma   Radius of sphere
        d       Dimension of space

    Returns: x1, x2, v1, v2, where
        x1      Centre of one sphere
        x2      Centre of the other sphere
        v1      Velocity of one sphere
        v2      Velocity of the other sphere, and
                the spheres are moving so that they will collide in a positive
                time, which may be np.inf

    '''
    while True:
        x1 =  2 * np.multiply(L, rng.random((d,))) - L
        x2 =  2 * np.multiply(L, rng.random((d,))) - L
        v1 = -V + 2 * V * rng.random((d,))
        v2 = -V + 2 * V * rng.random((d,))
        if np.dot(x1-x2,x1-x2) > 4 * sigma**2 and np.dot(x1 - x2,v1 - v2) < 0:
            return x1,x2,v1,v2

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--seed', type = int, default = None, help = 'Seed for random number generator')
    parser.add_argument('--sigma', type    = float, default = 0.01, help    = 'Radius of spheres')
    parser.add_argument('--N', type = int, default = 10000000, help = 'Number of iterations')
    parser.add_argument('--n', type = int, default = 5, help = 'Number of hard disks')
    parser.add_argument('--M', type = int, default = 1000, help = 'Number of attempts to create configuration')
    parser.add_argument('--L', type = float, nargs = '+', default = [1], help = 'Lengths of box walls')
    parser.add_argument('--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')

    return parser.parse_args()

def get_L(L,d):
    '''
    Verify that specified vector of lengths matches dimension of space.
    If only one value specified, replicate as needed.

    Parameters:
        L       Vector representing walls of a box
        d       Dimension of space
    '''
    match len(L):
        case 1:
            return L * d
        case d:
            return L

    raise Exception(f'Length of L is {len(L)}: should be 1 or {d}')

def create_config(n = 5, d = 2, L = [1,1], sigma = 0.1, V = 1, rng = None, M = 25):
    '''
    Create a configuration of disks or spheres, no two of which overlap

    Parameters:
        n       Number of spheres
        L       Lengths of all sides
        V       Limiting velocity: we aim for velocities to be in range (-V,V)
        sigma   Radius of sphere
        d       Dimension of space
        rng     Random number generator
        M       Number of attempt allowed to create configuration
    '''
    Volume = 1
    VolumeDisk = np.pi if d==2 else 4*np.pi/3
    for l in L:
        Volume *= (2*l*Volume)
        VolumeDisk *= sigma
    density = n * VolumeDisk/Volume

    print (f'Trying to create configuration: n={n}, d={d}, l={L}, sigma={sigma}, density ={density:2g}')
    for _ in range(M):
        Xs =  2 * np.multiply(L, rng.random((n,d))) - L
        reject = False
        for i in range(n):
            for j in range(i):
                reject = np.dot(Xs[i] - Xs[j],Xs[i] - Xs[j])< 4 * sigma**2
                if reject: break
        if not reject:
            Vs = -V + 2 * V * rng.random((n,d))
            return Xs, Vs

    raise RuntimeError(f'Failed to create configuration in {M} attempts: n={n}, d={d}, l={L}, sigma={sigma}')

def save_configuration(file_patterns = 'md.npz',
                       epoch = 0,
                       retention = 3,
                       seed = None,
                       args = None,
                       Xs = None,
                       Vs = None,
                       collision_type = None,
                       k = None,
                       l = None):
    '''
    Save configuration of disks

    Parameters:
        file_patterns
        epoch
        retention
        seed
        args
        collision_type
        k
        l
    '''
    def get_sequence(saved_files):
        '''
        Used to make file name unique
        '''
        if len(saved_files)==0: return 1
        saved_files.sort(reverse=True)
        last_file = splitext(saved_files[0])
        digits = search(r'\d+',last_file[0]).group(0)
        return int(digits) + 1

    pattern = splitext(file_patterns)
    saved_files = glob(f'./{pattern[0]}[0-9]*{pattern[1]}')

    np.savez(f'./{pattern[0]}{get_sequence(saved_files):06d}{pattern[1]}',
          args = args,
          seed = seed,
          epoch = epoch,
          Xs = Xs,
          Vs = Vs,
          collision_type = collision_type,
          k = k,
          l = l)

    while len(saved_files) >= retention:
        remove(saved_files.pop())

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start = time()
    args = parse_arguments()
    rng,seed = create_rng(args.seed)
    L  = get_L(args.L, args.d)
    n = 0
    Diffs = np.empty((args.N))
    while True and n < args.N:
        x1, x2, v1, v2 = sample(sigma = args.sigma, L = L, d = args.d)
        DeltaT = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
        if DeltaT < float('inf'):
            x1_prime = x1 + DeltaT*v1
            x2_prime = x2 + DeltaT*v2
            v1_prime, v2_prime = collide_pair(x1_prime, x2_prime, v1, v2)
            E = np.dot(v1,v1) + np.dot(v2,v2)
            E_prime = np.dot(v1_prime,v1_prime) + np.dot(v2_prime,v2_prime)
            Diffs[n] = (E-E_prime)/(E+E_prime)
            n += 1

    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    ax.hist(Diffs, bins=250 if args.N>9999 else 25, color='blue')
    ax.set_title (f'Discrepancy in energies for {args.N:,} trials')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
