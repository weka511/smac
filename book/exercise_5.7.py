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


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-i', '--input', default = basename(splitext(__file__)[0]),help='Name of parameters file')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


def get_file_name(args,default_ext='.csv'):
    base,ext = splitext(args.input)
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

    def evaluate(self,beta):
        ch = np.cosh(beta)
        sh = np.sinh(beta)
        th = np.tanh(beta)
        sigma_Z = 0
        sigma_Z1 = 0
        for i in self.non_zero:
            sigma_Z += self.C[i] * th**i
            sigma_Z1 += self.n_edges * ch**(self.n_edges-1) * sh * self.C[i] * th**i
            sigma_Z1 += ch**(self.n_edges-2) * i * th**(i-1)
        Z = 2**self.n_sites * ch**self.n_edges * sigma_Z
        Z1 = 2**self.n_sites * sigma_Z1
        return Z,Z1


if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    m,n,C = read_coefficients(args)
    Z = Partition(m,n,C)
    Ts = np.linspace(0.8,6)
    Zs = []
    Z1s = []
    for t in Ts:
        Z0,Z1 = Z.evaluate(1/t)
        Zs.append(Z0)
        Z1s.append(-Z1/Z0)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(Ts,Zs)
    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(Ts,Z1s)
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
