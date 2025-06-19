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
    allowing spheres to collide, and saving and restoring configurations.
'''


from glob import glob
from re import search
from os import remove
from os.path import splitext
from sys import maxsize
from unittest import TestCase, main
import numpy as np
from scipy.special import gamma

class Collision:
    '''A class for keeping track of the mechanism for a collision'''
    WALL = 0
    PAIR = 1
    SAMPLE = 2

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
        dt = - (np.dot(Delta_x,Delta_v)+np.sqrt(Upsilon))/np.dot(Delta_v,Delta_v)
        assert dt>-0
        return dt
    else:
        return float('inf')

def get_wall_time(x, v, sigma = 0.01, d = 2, L = np.array([1,1])):
    '''
        Fig 2.3 Calculate the time for the first collision of a sphere with a wall

        Parameters:
            x       Position of sphere
            v       Velocity of sphere
            sigma   Radius of sphere
            d       Dimension of space
            L       Lengths of sides
    '''
    collision_times = np.full((d),float('inf'))
    for i in range(d):
        if v[i] > 0:
            collision_times[i] = (L[i]-sigma - x[i]) / v[i]
        if v[i] < 0:
            collision_times[i] = (x[i] - sigma) / abs(v[i])

        assert collision_times[i] >= 0
    assert ([abs(abs(x[i] + collision_times[i] * v[i]) - sigma)==0 for i in range(d)])
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

    Returns:
       Velocities after collision
        '''
    Delta_x = x1 - x2
    e_hat_perp = Delta_x/np.linalg.norm(Delta_x)
    Delta_v = v1 - v2
    Delta_v_perp = np.dot(Delta_v,e_hat_perp)
    return (v1 - Delta_v_perp*e_hat_perp, v2 + Delta_v_perp*e_hat_perp)

def get_next_pair(Xs,Vs,sigma = 0.1):
    '''
    Algorithm 2.2 - calculate time to next pair collision

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

def get_next_wall(Xs, Vs, sigma = 0.1, d = 2, L = np.array([1,1])):
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
        assert t>0
        if t < next_wall[0]:
            next_wall = (t,wall,j)
    return next_wall

def event_disks(Xs, Vs, sigma = 0.01, d = 2, L = np.array([1,1]), tolerance=1e-12):
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

    Returns:
        Collision.WALL or Collision.PAIR
        Index of a sphere involved in collision
        Index of a other sphere or of wall, as appropriate
        Time to collision
    '''

    # Work out which collision is next, wall or pair
    t_wall,wall,j = get_next_wall(Xs, Vs, sigma = sigma, d = d, L = L)
    t_pair, k, l  = get_next_pair(Xs,Vs,sigma=sigma)

    if t_wall < t_pair:
        Xs += t_wall * Vs     # Update to new position
        # assert abs(abs(Xs[j,wall])-(L[wall]-sigma)) < tolerance
        Vs[j][wall] = - Vs[j][wall]
        return Collision.WALL, j, wall, t_wall
    else:
        Xs += t_pair * Vs
        E_before = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        Vs[k], Vs[l] = collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
        E_after = np.dot(Vs[k],Vs[k]) + np.dot(Vs[l],Vs[l])
        assert abs(E_before-E_after) < tolerance
        return Collision.PAIR, k, l, t_pair



