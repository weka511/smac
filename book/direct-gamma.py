#!/usr/bin/env python

# Copyright (c) 2018-2025 Simon Crase

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

#   The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
    Exercise 1.22 Implement Algorithm 1.29, subtract mean value for each sample, and generate
    histograms of the average of N samples and the rescaled averages.
'''
import argparse
from os.path import basename, join, splitext
from time import time
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.pyplot import figure, show

def direct_gamma(gamma,generator=False,K=10000,N=1000000, rng = np.random.default_rng()):
    sigma = 0
    for i in range(N):
        sigma += rng.random()**gamma
    return sigma/N

def parse_arguments():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('steps', metavar='M', type=int, nargs=1,help='Number of steps for integral')
    parser.add_argument('--N', metavar='N', type=int, nargs='+',default=[1,10,100,1000,10000],help='Number of steps for integral')
    parser.add_argument('--gamma',metavar='gamma',type=float,nargs=1,default=-0.8,help='exponent')
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
    args=parse_arguments()
    rng = np.random.default_rng(args.seed)
    M = args.steps[0]
    gamma = args.gamma
    bins = np.linspace(0,11.5,num=22,endpoint=True)
    bins[-1] = 100000000000
    fig = figure()
    ax1 = fig.add_subplot(1,1,1)

    for N in args.N:
        data = [direct_gamma(gamma,N=N) for m in range(M)]
        density = gaussian_kde(data)
        y,binEdges = np.histogram(data,density=True,bins=bins)
        bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        ax1.plot(bincenters,density(bincenters),label='N={0}'.format(N))

    ax1.set_xlim(1,10)
    ax1.set_xlabel(r'$\Sigma/N$')
    ax1.set_xlabel(r'$\pi(\Sigma/N$)')
    ax1.set_title(r'$Average\ {0}\ iterations$'.format(M))
    ax1.legend()
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
