#!/usr/bin/env python

# Copyright (c) 2018-2025 Simon Crase

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
    Exercise 1.22 Implement Algorithm 1.29, subtract mean value for each sample, and generate
    histograms of the average of N samples and the rescaled averages.
'''

import argparse
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib import rc
from scipy.interpolate import make_interp_spline, BSpline

def direct_gamma(gamma,N=10, rng = np.random.default_rng()):
    '''
    Algorithm 1.29 Computing the gamma integral by direct sampling

    Parameters:
        gamma
        N
        rng
    '''
    return (rng.random(size=N)**gamma).sum()/N

def parse_arguments():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--M', type=int, default=100000,help='Number of steps for integral')
    parser.add_argument('--N',  type=int, nargs='+',default=[1,10,100,1000,10000],help='Number of steps for integral')
    parser.add_argument('--gamma',type=float,default=-0.8,help='exponent')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs',help='Folder for storing plot')
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

if __name__ == '__main__':
    start = time()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    bins = np.linspace(0,11.5,num=22,endpoint=True)
    scaled_bins = np.linspace(-8,3,num=22,endpoint=True)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    for N in args.N:
        data = np.fromfunction(np.vectorize(lambda _:direct_gamma(args.gamma,N=N,rng=rng)), (args.M,))
        scaled = (data - 5)/(N**-0.2)
        y,_ = np.histogram(data,density=True,bins=bins)
        ax1.plot(bins[:-1],y,label=f'N={N:,}')
        upsilon,_ = np.histogram(scaled,density=True,bins=scaled_bins)
        ax2.plot(scaled_bins[:-1],upsilon,label=f'N={N:,}')

    ax1.set_xlim(1,10)
    ax1.set_xlabel(r'$\Sigma/N$')
    ax1.set_ylabel(r'$\pi(\Sigma/N$)')
    ax1.set_title('Average')
    ax1.legend()
    ax2.set_xlabel(r'$\upsilon/N$')
    ax2.set_ylabel(r'$\pi(\upsilon/N$)')
    ax2.set_title('Rescaled Average')
    ax2.legend()

    fig.suptitle(r'$\gamma=$'f'{args.gamma}, after {args.M:,} iterations')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
