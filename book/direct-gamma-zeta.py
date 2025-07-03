#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''
    Implement Algorithm 1.30: using importance sampling to compute the gamma integral.
'''
import argparse
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib import rc

def direct_gamma_zeta(gamma,zeta,n, rng=np.random.default_rng()):
    '''
    Algorithm 1.30: using importance sampling to compute the gamma integral

    Parameters:
        gamma
        zeta
        n
        rn
    '''
    def get_positive_sample():
        '''
        Used to compute random numbers in the open interval (0.0,1.0),
        i.e. exclude zero.
        '''
        while True:
            x = rng.random()
            if x > 0: return x

    sigma_x = 0
    sigma2 = 0
    for i in range(n):
        x = get_positive_sample()
        x1 = x ** (1/(1+zeta))
        x2 = x1 ** (gamma - zeta)
        sigma_x += x2
        sigma2 += x2**2

    mean = sigma_x/n
    return (mean,np.sqrt(sigma2/n-mean*mean)/np.sqrt(n))

def parse_arguments():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-n', '--n', type=int, default=1000,help='Number of steps for integral')
    parser.add_argument('--gammas', type=float, default= [2.0,1.0,0.0,-0.1,-0.4,-0.8], nargs='+')
    parser.add_argument('--zetas', type=float, default= [0.0, -0.1, -0.7, -0.8], nargs='+')
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

if __name__=="__main__":
    start = time()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    fig = figure(figsize=(12,12))
    fig.suptitle(f'n={args.n:,}')
    for i,zeta in enumerate(args.zetas):
        ax=fig.add_subplot(2,2,i+1)
        y = np.zeros((len(args.gammas),3))
        for j in range(len(args.gammas)):
            (s,t) = direct_gamma_zeta(args.gammas[j],zeta,args.n,rng=rng)
            y[j,0] = s - t
            y[j,1] = s + t
            y[j,2] = (zeta+1)/(args.gammas[j]+1)
        ax.plot(args.gammas,y[:,0],label='Lower bound')
        ax.plot(args.gammas,y[:,1],label='Upper bound')
        ax.plot(args.gammas,y[:,2],label='Estimate')
        ax.set_xlabel(r'$\gamma$')
        ax.legend(title=r'$\zeta=$'f'{zeta}')

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()

