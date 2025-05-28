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
    box without periodic boundary conditions. Starte from a legal configuration,
    allowing restart as discussed in exercise 1.3. Generate histograms of position
    and velocity.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import create_config, event_disks, save_configuration, create_rng, get_L, Collision, reload
from smacfiletoken import Registry

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--sigma', type    = float, default = 0.01, help    = 'Radius of spheres')
    parser.add_argument('-N','--N', type = int, default = 10000000, help = 'Number of iterations')
    parser.add_argument('-n','--n', type = int, default = 5, help = 'Number of hard disks')
    parser.add_argument('-M','--M', type = int, default = 1000, help = 'Number of attempts to create configuration')
    parser.add_argument('-L','--L', type = float, nargs = '+', default = [1], help = 'Lengths of box walls')
    parser.add_argument('-d','--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')
    parser.add_argument('--freq', type = int, default = 250, help = 'For saving configuration')
    parser.add_argument('--retention', type = int, default = 3, help = 'For saving configuration')
    parser.add_argument('--save',  default = f'{splitext(basename(__file__))[0]}_.npz', help = 'For saving configuration')
    parser.add_argument('--restart', default = None, help = 'Restart from saved configuration')
    parser.add_argument('--folder',default = 'configs', help= 'Folder to store config files')
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

def evolve(Xs,Vs,n_collisions = np.zeros((2),dtype=int),
           N=0,d = 2, L = [1,1], sigma = 0.1,
           freq=5,seed=None,save='TBP',retention=0,initial_epoch=0):
    t = 0
    '''
    Allow configuration to evolve by performing a specified number of collisions,

    Parameters:
        Xs              Positions of all particles
        Vs              Velocities of all particles
        n_collisions    Vector containing number of wall collisions and pair collisions
        N               Target number of collisions
        L               Lengths of all sides
        sigma           Radius of sphere
        d               Dimension of space
        freq            Frequency for reporting and saveing configurations
        seed            Seed used when random number generator was created
        save            File name for saving configurations
        retention       Number of vesions of file that should be retained
        initial_epoch   Used when we restart to ensure epoch number is correct
        folder          Folder to store configuration files
    '''
    for epoch in range(initial_epoch,N):
        if registry.is_kill_token_present(): break
        collision_type, k, l,dt = event_disks(Xs,Vs, sigma =sigma, d = d, L = L)
        t += dt
        n_collisions[collision_type] += 1

        if epoch%freq==0:
            print (f'Epoch = {epoch}, t={t}, Wall collisions={n_collisions[Collision.WALL]},'
                   f'Pair collisions={n_collisions[Collision.PAIR]}'
                   f' {100*n_collisions[Collision.PAIR]/(n_collisions.sum()):.2f}%')
            save_configuration(file_patterns = save,
                               epoch = epoch,
                               retention = retention,
                               n_collisions = n_collisions,
                               Xs = Xs,
                               Vs = Vs,
                               d = d,
                               L =  L,
                               sigma = sigma,
                               folder = args.folder)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    registry = Registry()
    registry.register_all("md%d.txt")

    if args.restart == None:
        rng,seed = create_rng(args.seed)
        L  = get_L(args.L, args.d)
        Xs,Vs = create_config(n = args.n, d = args.d, L = L, sigma = args.sigma, rng = rng, M = args.M)
        print (f'Created configuration for {args.n} {args.d} dimensional spheres')
        evolve(Xs,Vs,N=args.N,d = args.d, L = L, save=args.save,sigma = args.sigma, freq=args.freq,seed=args.seed,retention=args.retention)
    else:
        Xs, Vs, epoch,n_collisions,d,L,sigma = reload(args.restart)
        n,d = Xs.shape
        print (f'Restart with configuration read from {args.restart}. There are {n}x{d} dimensional spheres')
        evolve(Xs,Vs,N=args.N,d = d, L = L, sigma = sigma, n_collisions=n_collisions,
               freq=args.freq,seed=args.seed,retention=args.retention,initial_epoch=epoch+1,save=args.save)

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')
