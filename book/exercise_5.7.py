#!/usr/bin/env python

#   Copyright (C) 2024-2025 Simon Crase

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

'''Exercise 5.7. Compute Partition function'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from re import split
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import show, subplots
from ising_stats import read_data, thermo

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument( '-p','--params', default = basename(splitext(__file__)[0]),help='Name of parameters file')
    parser.add_argument('-i', '--input', default = 'ising.csv',  help  = 'File to read stats from')
    parser.add_argument('--figs', default = './figs',  help  = 'Folder to save plots')
    # parser.add_argument('-o', '--output', default = 'ising.csv',  help  = 'File to save plots')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


def get_file_name(args,default_ext='.csv'):
    base,ext = splitext(args.params)
    if len(ext)==0:
        ext = default_ext
    return f'{base}{ext}'

def read_coefficients(args):
    m = None
    n = None
    with open(get_file_name(args)) as parameter_file:
        for line in parameter_file:
            params = line.strip()
            if m == None:
                parts = params.split(',')
                m = int(parts[0])
                n = int(parts[1])

    return m,n,np.array([float(x) for x in params.split(',')])

class Partition:
    '''
    This class represent the partition function
    '''
    def __init__(self,m,n,C):
        self.C = C.copy()
        self.non_zero = [i for i in range(len(C)) if C[i] != 0]
        self.n_sites = m*n
        self.n_edges = (m-1)*n + m*(n-1)

    def evaluate(self,beta=1):
        ch = np.cosh(beta)
        sh = np.sinh(beta)
        tanh_beta = np.tanh(beta)
        def get_than_k(beta):
            tanh_beta = np.tanh(beta)
            than_k_beta = [1]
            for k in range(1,len(C)):
                than_k_beta.append(than_k_beta[-1]*tanh_beta)
            return np.array(than_k_beta)
        than_k_beta = get_than_k(beta)
        S0 = np.dot(C,than_k_beta)
        k_C_k = np.multiply(np.arange(0,len(C)),C)
        S1 = np.dot(k_C_k[1:],than_k_beta[:-1])
        Z = 2**self.n_sites * ch**self.n_edges * S0
        E_mean = -2**self.n_sites * (n*ch*sh*S0 + S1)/(S0*ch**2)
        return Z,E_mean


if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    m,n,C = read_coefficients(args)
    data,E,N = read_data(args.input)
    T = np.linspace(0.8,6.0)
    cV0 = []
    E_ising_stats = []
    Z_ising_stats = []
    for t in T:
        z,e,c = thermo(N,E,beta=1/t)
        Z_ising_stats.append(z)
        cV0.append(c)
        E_ising_stats.append(e)

    Z_fn = Partition(m,n,C)
    Z_param = []
    E_param = []
    for t in T:
        z,dz = Z_fn.evaluate(beta=1/t)
        Z_param.append(z)
        E_param.append(-dz/z)

    cols = ['Partition Function', 'Energy']
    rows = ['Stats', 'Params']

    fig, axes = subplots(nrows=2, ncols=2, figsize=(12, 8))

    for ax, col in zip(axes[0], cols):
        ax.set_title(col)

    for ax, row in zip(axes[:,0], rows):
        ax.set_ylabel(row, rotation=0, size='large')

    axes[0][0].plot(T,Z_ising_stats,color='b',label='$Z$')
    # axes[0][0].set_xlabel('Temperature')
    axes[0][0].legend()

    axes[0][1].plot(T,E_ising_stats,color='b',label='$E$')
    # axes[0][1].set_xlabel('Temperature')
    axes[0][1].legend()

    axes[1][0].plot(T,Z_param,label='$Z$')
    axes[1][0].set_xlabel('Temperature')
    axes[1][0].legend()

    axes[1][1].plot(T,E_param,color='b',label='$E$')
    axes[1][1].set_xlabel('Temperature')
    axes[1][1].legend()

    fig.tight_layout()
    fig.savefig(join(args.figs,'ex27'))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
