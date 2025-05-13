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
    Exercise 1.11: investigate the distribution of x**2 + y**2.
    Compare theoretical and empirical distributions.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('-N','--N', type=int, default=10000, help = 'Number of points')
    parser.add_argument('-n','--n', type=int, default=1000, help = 'Number of bins for histogram')
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

def get_distribution(num=10):
    '''
    This function is used to calculate the empirical distribution of x**2 + y**2, on the assumption that
    x**2 + y**2 < 1. It is used in conjunction with get_distribution_extended(...)

    Parameters:
        num    Number of points to be plotted

    Returns:
        xs    An array, each of whose elements represents the area of a circle in the x-y plane
        ys    An array, each of whose elements, ys[i], represents the probability that x**2 + y**2<xs[i]
    '''
    xs = np.linspace(0,1,num=num,endpoint=True)
    ys = np.linspace(0,np.pi/4,num=num,endpoint=True)
    return xs,ys

def get_distribution_extended(num=50):
    '''
    This function is used to calculate the empirical distribution of x**2 + y**2, on the assumption that
    x**2 + y**2 >1 1. It is used in conjunction with get_distribution(...).

    Parameters:
        num    Number of points to be plotted

    Returns:
        xs    An array, each of whose elements represents the area of a circle in the x-y plane
        ys    An array, each of whose elements, ys[i], represents the probability that x**2 + y**2<xs[i]

    The probability is the sum of two areas, a triangle OAB and a sector OBC, as depicted in  notes and diagram in
    SMAC notebook, page 59.

    '''
    def get_probability(R):
        def get_area_triangle():
            '''
            Area of triangle AOB
            '''
            return 0.5 * np.sqrt(R**2 - 1)

        def get_area_sector():
            '''
            Area of sector OBC
            '''
            theta = np.arccos(1/R)
            theta_segment = np.pi/4 - theta
            return R**2 * theta_segment/2

        return 2 * (get_area_triangle() + get_area_sector())

    xs = np.linspace(1,2,num=num,endpoint=True)
    return xs, np.array([get_probability(np.sqrt(Area)) for Area in xs])

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    ax.hist(np.fromfunction(np.vectorize(lambda _:np.square(2.0 * rng.random((2)) - 1).sum()),(args.N,)),
            bins = np.linspace(0,2,num=args.n,endpoint=True),
            density = True,
            cumulative = True,
            color = 'cyan',
            label = 'Empirical')

    xs,ys = get_distribution()
    ax.plot(xs,ys,color='red',label=r'$Theoretical\ (R\le 1)$')
    x1s,y1s = get_distribution_extended()
    ax.plot(x1s,y1s,color='blue',label=r'$Theoretical\ (R>1)$')
    ax.set_xlabel(r'$\upsilon$')
    ax.set_ylabel('Frequency')
    ax.set_title(r'$\upsilon=x^2+y^2$' f' for {args.N:,} points')
    ax.legend(title='Cumulative distribution')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
