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

''' Template for Python programs'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show


def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--L', type = float, default = 1.0, help = 'Length of box')
    parser.add_argument('--sigma', type = float, default = 0.365, help = 'Radius of sphere')
    parser.add_argument('--N', type = int, default = 1000000, help = 'Number of steps to evolve configuration')
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

def create_config(sigma= 0.365,L=1,d=2,corners=np.array([[0,0],[0,1],[1,1],[1,0]]),rng = np.random.default_rng(),V=1):
    def acceptable(x):
        for i in range(2*d):
            if np.linalg.norm(x - corners[i,:]) < sigma:
                return False
        return True
    x = L*np.ones((d))
    while not acceptable(x):
        x = rng.random((d))

    v = 2*rng.random((d)) - 1
    return x,v/np.linalg.norm(v)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    corners = np.array([[0,0],[0,args.L],[args.L,args.L],[args.L,0]])

    x = np.zeros((args.N,2))
    for i in range(args.N):
        x[i,:],_ = create_config(args.sigma,args.L,corners=corners,rng=rng)

    fig = figure(figsize=(8,12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.scatter(x[:,0],x[:,1],s=1)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
