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
    Exercise 5.7. Compute Partition function
    using loop configurations as described in 5.1.3
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import show, subplots
from ising_stats import thermo

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument( '-p','--params', default = basename(splitext(__file__)[0]),help='Name of parameters file')
    parser.add_argument('-i', '--input', default = 'ising.csv',  help  = 'File to read stats from')
    parser.add_argument('-T', '--T', default=[0.8,6], type=float, help = 'Range for temperature')
    parser.add_argument('--nT', default=10, type=int, help='Number of temperature to plot ')
    parser.add_argument('--figs', default = './figs',  help  = 'Folder to save plots')
    default_plot_file_name,_ = splitext(__file__)
    parser.add_argument('--plots', default=default_plot_file_name,help  = 'Folder to save plots')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


def get_file_name(name,default_ext='.csv'):
    base,ext = splitext(name)
    if len(ext)==0:
        ext = default_ext
    return f'{base}{ext}'

def read_coefficients(params):
    m = None
    n = None
    with open(get_file_name(params)) as parameter_file:
        for line in parameter_file:
            params = line.strip()
            if m == None:
                parts = params.split(',')
                m = int(parts[0])
                n = int(parts[1])

    return m,n,np.array([float(x) for x in params.split(',')])

def read_data(input_file):
    '''
    Read Counts by Energy and Magnetization prepared by ising.py
    '''
    data = np.genfromtxt(input_file, delimiter=',')[1:,:]
    m,_ = data.shape
    E = np.unique(data[:,0])
    N = np.zeros_like(E)
    for i in range(len(E)):
        mask = np.in1d(data[:,0],E[i])
        N[i] = data[mask,2].sum()

    return E,N

class Partition:
    '''
    This class represent the partition function using the representation
    of given in Section 5.3.1
    '''
    def __init__(self,m,n,C):
        self.C = C.copy()
        self.non_zero = [i for i in range(len(C)) if C[i] != 0]
        self.n_sites = m*n
        self.n_edges = (m-1)*n + m*(n-1)

    def evaluate(self,beta=1):
        '''
        Calculate Thermodynamic quantities

        Parameters:
            beta
        '''
        def create_powers(x=np.tanh(beta),n=3):
            '''
            Populate an array withe powers of tanh(beta),
            which are used in the calculatation of Z and its derivatines.
            '''
            Product = np.ones((n))
            for k in range(1,n):
                Product[k] = Product[k-1]*x
            return Product

        ch = np.cosh(beta)
        sh = np.sinh(beta)
        tanh_k_beta = create_powers(n=len(C))
        S0 = np.dot(C,tanh_k_beta)
        S1 = np.dot(np.multiply(np.arange(1,len(C)),C[1:]), tanh_k_beta[:-1])
        Z = 2**self.n_sites * ch**self.n_edges * S0
        E_mean =  - (self.n_edges*ch*sh*S0 + S1)/(S0 * ch**2)
        return Z,E_mean



if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    m,n,C = read_coefficients(args.params)
    E,N = read_data(get_file_name(args.input))
    T = np.linspace(args.T[0],args.T[1],num=args.nT)
    cV0 = []
    E_ising_stats = []
    Z_ising_stats = []
    for t in T:
        z,e,c = thermo(E,N,beta=1/t)
        Z_ising_stats.append(z)
        cV0.append(c)
        E_ising_stats.append(e)

    Z_fn = Partition(m,n,C)
    Z_param = []
    E_param = []
    for t in T:
        z,E_mean = Z_fn.evaluate(beta=1/t)
        Z_param.append(z)
        E_param.append(E_mean)

    cols = [r'$Z(\beta)$', r'$\bar{E}$']
    rows = ['Thermo Ising', 'Edge Ising']

    fig, axes = subplots(nrows=2, ncols=2, figsize=(12, 8))
    fig.suptitle(str(m)+r'$\times$'+str(n))
    for ax, col in zip(axes[0], cols):
        ax.set_title(col)

    for ax, row in zip(axes[:,0], rows):
        ax.set_ylabel(row, rotation=90)

    axes[0][0].plot(T,Z_ising_stats,color='b',label='$Z$')
    axes[0][0].legend()

    axes[0][1].plot(T,E_ising_stats,color='b',label='$E$')
    axes[0][1].legend()

    axes[1][0].plot(T,Z_param,label='$Z$')
    axes[1][0].set_xlabel('Temperature')
    axes[1][0].legend()

    axes[1][1].plot(T,E_param,color='b',label='$E$')
    axes[1][1].set_xlabel('Temperature')
    axes[1][1].legend()

    fig.tight_layout()
    fig.savefig(join(args.figs,get_file_name(basename(args.plots),default_ext='.png')))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
