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

'''Exercise 2.3'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import create_config, event_disks, save_configuration, create_rng, get_L, WALL_COLLISION, PAIR_COLLISION
from smacfiletoken import Registry

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--sigma', type    = float, default = 0.01, help    = 'Radius of spheres')
    parser.add_argument('--N', type = int, default = 10000000, help = 'Number of iterations')
    parser.add_argument('--n', type = int, default = 5, help = 'Number of hard disks')
    parser.add_argument('--M', type = int, default = 1000, help = 'Number of attempts to create configuration')
    parser.add_argument('--L', type = float, nargs = '+', default = [1], help = 'Lengths of box walls')
    parser.add_argument('--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')
    parser.add_argument('--freq', type = int, default = 250, help = 'For saving configuration')
    parser.add_argument('--retention', type = int, default = 3, help = 'For saving configuration')
    parser.add_argument('--save',  default = f'{splitext(basename(__file__))[0]}_.npz', help = 'For saving configuration')

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
    rng,seed = create_rng(args.seed)
    L  = get_L(args.L, args.d)

    registry = Registry()
    registry.register_all("md%d.txt")
    Xs,Vs = create_config(n = args.n, d = args.d, L = L, sigma = args.sigma, rng = rng, M = args.M)
    print ('Created configuration')
    n_collisions = np.zeros((2),dtype=int)
    for epoch in range(args.N):
        if registry.is_kill_token_present(): break
        collision_type, k, l = event_disks(Xs,Vs, sigma = args.sigma, d = args.d, L = L)
        n_collisions[collision_type] += 1

        if epoch%args.freq==0:
            print (f'Epoch = {epoch}, Wall collisions={n_collisions[WALL_COLLISION]},'
                   f'Pair collisions={n_collisions[PAIR_COLLISION]}'
                   f' {100*n_collisions[PAIR_COLLISION]/(n_collisions.sum()):.2f}%')
            save_configuration(file_patterns = args.save,
                               epoch = epoch,
                               retention = args.retention,
                               seed = seed,
                               args = args,
                               collision_type = collision_type,
                               Xs = Xs,
                               Vs = Vs,
                               k = k,
                               l = l)

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')


