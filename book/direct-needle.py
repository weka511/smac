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
from matplotlib.pyplot import figure, show, colorbar
from matplotlib.cm import autumn, ScalarMappable
from matplotlib.colors import BoundaryNorm

def direct_needle(a=1.0,b=1.0,rng=np.random.default_rng(None)):
    '''
    Algorithm 1.4 direct needle

    Parameters:
        a        Length of needle
        b        Distance between cracks

    Returns:    Number of hits
    '''
    x0 = rng.uniform(0,b/2)
    phi = rng.uniform(0,np.pi/2)
    x1 = x0 - (a/2)*np.cos(phi)
    return 1 if x1 < 0 else 0

def direct_needle_patch(a=1.0,b=1.0,rng=np.random.default_rng(None)):
    '''
    Algorithm 1.4 direct needle (patch)

    Parameters:
        a        Length of needle
        b        Distance between cracks

    Returns:    Number of hits
    '''
    x0 = rng.uniform(0,b/2)
    Upsilon2 = np.inf
    while Upsilon2 > 1:
        Delta_x = rng.uniform(0,1)
        Delta_y = rng.uniform(0,1)
        Upsilon2 = Delta_x**2 + Delta_y**2
    Upsilon = np.sqrt(Upsilon2)
    x1 = x0 - (a/2) * Delta_x/Upsilon
    return 1 if x1 < 0 else 0

def driver(N,fn,m=1):
    '''
    Use either direct needle or direct needle (patch) to popululate an array with estimates
    '''
    xs = np.zeros((N))
    xs[0] =  fn()
    for i in range(1,N):
        xs[i] = xs[i-1] + fn()
    return xs[m:]/np.array(range(m,N))

def get_pi(x,a,b):
    '''
    Estimate pi using fraction of hits

    Parameters:
        x        Ratio of hits to trials
        a        Length of needle
        b        Distance between cracks
    '''
    return (2*a/b)/x

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-a','--a',type=float,default=1.0,help='Length of needle')
    parser.add_argument('-b','--b',type=float,default=1.0,help='Distance between cracks')
    parser.add_argument('-N','--N',type=int,default=10000,help='Number of trials')
    parser.add_argument('-m','--m',type=int,default=None,help='Burn in')
    parser.add_argument('-r','--rows',type=int,default=1000,help='Number of rows for landing pad')
    parser.add_argument('-c','--columns',type=int,default=1000,help='Number of columns for landing pad')
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


def get_hits(a,b,x,phi):
    '''
    Used to calculate number of hits at each position in heatmap

    Parameters:
        a       Lenght of needle
        b       Distance between cracks
        x       x coordinate of centre
        phi     Angle to horizontal
    '''
    return 1 if x < a/2 and abs(phi) < np.arccos(x/(a/2)) else 0

def hits(i,j,nrows,ncolumns,a,b):
    '''
    Adapter for get_hits(...), used to calculate number of hits at each position in heatmap

    Parameters:
        i         Row number in heatmap
        j         Columns number in heatmap
        nrows     Number of rows in heatmap
        ncolumns  Number of columns in heatmap
        a         Length of needle
        b         Distance between cracks
    '''
    x = j * (b/2) / ncolumns
    phi = i * (np.pi/2) / nrows
    return get_hits(a,b,x,phi)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    m = args.N//4 if args.m==None else args.m
    xs = driver(args.N + m,lambda :direct_needle(a=args.a,b=args.b,rng=rng),m=m)
    ys = driver(args.N + m,lambda :direct_needle_patch(a=args.a,b=args.b,rng=rng),m=m)
    nhits = np.fromfunction(
                    np.vectorize(lambda i,j:hits(i,j,args.rows,args.columns,args.a,args.b)),
                    (args.rows,args.columns))
    fig = figure(figsize=(12,12))
    fig.suptitle("Buffon's needle")
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(xs,color='r',label=f'direct needle {get_pi(xs[-1],args.a,args.b)}')
    ax1.plot(ys,color='b',label=f'direct needle (patch) {get_pi(ys[-1],args.a,args.b)}')
    ax1.legend()
    ax1.set_title(r'Estimates for $\pi$, using ' f'N={args.N:,}, burn={m:,}, a={args.a}, b={args.b}')

    ax2 = fig.add_subplot(1,2,2)
    Bounds = np.unique(nhits)
    heatmap = ax2.imshow(nhits,
                         origin = 'lower',
                         cmap = autumn,
                         norm = BoundaryNorm(Bounds, autumn.N, extend='max'),
                         interpolation = 'nearest')
    colorbar(heatmap,
             ticks = np.linspace(start=Bounds[0],stop=Bounds[-1],endpoint=True,num=len(Bounds)),
             shrink = 0.625)
    ax2.set_title('Number of hits')
    ax2.set_xlabel('$x_{center}$')
    ax2.set_ylabel(r'$\phi$')
    ax2.get_xaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
