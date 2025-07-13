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
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N', '--N', type=int, default=100000, help='Number of iterations')
    return parser.parse_args()


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

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    file_name = r'C:\cygwin64\home\Weka\smac\book\ex2_3\samples.csv'
    count = 0
    for line in open(file_name):
        count += 1

    E = np.empty((count))
    X = np.empty((count,3))
    V = np.empty((count,3))
    for i,line in enumerate(open(file_name)):
        fields = [float(f) for f in line.strip().split(',')]
        X[i,:] = np.array([fields[j] for j in range(1,4)])
        V[i,:] = np.array([fields[j] for j in range(4,7)])
        E[i] = (V[i,:]**2).sum()

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(2,2,1)
    ax1.hist(X[:,0],bins='sqrt',density=True)
    ax2 = fig.add_subplot(2,2,2)
    ax2.hist(V[:,0],bins='sqrt',density=True)
    ax3 = fig.add_subplot(2,2,3)
    ax3.hist(E[:],bins='sqrt',density=True)
    fig.savefig(get_file_name(args.out,figs=args.figs))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
