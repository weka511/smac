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
    Exercise 1-13: generate uniformly distributed vectors inside sphere,
    then augment with an additional component in the range (-1,+1), and reject if length exceeds 1.
    Use to estimate ratios of volumes.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.special import gamma


def parse_arguments():
    '''
    Parse command line arguments
    '''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N', '--N', type=int, default=1000)
    parser.add_argument('-d', '--d', type=int, default=[3,30],nargs=2)
    return parser.parse_args()

def direct_sphere(d=3,radius=1.0,rng = np.random.default_rng()):
    '''
    Algorithm 1.21: generate a uniform random vector inside a sphere

    Parameters:
        d         Dimension of sphere
        radius    Radius of sphere
        rng       Random number generator
    '''
    X = rng.normal(scale=radius,size=d)
    Sigma = np.sum(X*X)
    Upsilon = rng.random()**(1/d)
    return Upsilon*X/np.sqrt(Sigma)

def estimate_ratio(d=3,N=1000,rng = np.random.default_rng()):
    '''
    Exercise 1-13: generate uniformly distributed vectors inside sphere,
    then augment with an additional component in the range (-1,+1), and reject if length exceeds 1.

    Parameters:
        d       Dimension of initial sphere (final is d+1)
        N       Number of dimensions
        rng     Random number generator
    '''
    accepted = 0

    for _ in range(N):
        X = np.zeros(d+1)
        X[0:d] = direct_sphere(d=d,rng=rng)
        X[d] = 2*rng.random() - 1
        if np.sum(X*X) < 1:
            accepted += 1

    return 2 * accepted/N # We need to compare with 2R, not R - e.g. Figure 1.5

def get_V(d):
    '''
    Calculate volume of a unit sphere after Equation 1.39

    Parameters:
        d   Dimension of sphere
    '''
    return (np.pi**(d/2))/gamma(d/2+1)

def get_ratio(d=4):
    '''
    Equation 1.42: ratio of volume of d dimensional sphere to (d-2)

    Parameters:
        d   Dimension of final sphere
    '''
    return np.pi/(d/2)

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

    r501 = estimate_ratio(d=500,N=args.N,rng=rng)
    r502 = estimate_ratio(d=501,N=args.N,rng=rng)
    # print (r502, r501, r502*r501,  2*np.pi/502)

    Ds = np.linspace(args.d[0],args.d[1],num=args.d[1]-args.d[0]+1)
    Estimated = np.vectorize(lambda d:estimate_ratio(d=int(d),N=args.N,rng=rng))(Ds)
    Ratios = np.vectorize(lambda d:get_V(d+1)/get_V(d))(Ds)

    fig = figure(figsize=(12,12))
    fig.suptitle(r'Exercise 1.13: $\frac{V_{252}(1)}{V_{250}(1)}=$ 'f'{r502*r501:.6}'
                 r'$\approx\frac{2\pi}{d}=$' f'{2*np.pi/502:.6}')
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(Ds,Estimated,label=f'Estimated, after {args.N:,} iterations',color='red',linestyle=(0,(5,5)))
    ax1.plot(Ds,Ratios,label='Ratios of volumes',color='blue',linestyle=(5,(5,5)))
    ax1.legend()
    ax1.set_xlabel('Dimension')
    ax1.set_ylabel('Ratio')
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
