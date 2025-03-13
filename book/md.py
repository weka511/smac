#!/usr/bin/env python

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

'''Algorithm 2.3 Pair collision'''

from argparse          import ArgumentParser
from glob              import glob
from matplotlib.pyplot import figure, hist, plot, savefig, show, title
from numpy             import argmin, dot, multiply, pi, savez, sign, sqrt
from numpy.linalg      import norm
from numpy.random      import default_rng
from os                import remove
from os.path           import basename, splitext
from matplotlib        import rc
from re                import search
from smacfiletoken     import Registry
from sys               import maxsize

WALL_COLLISION = 0
PAIR_COLLISION = 1
TOLERANCE      = 1e-12

def get_pair_time(x1, x2, v1, v2,
                  sigma = 0.01):
    '''Algorithm 2.2 Pair Time. Pair collision time for two particles'''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    Upsilon = dot(Delta_x,Delta_v)**2 - dot(Delta_v,Delta_v)*(dot(Delta_x,Delta_x)-4*sigma**2)
    return - (dot(Delta_x,Delta_v)+sqrt(Upsilon))/dot(Delta_v,Delta_v) if Upsilon>0 and dot(Delta_x,Delta_v) <0 else float('inf')

def get_wall_time(x, v,
                  sigma = 0.01,
                  d     = 2,
                  L     = [1,1]):
    '''Fig 2.3 Calculate the time for the first collision with a wall'''
    time_to_collide_with_each_wall = [(sign(v[i])*(L[i]-sigma)-x[i]) / v[i] for i in range(d)]
    assert ([abs(abs(x[i]+time_to_collide_with_each_wall[i] * v[i])-sigma)==0 for i in range(d)])
    wall  = argmin(time_to_collide_with_each_wall)
    return wall, time_to_collide_with_each_wall[wall]

def collide_pair(x1, x2, v1, v2):
    '''Algorithm 2.3 Pair collision'''
    Delta_x      = x1 - x2
    e_hat_perp   = Delta_x/norm(Delta_x)
    Delta_v      = v1 - v2
    Delta_v_perp = dot(Delta_v,e_hat_perp)
    return (v1 - Delta_v_perp*e_hat_perp, v2 + Delta_v_perp*e_hat_perp)

def event_disks(Xs, Vs,
                sigma = 0.01,
                d     = 2,
                L     = [1,1,1]):
    '''
    Algorithm 2.1: event driven molecular dynamics for particles in a box.
    Calculate time to next collision of a sphere with another sphere or
    with a wall, run time fprward until collision, then adjust velocities
    to immediately after.
    '''

    # Calculate time to next pair collision
    next_pair = (float('inf'), None, None)
    for k in range(len(Xs)):
        for l in range(k+1,len(Xs)):
            t = get_pair_time(Xs[k], Xs[l], Vs[k], Vs[l],
                              sigma = sigma)
            if t<next_pair[0]:
                next_pair=(t,k,l)

    # Calculate time to next wall collision
    next_wall = (float('inf'), None, None)
    for j in range(len(Xs)):
        wall,t = get_wall_time(Xs[j], Vs[j],
                               sigma = sigma,
                               d     = d,
                               L     = L)
        if t<next_wall[0]:
            next_wall = (t,wall,j)

    # Work out which collision is next, wall or pair
    t_wall,wall,j = next_wall
    t_pair, k, l  = next_pair

    if t_wall<t_pair:
        Xs         += t_wall * Vs     # Update to new position
        assert(abs(abs(Xs[j,wall])-(L[wall]-sigma))<TOLERANCE)
        Vs[j][wall] = - Vs[j][wall]
        return WALL_COLLISION, j, wall
    else:
        Xs += t_pair * Vs
        E_before = dot(Vs[k],Vs[k]) + dot(Vs[l],Vs[l])
        collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
        E_after = dot(Vs[k],Vs[k]) + dot(Vs[l],Vs[l])
        assert (E_before==E_after)
        return PAIR_COLLISION, k, l

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def create_rng(seed0):
    '''
    Make sure run is reproducible by displaying seed

    Parameters:
         seed0 is seed supplied by user

    Returns: Default random number generator, seedes with seed0 or newly generated seed
    If seed0 is not Mone, use it

    If seed0 is None (no seed supplied),
    generate a new seed using random number generator and print it so user can reuse.

    '''
    rng    = default_rng(seed = seed0)
    if seed0==None:
        seed = rng.integers(0,maxsize)
        print (f'Setting seed to {seed}')
        return default_rng(seed = seed),seed
    else:
        return rng,seed0

def sample(rng,
           L      = 1,
           V      = 1,
           sigma  = 0.1,
           d      = 2):
    '''Find one sample where points admissable'''
    while True:
        x1 =  2 * multiply(L, rng.random((d,))) - L
        x2 =  2 * multiply(L, rng.random((d,))) - L
        v1 = -V + 2 * V * rng.random((d,))
        v2 = -V + 2 * V * rng.random((d,))
        if dot(x1-x2,x1-x2) > 4 * sigma**2 and dot(x1 - x2,v1 - v2)<0:
            return x1,x2, v1, v2

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--action',
                        default = '2.3',
                        choices = ['2.2',
                                   '2.3'])
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
                        default = 0.01,
                        help    = 'Radius of spheres')
    parser.add_argument('--N',
                        type    = int,
                        default = 10000000,
                        help    = 'Number of iterations')
    parser.add_argument('--n',
                        type    = int,
                        default = 5,
                        help    = 'Number of hard disks')
    parser.add_argument('--M',
                        type    = int,
                        default = 1000,
                        help    = 'Number of attempts to create configuration')
    parser.add_argument('--L',
                        type    = float,
                        nargs   = '+',
                        default = [1],
                        help    = 'Lengths of box walls')
    parser.add_argument('--d',
                        type    = int,
                        default = 2,
                        choices = [2,3],
                        help    = 'Dimension of space')
    parser.add_argument('--freq',
                        type    = int,
                        default = 25,
                        help    = 'For saving configuration')
    parser.add_argument('--retention',
                        type    = int,
                        default = 3,
                        help    = 'For saving configuration')
    parser.add_argument('--save',
                        default = f'{splitext(basename(__file__))[0]}.npz',
                        help    = 'For saving configuration')

    return parser.parse_args()

