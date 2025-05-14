#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Limited

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

'''Exercise 1.18 and Algorithm 1.25 from Krauth'''

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
    parser.add_argument('--theta',type=float,default = np.pi/4)
    parser.add_argument('--N',type=int,default = 1000)
    parser.add_argument('--M',type=int,default = 100000)
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


def binomial_convolution(theta = np.pi/4,N=9):
    '''Algorithm 1.25 from Krauth'''
    P = np.full((N,N),np.nan)   # P[N,k] - k hits in N trials
    P[0,0] = 1
    for n in range(1,N):
        P[n,0] = (1-theta) * P[n-1,0]
        for k in range(1,n):
            P[n,k] = (1-theta) * P[n-1,k] +  theta* P[n-1,k-1]
        P[n,n] = theta * P[n-1,n-1]

    return P

def direct_pi(M):
    n_hits = 0
    for i in range(args.M):
        x,y = rng.uniform(-1,1,2)
        if x**2 + y**2 < 1:
            n_hits += 1
    return n_hits

if __name__=='__main__':

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)


    direct_pi(args.M)
    P = binomial_convolution(theta = args.theta,N=args.N)
    ax.plot(P[-1,:])

    fig.savefig(get_file_name(args.out))
    show()
