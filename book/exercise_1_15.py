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
    Exercise 1.15. Generate 3 dimensional orthonormal coordinate systems
    with axes randomly oriented in space, using Algorithm 1.22.
    Test by computing average scalar products for pairs of random coordinate systems.
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
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('--N', type=int, default=100000, help='Number of iterations')
    return parser.parse_args()

def direct_surface(d=3,rng = np.random.default_rng(None)):
    '''
    Sample random vectors on the surface of a sphere using Algorithm 1.22

    Parameters:
        d        Dimension of sphere
        rng      Random number generator
    '''
    sigma = 1/np.sqrt(d)
    x = rng.normal(scale=sigma,size=d)
    Sigma = np.square(x).sum()
    return x/np.sqrt(Sigma)

def direct_coordinates():
    '''
    Generate 3 dimensional orthonormal coordinate systems
    with axes randomly oriented in space, using Algorithm 1.22.

    Returns:
        An array comprising:
            x0         A random unit vector
            x1prime    A unit vector, orthogonal to x0, in a plane defined by x0 and a random vector
            x2         The vector product of x0 and x1prime
    '''
    x0 = direct_surface()
    x1 = direct_surface()
    alpha = 1
    beta = -alpha*np.dot(x0,x0)/np.dot(x0,x1)
    x1prime = alpha*x0 + beta*x1
    x1prime /= np.sqrt(np.dot(x1prime,x1prime))
    return np.array([x0,x1prime,np.cross(x0,x1prime)])

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
    Products = np.zeros((args.N,3))
    for i in range(args.N):
        x = direct_coordinates()
        xprime = direct_coordinates()
        for j in range(3):
            Products[i,j] = np.dot(x[j],xprime[j])
    Average = np.average(Products,axis=0)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.hist(Products,bins=25,density=True)
    ax1.set_title(f'N={args.N}: Averages = {Average}')
    ax1.set_xlabel('Inner Product')
    ax1.set_ylabel('Frequency')
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
