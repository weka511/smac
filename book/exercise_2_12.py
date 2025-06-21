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
    Sample the gamma distribution using the naive algorithm contained in Algorithm 2.13.
    Likewise implement Algorithm 2.15, gamma-cut.
'''

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
    parser.add_argument('--NTrials', type=int, default=100000, help='Number of trials for histogram')
    parser.add_argument('--N', type=int, default=5,help='Maximum number of particles for histogram')
    return parser.parse_args()

def get_piston_particles(N=12,beta=1,P=1,rng = np.random.default_rng()):
    '''
     Direct sampling of one-dimensional point particles
     and a piston at pressure P

    Parameters:
        N       Number of particles
        beta    Inverse temperature
        P       Pressure
        rng     Random number generator

    Returns:
        L       Variable to be sampled
        alpha   Positions of particles
    '''
    Upsilon = rng.random()
    alpha = rng.random((N))
    for k in range(N):
        Upsilon *= rng.random()
    L = - np.log(Upsilon)/(beta*P)
    return L,alpha * L

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
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)

    for n in range(args.N):
        L = np.zeros((args. NTrials))
        for i in range(args. NTrials):
            L[i],_ = get_piston_particles(N=n,rng = rng)
        freq,bins = np.histogram(L,bins=12,density=True)
        ax1.plot(0.5*(bins[1:] + bins[:-1]),freq,label=f'{n}')

    ax1.legend(title='N')
    ax1.set_title(r'Sampling the $\Gamma$ distribution using direct-piston-particles')
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
