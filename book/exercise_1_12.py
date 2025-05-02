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
from scipy.stats import kstest

def naive_gauss(K=3,rng=np.random.default_rng()):
    sigma = np.sqrt(K/12)
    while True:
        yield (rng.random(K) - 0.5).sum()/sigma

def gauss(sigma,rng=np.random.default_rng()):
    while True:
        phi = 2*np.pi * rng.random()
        upsilon = -np.log(rng.random())
        r = sigma * np.sqrt(2 * upsilon)
        yield r * np.cos(phi)
        yield r * np.sin(phi)

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-n','--n',type=int,default=10000)
    parser.add_argument('-K','--K',type=int,default=5)
    parser.add_argument('-b','--bins',type=int,default=25)
    parser.add_argument('--sigma',type=float,default=1.0)
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
    naive_gauss()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    xs = np.zeros((args.n))
    ys = np.zeros((args.n))
    naive = naive_gauss(K=args.K,rng=rng)
    g = gauss(args.sigma,rng=rng)
    for i in range(args.n):
        xs[i] = next(naive)
        ys[i] = next(g)

    ks1 = kstest(xs,ys)

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.hist(xs,bins=args.bins,color='red',alpha=0.5,label=f'Naive K={args.K}')
    ax1.hist(ys,bins=args.bins,color='blue',alpha=0.5,label='Gauss')
    ax1.set_title(f'K={args.K}, sigma={args.sigma}, pvalue={ks1.pvalue}')

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
