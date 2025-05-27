#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License a s published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

'''
    This module comprises functions for creating configurations,
    allowing spheres to collide, and save and restore configurations.
'''


from glob import glob
from re import search
from os import remove
from os.path import splitext
from sys import maxsize
from unittest import TestCase, main
import numpy as np

class Collision:
    '''A class for keeping track of the mechanism for a collision'''
    WALL = 0
    PAIR = 1

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
        return Collision.WALL, j, wall
    else:
        Xs += t_pair * Vs
        E_before = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
        E_after = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        assert E_before==E_after
        return Collision.PAIR, k, l



def create_rng(seed0):
    '''
    Make sure run is reproducible by displaying seed

    Parameters:
         seed0 is seed supplied by user

    Returns: Default random number generator, seeded with seed0 or newly generated seed
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

def find_admissable_pair(L = 1, V = 1, sigma = 0.1, d = 2, rng=np.random.default_rng()):
    '''
    Find a pair of spheres which don't overlap, and are moving so that they
    will collide in a positive time, which may beinfinite

    Parameters:
        L       Lengths of all sides
        V       Limiting velocity: we aim for velocities to be in range (-V,V)
        sigma   Radius of sphere
        d       Dimension of space

    Returns: x1, x2, v1, v2, where
        x1      Centre of one sphere
        x2      Centre of the other sphere
        v1      Velocity of one sphere
        v2      Velocity of the other sphere,

    '''
    while True:
        x1 =  2 * np.multiply(L, rng.random((d,))) - L
        x2 =  2 * np.multiply(L, rng.random((d,))) - L
        v1 = -V + 2 * V * rng.random((d,))
        v2 = -V + 2 * V * rng.random((d,))
        if np.dot(x1-x2,x1-x2) > 4 * sigma**2 and np.dot(x1 - x2,v1 - v2) < 0:
            return x1,x2,v1,v2


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

def get_density(n=5,d=2,sigma = 0.1, L = [1,1]):
    '''
    Determine the density of spheres in box

       Parameters:
        n       Number of spheres
        L       Lengths of all sides
        sigma   Radius of sphere
        d       Dimension of space

    '''
    VolumeBox = 1
    VolumeDisk = np.pi if d==2 else 4*np.pi/3
    for l in L:
        VolumeBox *= (2*l*VolumeBox)
        VolumeDisk *= sigma
    return n * VolumeDisk/VolumeBox

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
        M       Number of attempts allowed to create configuration
    '''

    print (f'Trying to create configuration: n={n}, d={d}, L={L}, sigma={sigma},'
           f' density ={get_density(n=5,d=d,sigma=sigma,L=L):2g}')
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
                       retention = 3,
                       epoch = 0,
                       Xs = None,
                       Vs = None,
                       n_collisions = None,
                       d = 2,
                       L =  [1,1],
                       sigma = 0.05,
                       folder = 'configs'):
    '''
    Save configuration of disks

    Parameters:
        file_patterns   Underlying pattern for file names (extended with generation number)
        epoch           Current epoch (total number of all collisions)
        retention       Number of vesions of file that should be retained
        Xs              Positions of all particlesenerator
        Vs              Velocities of all particles
        seed            Seed used when random number generator was created
        n_collisions    Vector containing number of wall collisions and pair collisions
        L               Lengths of all sides
        sigma           Radius of sphere
        d               Dimension of space
        folder          Folder to store files
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
    saved_files = glob(f'./{pattern[0]}[0-9]*{pattern[1]}',root_dir=folder)

    np.savez(f'{folder}/{pattern[0]}{get_sequence(saved_files):06d}{pattern[1]}',
          epoch = epoch,
          Xs = Xs,
          Vs = Vs,
          n_collisions = n_collisions,
          d = d,
          L =  L,
          sigma = sigma)

    while len(saved_files) >= retention:
        remove(f'{folder}{saved_files.pop()}')

def reload(file, folder = 'configs'):
    '''
    Reload configuration stored by save_configuration

    Parameters:
        file       Name of file to load
        folder     Folder where files are stored
    '''
    if len(splitext(file)[1]) ==0:
        file = f'{file}.npz'
    restored = np.load(f'{folder}/{file}', allow_pickle=True)
    return (restored['Xs'], restored['Vs'], restored['epoch'].astype(int),
            restored['n_collisions'],restored['d'].astype(int),restored['L'],restored['sigma'].astype(float))

if __name__=='__main__':
    main()
