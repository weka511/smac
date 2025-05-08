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
    Exercise 1.14 Sample random vectors on the surface of a hypersphere using Algorithm 1.22
    and plot x[0]**2 + y[0]**2.
    I have allowed a polynomial of arbitrary order to be plotted. The plots are prepared
    for a range of values of the dimension, organized into rows and columns.S
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def direct_surface(d,rng = np.random.default_rng(None)):
    '''
    Sample random vectors on the surface of a sphere using Algorithm 1.22

    Parameters:
        d        Dimension of sphere
        rng      Random number generator
    '''
    sigma = 1/np.sqrt(d)
    while True:
        x = rng.normal(scale=sigma,size=(d))
        Sigma = np.square(x).sum()
        yield x/np.sqrt(Sigma)

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs',help='Folder for storing plot')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--rows',type=int,default=3,help = 'Number of rows to be plotted')
    parser.add_argument('--columns',type=int,default=3,help = 'Number of columns to be plotted')
    parser.add_argument('-n','--n',type=int,default=1000, help='Number of points to be sampled')
    parser.add_argument('-m','--m',type=int,default=100,help='Number of bins for histogram')
    parser.add_argument('-k','--k',type=int,default=2,help='Degree of polynomial to be sampled')
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
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))
    for i in range(args.rows*args.columns):
        d = i + 1 + args.k
        SumSquares = np.zeros((args.n))
        ds = direct_surface(d=d,rng=rng)
        for j in range(args.n):
            x = next(ds)
            SumSquares[j] = np.square(x[0:args.k]).sum()
        ax = fig.add_subplot(args.rows,args.columns,i+1)
        ax.hist(SumSquares,bins=args.m,color='blue',density=True)
        ax.set_title(f'd={d}, k={args.k}')

    fig.tight_layout(h_pad=2)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