def create_rng(seed0):
    '''
    Make sure run is reproducible by displaying seed

    Parameters:
         seed0 is seed supplied by user

    Returns:    Default random number generator, seeded with seed0 or newly generated seed
                If seed0 is not None, use it
                If seed0 is None (no seed supplied), generate a new seed using random number
                generator and print it so user can reuse.

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
    will collide in a positive time, which may be infinite

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
    if type(L) in [int,float]:
        return np.array([L] * d)
    match len(L):
        case 1:
            return np.array(L * d)
        case d:
            return np.array(L)

    raise Exception(f'Length of L is {len(L)}: should be 1 or {d}')


def get_volume_sphere(d=2,sigma = 0.1):
    '''
    Calculate the volume of a sphere.

    Parameters:
        d      Number of dimensions for sphers
        sigma  Radius
    '''
    return np.pi**(d/2) * (sigma ** d) / gamma(d/2+1)

def get_volume_box(d=2, L = np.array([1,1])):
    '''
    Calculate volume of a box

    Parameters:
        d      Number of dimensions for box
        sigma  Radius
    '''
    return  np.prod(get_L(L,d))

def get_density(n=5,d=2,sigma = 0.1,  L = np.array([1,1])):
    '''
    Determine the density of spheres in box

       Parameters:
        n       Number of spheres
        L       Lengths of all sides
        sigma   Radius of sphere
        d       Dimension of space

    '''
    s=  get_volume_sphere(d=d,sigma=sigma)
    b = get_volume_box(d=d,L=L)
    return n * s / b

def create_config(n = 5, d = 2,  L = np.array([1,1]), sigma = 0.1, V = 1, rng = np.random.default_rng(), M = 25, verbose=True):
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
    def any_spheres_too_close(X):
        for i in range(n):
            for j in range(i):
                if np.linalg.norm(Xs[i,:] - Xs[j,:]) < 2 * sigma: return True
        return False

    if verbose:
        print (f'Trying to create configuration: n={n}, d={d}, L={L}, sigma={sigma},'
            f' density ={get_density(n=5,d=d,sigma=sigma,L=L):2g}')
    for _ in range(M):
        Xs = sigma + rng.random((n,d)) * (L - 2*sigma)
        if not any_spheres_too_close(Xs):
            Vs = -V + 2 * V * rng.random((n,d))
            return Xs, Vs

    raise RuntimeError(f'Failed to create configuration in {M} attempts: n={n}, d={d}, l={L}, sigma={sigma}')

def get_sequence(saved_files,increment=1):
    '''
    Used to make file name unique

    Parameters:
        saved_files   A list of file names for saved configurations

    Returns:
        The sequence number for the last file, incremented by 1. If there
        are no saved files, returns 1.
    '''
    if len(saved_files)==0: return 1
    saved_files.sort(reverse=True)
    last_file = splitext(saved_files[0])
    digits = search(r'(\d+)$',last_file[0]).group(1)
    return int(digits) + increment

def get_path_to_config(file_patterns = 'md.npz',folder = 'configs',increment=1):
    pattern = splitext(file_patterns)
    saved_files = glob(f'./{pattern[0]}[0-9]*{pattern[1]}',root_dir=folder)
    return f'{folder}/{pattern[0]}{get_sequence(saved_files,increment=increment):06d}{pattern[1]}',saved_files

def save_configuration(file_patterns = 'md.npz',
                       retention = 3,
                       epoch = 0,
                       Xs = None,
                       Vs = None,
                       n_collisions = None,
                       d = 2,
                       L = np.array([1,1]),
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
    file,saved_files = get_path_to_config(file_patterns = file_patterns,folder = folder)
    np.savez(file, epoch = epoch, Xs = Xs, Vs = Vs, n_collisions = n_collisions, d = d, L =  L, sigma = sigma)

    while len(saved_files) >= retention:
        remove(f'{folder}{saved_files.pop()}')

def reload(file, folder = 'configs'):
    '''
    Reload configuration stored by save_configuration

    Parameter
        file       Name of file to load
        folder     Folder where files are stored
    '''
    if len(splitext(file)[1]) ==0:
        file = f'{file}.npz'
    full_file_name = f'{folder}/{file}' if folder != None else file
    restored = np.load(full_file_name, allow_pickle=True)
    return (restored['Xs'], restored['Vs'], restored['epoch'].astype(int),
            restored['n_collisions'],restored['d'].astype(int),restored['L'],restored['sigma'].astype(float))

class TestsForFiles(TestCase):
    '''
    Tests for saving and reloading configurations.
    '''
    def test_get_sequence(self):
        '''
        Test for Issue #79: md.save_configuration does not handle
        filename correctly if base contains digits
        '''
        self.assertEqual(4,get_sequence(['.\\exercise_2_3_000001.npz', '.\\exercise_2_3_000003.npz']))

class TestsForSpheres(TestCase):
    def test_easy_case(self):
        Xs,Vs = create_config(n = 5, d = 2,  L = np.array([1,1]), sigma = 0.1, V = 1,  M = 25, verbose=False)
        n,d = Xs.shape
        self.assertEqual(5,n)
        self.assertEqual(2,d)
        self.assertEqual(Xs.shape,Vs.shape)

    def test_too_dense(self):
        with self.assertRaises(RuntimeError) as cm:
            create_config(n = 100, d = 2,  L = np.array([1,1]), sigma = 0.1, V = 1,  M = 25, verbose=False)

class TestVolume(TestCase):
    def test_sphere2d(self):
        self.assertEqual(np.pi,get_volume_sphere(sigma=1))
        self.assertEqual(np.pi/100,get_volume_sphere(sigma=0.1))

    def test_sphere3d(self):
        self.assertAlmostEqual(4*np.pi/3000,get_volume_sphere(d=3,sigma=0.1))

    def test_sphere4d(self):
        self.assertAlmostEqual(np.pi**2/20000,get_volume_sphere(d=4,sigma=0.1))

    def test_box2d(self):
        self.assertEqual(6,get_volume_box(L=np.array([2,3])))

    def test_box3d(self):
        self.assertEqual(30,get_volume_box(d=3,L=np.array([2,3,5])))

    def test_box3simple(self):
        self.assertEqual(8,get_volume_box(d=3,L=2))


if __name__=='__main__':
    main()
