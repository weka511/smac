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

'''Exercise 5.7. Compute Partition functions'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from re import split
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from ising_stats import read_data, thermo

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument( '-p','--params', default = basename(splitext(__file__)[0]),help='Name of parameters file')
    parser.add_argument('-i', '--input',
                         default = 'ising.csv',
                         help  = 'File to read data from')
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
        S1 = np.dot(C[1:],than_k_beta[:-1])
        # for i in self.non_zero:
            # # sigma_Z += self.C[i] * th**i
            # S1 += self.n_edges * ch**(self.n_edges-1) * sh * self.C[i] * tanh_beta**i
            # S1 += ch**(self.n_edges-2) * i * tanh_beta**(i-1)
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
    Ts = np.linspace(0.8,6)
    Z_param = []
    E_param = []
    for t in Ts:
        z,dz = Z_fn.evaluate(beta=1/t)
        Z_param.append(z)
        E_param.append(-dz/z)

    fig = figure(figsize=(12,12))

    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(T,Z_ising_stats,color='b',label='$Z$')
    ax1.set_xlabel('Temperature')
    ax1.set_ylabel('Partition Function')
    ax1.set_title('Partition Function (stats)')
    ax1.legend()

    ax2 = fig.add_subplot(2,2,2)
    ax2.plot(T,E_ising_stats,color='b',label='$E$')
    ax2.set_xlabel('Temperature')
    ax2.set_ylabel('Energy')
    ax2.set_title('Energy')
    ax2.legend()

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(Ts,Z_param,label='$Z$')
    ax3.set_xlabel('Temperature')
    ax3.set_ylabel('Partition Function')
    ax3.set_title('Partition Function (parama)')
    ax3.legend()

    ax4 = fig.add_subplot(2,2,4)
    ax4.plot(Ts,E_param,color='b',label='$E$')
    ax4.set_xlabel('Temperature')
    ax4.set_ylabel('Energy')
    ax4.set_title('Energy')
    ax4.legend()

    # ax2 = fig.add_subplot(2,1,2)
    # ax2.plot(Ts,Z1s)

    fig.tight_layout()
    fig.savefig('exe')
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
