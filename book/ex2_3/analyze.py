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

'''Plot samples from C++ program'''

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
    parser.add_argument('--samples', default = 'samples.csv', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--path', default = r'C:\cygwin64\home\Weka\smac\book\ex2_3', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
    parser.add_argument('-b', '--burn', type=int, default=10, help='Burn in time')
    return parser.parse_args()

def get_bins(bins):
    '''
    Used to parse args.bins: either a number of bins, or the name of a binning strategy.
    '''
    try:
        return int(bins)
    except ValueError:
        if bins in ['auto', 'fd', 'doane', 'scott', 'sturges', 'sqrt', 'stone', 'rice']:
            return bins
        raise ArgumentTypeError(f'Invalid binning strategy "{bins}"')

def get_file_name(name,default_ext='png',figs='./figs',seq=None):
    '''
    Used to create file names

    Parameters:
        name          Basis for file name
        default_ext   Extension if non specified
        figs          Directory for storing figures
        seq           Used if there are multiple files
    '''
    base,ext = splitext(name)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    qualified_name = f'{base}.{ext}'
    return join(figs,qualified_name) if ext == 'png' else qualified_name

def get_line_count(file_name):
    '''
    Count lines in file
    snarfed from https://stackoverflow.com/questions/845058/how-to-get-the-line-count-of-a-large-file-cheaply-in-python
    '''
    return sum(1 for _ in open(file_name))

def read_data(file_name):
    '''
    Extract X, V, T amd E from file
    '''
    count = get_line_count(file_name)
    T = np.empty((count))
    E = np.empty((count))
    X = np.empty((count,3))
    V = np.empty((count,3))
    for i,line in enumerate(open(file_name)):
        fields = [float(f) for f in line.strip().split(',')]
        T[i] = fields[0]
        X[i,:] = np.array([fields[j] for j in range(1,4)])
        V[i,:] = np.array([fields[j] for j in range(4,7)])
        E[i] = (V[i,:]**2).sum()
    return T,E,X,V

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    T,E,X,V = read_data(join(args.path,args.samples))
    m = len(T)
    n = len(np.unique(T))
    k = m//n
    burn_in = args.burn * k
    fig = figure(figsize=(12,12))
    fig.suptitle(f'{args.samples}:  {k} spheres, {n} samples, burn in for {args.burn} samples')

    ax1 = fig.add_subplot(2,2,1)
    ax1.hist(X[burn_in:,0],bins=args.bins,density=True)
    ax1.set_xlabel('$x_0$')

    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(V[burn_in:,0],bins=args.bins,density=True)
    ax2.set_xlabel('$V_0$')

    ax3 = fig.add_subplot(2,2,3)
    ax3.hist(E[burn_in:],bins=args.bins,density=True)
    ax3.set_xlabel('$E$')

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out,figs=args.figs))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
