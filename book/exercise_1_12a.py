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
from exercise_1_12 import naive_gauss,gauss,gauss_patch

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-m','--m',type=int,default=10)
    parser.add_argument('-n','--n',type=int,default=10000)
    parser.add_argument('-K','--K',type=int,nargs='+', default=[5,12])
    parser.add_argument('-b','--bins',type=int,default=25)
    parser.add_argument('--sigma',type=float,default=1.0)
    parser.add_argument('--significance',type=float,default=0.05)
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

def get_rows_columns(kmax):
    '''
    Used when we want a number of subplots. Choose number of rows and
    columns to make the array of plots be as square as possible.
    '''
    nrows = int(np.sqrt(kmax))
    ncolumns = kmax // nrows
    if nrows * ncolumns < kmax:
        if nrows < ncolumns:
            nrows += 1
        else:
            ncolumns += 1
    return nrows,ncolumns

def get_range(K):
    '''
    Parse up to 3 parameters into a range.
    '''
    match len(K):
        case 1:
            return K
        case 2:
            return range(K[0],K[1]+1)
        case 3:
            return range(K[0],K[1]+K[2],K[2])
        case _:
            raise ValueError('K should have length 1, 2, or 3.')

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    Ks = get_range(args.K)
    nrows,ncolumns = get_rows_columns(len(list(Ks)))
    fig = figure(figsize=(12,12))
    fig.suptitle(f'Kolmogorov Smirnov test, {args.m} iterations, {args.n:,} samples per iteration')
    for k,K in enumerate(Ks):
        ax = fig.add_subplot(nrows,ncolumns,k+1)
        pvalues = np.zeros((args.m,3))
        for i in range(args.m):
            naive = naive_gauss(K=K,rng=rng)
            g = gauss(args.sigma,rng=rng)
            patch = gauss_patch(args.sigma,rng=rng)
            xs = np.fromfunction(np.vectorize(lambda i:next(naive)),(args.n,))
            ys = np.fromfunction(np.vectorize(lambda i:next(g)),(args.n,))
            zs = np.fromfunction(np.vectorize(lambda i:next(patch)),(args.n,))
            pvalues[i,0] = kstest(ys,zs).pvalue
            pvalues[i,1] = kstest(zs,xs).pvalue
            pvalues[i,2] = kstest(xs,ys).pvalue
        ax.plot(np.sort(pvalues[:,0]),label='Gauss/Gauss Patch',color='r')
        ax.plot(np.sort(pvalues[:,1]),label='Naive Gauss/Gauss Patch',color='g')
        ax.plot(np.sort(pvalues[:,2]),label='Naive Gauss/Gauss',color='b')
        ax.axhline(y=args.significance,label=f'p={args.significance}',color='m')
        ax.legend(title=f'K={K}')

    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