def get_L(L,d):
    '''Verify that specified vector of lengths matches dimension of space. If only one value specified, replicate as needed.'''
    if len(L)==1:
        return L * d
    if len(L)==d:
        return L
    raise Exception(f'Length of L is {len(L)}: should be 1 or {d}')

def create_config(n     = 5,
                  d     = 2,
                  L     = [1,1],
                  sigma = 0.1,
                  V     = 1,
                  rng   = None,
                  M     = 25):
    Volume = 1
    VolumeDisk = pi if d==2 else 4*pi/3
    for l in L:
        Volume     *= 2*l*Volume
        VolumeDisk *= sigma
    density = n * VolumeDisk/Volume

    print (f'Trying to create configuration: n={n}, d={d}, l={L}, sigma={sigma}, density ={density:2g}')
    for _ in range(M):
        Xs     =  2 * multiply(L, rng.random((n,d))) - L
        reject = False
        for i in range(args.n):
            for j in range(i):
                reject = dot(Xs[i] - Xs[j],Xs[i] - Xs[j])< 4 * sigma**2
                if reject: break
        if not reject:
            Vs = -V + 2 * V * rng.random((n,d))
            return Xs, Vs
    raise Exception(f'Failed to create configuration in {M} attempts: n={n}, d={d}, l={L}, sigma={sigma}')

def save_configuration(file_patterns = 'md.npz',
                       epoch          = 0,
                       retention      = 3,
                       seed           = None,
                       args           = None,
                       collision_type = None,
                       k              = None,
                       l              = None):
    def get_sequence(saved_files):
        if len(saved_files)==0:
            return 1
        else:
            saved_files.sort(reverse=True)
            last_file = splitext(saved_files[0])
            digits    = search(r'\d+',last_file[0]).group(0)
            return int(digits)+1

    pattern      = splitext(file_patterns)
    saved_files  = glob(f'./{pattern[0]}[0-9]*{pattern[1]}')

    savez(f'./{pattern[0]}{get_sequence(saved_files):06d}{pattern[1]}',
          args = args,
          seed           = seed,
          epoch          = epoch,
          Xs             = Xs,
          Vs             = Vs,
          collision_type = collision_type,
          k              = k,
          l              = l)
    while len(saved_files) >= retention:
        remove(saved_files.pop())

if __name__=='__main__':
    args     = parse_arguments()
    rng,seed = create_rng(args.seed)
    L        = get_L(args.L, args.d)

    if args.action=='2.2':
        n      = 0
        Diffs  = []
        while True:
            x1, x2, v1, v2 = sample(rng,
                                    sigma = args.sigma,
                                    L     = L,
                                    d     = args.d)
            DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
            if DeltaT<float('inf'):
                n += 1
                x1_prime           = x1 + DeltaT *v1
                x2_prime           = x2 + DeltaT *v2
                v1_prime, v2_prime = collide_pair(x1_prime, x2_prime, v1, v2)
                E                  = dot(v1,v1) + dot(v2,v2)
                E_prime            = dot(v1_prime,v1_prime) + dot(v2_prime,v2_prime)
                Diffs.append((E-E_prime)/(E+E_prime))
            if n>args.N: break

        rc('font',**{'family':'serif','serif':['Palatino']})
        rc('text', usetex=True)
        figure(figsize=(12,12))
        hist(Diffs,
             bins=250 if args.N>9999 else 25)
        title (f'Discrepancy in energies for {args.N:,} trials')

    if args.action=='2.3':
        registry = Registry()
        registry.register_all("md%d.txt")
        Xs,Vs = create_config(n     = args.n,
                              d     = args.d,
                              L     = L,
                              sigma = args.sigma,
                              rng   = rng,
                              M     = args.M)
        print ('Created configuration')
        n_wall_collisions = 0
        n_pair_collisions = 0
        for epoch in range(args.N):
            if registry.is_kill_token_present(): break
            collision_type, k, l = event_disks(Xs,Vs,
                                               sigma = args.sigma,
                                               d     = args.d,
                                               L     = L)
            if collision_type==WALL_COLLISION:
                n_wall_collisions += 1
            else:
                n_pair_collisions += 1
            if epoch%args.freq==0:
                print (f'Epoch = {epoch}, Wall collisions={n_wall_collisions}, Pair collisions={n_pair_collisions} {100*n_pair_collisions/(n_pair_collisions+n_wall_collisions):.2f}%')
                save_configuration(file_patterns = args.save,
                                   epoch          = epoch,
                                   retention      = args.retention,
                                   seed           = seed,
                                   args           = args,
                                   collision_type = collision_type,
                                   k              = k,
                                   l              = l)



    # savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
