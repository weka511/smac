#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Pty Ltd

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

'''Algorithm 1.32 levy convolution'''

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
    parser.add_argument('-N', '--N', type=int, default=10, help='Number of iterations')
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


def levy_convolution(pi,A_Plus=1.25,alpha=1.25):
    '''
    Algorithm 1.32 levy convolution
    Parameters:
        pi
        A_Plus
        alpha
    '''

    x0,_ = pi[0]
    xK,_ = pi[-1]
    K    = len(pi)
    Delta = (xK-x0)/(K-1)
    for k in range(K):
        x = x0 + (K + k) * Delta
        pik = A_Plus/x**(1+alpha)
        pi.append((x,pik))
    pi_dash=[]
    for k in range(0,2*K):
        x = (pi[0][0]+pi[k][0])/(2**(1/alpha))
        pi_x = Delta * sum([pi[i][1]*pi[k-i][1] for i in range(k)])/2**(1/alpha)
        pi_dash.append((x,pi_x))
    norm = sum([p for (_,p) in pi_dash])
    return [(x,p/norm) for (x,p) in pi_dash if x>= x0 and x0 <= xK]

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    pi = [(x/10,0.1) for x in range(11)]
    ax1.plot([x for (x,_) in pi],[p for (_,p) in pi],label=f'{0}')
    for i in range(args.N):
        pi = levy_convolution(pi)
        ax1.plot([x for (x,_) in pi],[p for (_,p) in pi],label=f'{i+1}')
    ax1.legend()
    ax1.set_xlabel('$x$')
    ax1.set_ylabel(r'$\pi(x)$')

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
