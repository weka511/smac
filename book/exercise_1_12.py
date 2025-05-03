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
    Exercise 1.12. Implement both naive Algorithm 1.17 (naive Gauss) and 1.18 (Box Muller).
    For what value of K can you still detect statistially significant differences between
    the two algorithms?
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from scipy.stats import kstest

def naive_gauss(K=3,rng=np.random.default_rng()):
    '''Algorithm 1.17'''
    sigma = np.sqrt(K/12)
    while True:
        yield (rng.random(K) - 0.5).sum()/sigma

def gauss(sigma=1,rng=np.random.default_rng()):
    '''Algorithm 1.18'''
    while True:
        phi = 2*np.pi * rng.random()
        upsilon = -np.log(rng.random())
        r = sigma * np.sqrt(2 * upsilon)
        yield r * np.cos(phi)
        yield r * np.sin(phi)

def gauss_patch(sigma=1,rng=np.random.default_rng()):
    '''Algorithm 1.19'''
    def get_sample():
        while True:
            x = -1 + 2* rng.random()
            y = -1 + 2* rng.random()
            upsilon1 = x**2 + y**2
            if 0 < upsilon1 and upsilon1 < 1: return upsilon1,x,y
    while True:
        upsilon1,x,y = get_sample()
        upsilon = - np.log(upsilon1)
        upsilon2 = -sigma*np.sqrt(2*upsilon/upsilon1)
        yield upsilon2*x
        yield upsilon2*y

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
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    naive = naive_gauss(K=args.K,rng=rng)
    g = gauss(args.sigma,rng=rng)
    patch = gauss_patch(args.sigma,rng=rng)
    xs = np.fromfunction(np.vectorize(lambda i:next(naive)),(args.n,))
    ys = np.fromfunction(np.vectorize(lambda i:next(g)),(args.n,))
    zs = np.fromfunction(np.vectorize(lambda i:next(patch)),(args.n,))

    ks12 = kstest(xs,ys)
    ks31 = kstest(zs,xs)
    ks23 = kstest(ys,zs)

    fig = figure(figsize=(12,12))
    fig.suptitle(f'Number of samples = {args.n:,}')
    ax1 = fig.add_subplot(2,3,1)
    ax1.hist(ys,bins=args.bins,color='blue',alpha=0.5,label='Gauss')
    ax1.legend()

    ax2 = fig.add_subplot(2,3,2)
    ax2.hist(zs,bins=args.bins,color='green',alpha=0.5,label='Gauss (patch)')
    ax2.legend()

    ax3 = fig.add_subplot(2,3,3)
    ax3.hist(xs,bins=args.bins,color='red',alpha=0.5,label=f'Naive K={args.K}')
    ax3.legend()

    ax4 = fig.add_subplot(2,3,4)
    ax4.hist(zs,bins=args.bins,color='green',alpha=0.5,label='Gauss (patch)')
    ax4.set_title(f'pvalue={ks23.pvalue:.3}')
    ax4.legend()

    ax5 = fig.add_subplot(2,3,5)
    ax5.hist(xs,bins=args.bins,color='red',alpha=0.5,label=f'Naive K={args.K}')
    ax5.set_title(f'pvalue={ks31.pvalue:.3}')
    ax5.legend()

    ax6 = fig.add_subplot(2,3,6)
    ax6.hist(ys,bins=args.bins,color='blue',alpha=0.5,label='Gauss')
    ax6.set_title(f'pvalue={ks12.pvalue:.3}')
    ax6.legend()

    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
