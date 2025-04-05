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

'''Exercise 5.6'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('-i', '--input', default = r'C:\cygwin64\home\Weka\smac\book\ising\out.txt',help='Name of input file')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-T', '--T', default=[0.5,4,0.5], nargs='+', type=float, help = 'Range for temperature: [start, ]stop, [step, ]')
    return parser.parse_args()

def get_range(T,deltaT=0.1):
    '''
    Used to convert temperature (specified in args) to a range

    Parameters:
        T       [start, ]stop, [step, ]
    '''
    match (len(T)):
        case 1:
            return T
        case 2:
            return np.arange(T[0],T[1],deltaT)
        case 3:
            return np.arange(T[0],T[1]+T[2],T[2])

    raise ValueError(f'Parameter T must have length of 1,2, or 3')

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

def get_data(file_name):
    data = []
    n = None
    periodic = False
    with open(file_name) as input:
        i = 0
        data = []
        for line in input:
            match (i):
                case 0:
                    parts = line.strip().split(',')
                    n = int(parts[0][2:])
                    periodic = parts[1].lower() == 'periodic'
                case 1:
                    pass
                case _:
                    data.append([int(j) for j in line.split(',')])
            i += 1
        return n,periodic,np.array(data,dtype=np.int64)

def create_M(M,P):
    def get_upper_limit(i):
        return indices[i+1] if i+1 < len(indices) else m

    m = len(M)
    Ms,indices = np.unique(M,return_index=True)
    product = np.zeros((len(Ms)))
    for i in range(len(Ms)):
        product[i] = sum(P[j] for j in range(indices[i],get_upper_limit(i)))
    return Ms,product

def thermo(E,N,beta=1,NObservations=36):
    weights = np.exp(-beta*E) *N
    Emean = np.average(E,weights=weights)
    e = Emean/NObservations
    cV = beta**2 * np.average((E-Emean)**2,weights=weights)/NObservations
    return e, cV

def get_probabilities(data,beta=1.0):
    E = data[:,0] - min(data[:,0])
    weights = np.exp(-beta * E)
    Z = weights.sum()
    probabilities = weights * data[:,2]/Z
    indices = np.argsort(data[:,1])
    return data[indices,1],probabilities[indices]

def get_boundary_conditions(periodic):
    return ' with periodic boundary conditions' if periodic else ''

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    n,periodic,data = get_data(args.input)
    fig = figure(figsize=(12,12))
    ax1 = fig.add_subplot(1,1,1)
    for T in get_range(args.T):
        M,P = get_probabilities(data,beta=1/T)
        Ms,probabilities=create_M(M,P)
        ax1.plot(Ms,probabilities/probabilities.sum(),label=f'T={T}')
    ax1.set_xlabel('M')
    ax1.set_ylabel(r'$\pi$')
    ax1.set_title(fr'Exercise 2.6: {n}$\times${n} grid {get_boundary_conditions(periodic)}')
    ax1.legend()
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed  - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
