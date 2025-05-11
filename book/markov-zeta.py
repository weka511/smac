#!/usr/bin/env python
# Copyright (C) 2015-2015 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

import argparse
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib import rc

'''
    Exercise 1.21
'''
def markov_zeta(x,delta = 0.005,zeta = -0.8,rng=np.random.default_rng()):
    '''
    Algorithm 1.31
    '''
    x_bar = x + 2*delta*rng.random() - delta
    if 0 < x_bar and x_bar < 1:
        p_accept = (x_bar/x)**zeta
        if rng.random() < p_accept: x=x_bar
    return x

def parse_arguments():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-n', '--n', type=int, default=1000000,help='Number of steps for integral')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs',help='Folder for storing plot')
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

    start = time()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    xs = np.zeros((args.n,2))
    xs[0,0] = 1
    for i in range(1,args.n):
        xs[i,0] = markov_zeta(xs[i-1,0],zeta = -0.8,rng=rng)

    xs[0,1] = 1
    for i in range(1,args.n):
        xs[i,1] = markov_zeta(xs[i-1,1],zeta = -1.6,rng=rng)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,2,1)

    ax1.plot(xs[:,0])
    ax1.set_title(r'$\zeta=-0.8$')
    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(xs[:,1])
    ax2.set_title(r'$\zeta=-1.6$')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
