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

'''Exercise 1.6: implement Alg 1.4 direct needle and Alg 1.5 direct-needle(patch).'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def direct_needle(N=10000,a=1.0,b=2.0,rng=np.random.default_rng(None)):
    n_hits = 0
    for _ in range(N):
        x0 = rng.uniform(0,b/2)
        phi = rng.uniform(0,np.pi/2)
        x1 = x0 - (a/2)*np.cos(phi)
        if x1 < 0:
            n_hits += 1
    return n_hits

def direct_needle_patch(N=10000,a=1.0,b=2.0,rng=np.random.default_rng(None)):
    def direct_needle_one_step():
        x0 = rng.uniform(0,b/2)
        Upsilon = 2
        while Upsilon > 1:
            Delta_x = rng.uniform(0,1)
            Delta_y = rng.uniform(0,1)
            Upsilon = np.sqrt(Delta_x**2 + Delta_y**2)
        x1 = x0 - (a/2) * Delta_x/Upsilon
        return 1 if x1 < 0 else 0
    N_hits = 0
    for _ in range(N):
        N_hits += direct_needle_one_step()
    return N_hits



def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
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
    x = direct_needle(N=1000000)
    y = direct_needle_patch(N=1000000)
    z=0
    # rc('font',**{'family':'serif','serif':['Palatino']})
    # rc('text', usetex=True)
    # start  = time()
    # args = parse_arguments()
    # rng = np.random.default_rng(args.seed)
    # fig = figure(figsize=(12,12))

    # fig.savefig(get_file_name(args.out))
    # elapsed = time() - start
    # minutes = int(elapsed/60)
    # seconds = elapsed - 60*minutes
    # print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    # if args.show:
        # show()
