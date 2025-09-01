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

'''Simulate preferential attachment'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from numpy.linalg import cond
from scipy.optimize import curve_fit

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-N', '--N', type=int, default=100000, help='Number of iterations')
    parser.add_argument('-p', '--p', type=float, default=0.1, help='Number of iterations')
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

def build(N,p,rng = np.random.default_rng()):
    '''
    Simulate preferential attachment. Use tower sampling to build table of frequencies

    Parameters:
        N
        p
        rng
    '''
    n = 0
    frequencies = np.zeros((N),dtype=int)
    frequencies[n] = 1
    tower = np.zeros((N),dtype=int)
    tower[n] = 1
    n += 1
    for _ in range(N):
        if rng.uniform() < p:
            frequencies[n] = 1
            tower[n] = tower[n-1] + 1
            n += 1
        else:
            sample = rng.choice(tower[n-1])
            i = 0
            while tower[i] < sample:
                i += 1
            frequencies[i] += 1
            while i<n:
                tower[i] += 1
                i += 1

    return np.flip(np.sort(np.resize(frequencies,(n))))

def get_frequencies(word_counts):
    '''
    Establish mapping from word occurrences to frequency
    '''
    m = word_counts[0]
    frequencies = np.zeros((m))
    for i in range((len(word_counts))):
        frequencies[word_counts[i]-1] += 1
    return frequencies/sum(frequencies)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    word_counts = build(args.N,args.p,rng = rng)
    frequencies = get_frequencies(word_counts)

    n = len(frequencies)
    xdata = np.arange(0,n)
    power_law = lambda x,a,b: (a**x) * b

    popt, pcov = curve_fit(power_law, xdata, frequencies)
    ydata = [power_law(x,popt[0],popt[1]) for x in xdata]

    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(xdata,frequencies,label='Probabilities')
    ax1.plot(xdata,ydata,linestyle=':',label=f'Power law: a={popt[0]:.3f}({-(1+1/(1-args.p)):.3f}),b={popt[1]:.3f},cond={cond(pcov):.3f}')
    ax1.legend()
    ax1.set_title(f'Preferential attachment: p={args.p}')
    fig.savefig(get_file_name(args.out,figs=args.figs))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
