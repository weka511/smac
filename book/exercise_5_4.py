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

''' Exercise 5.4: implement thermo-ising'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np



def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-i', '--input', default = r'C:\cygwin64\home\Weka\smac\book\ising\out.txt',help='Name of input file')
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

def create_E(data):
    def get_upper_limit(i):
        return indices[i+1] if i+1 < len(indices) else m

    m,_ = data.shape
    Es,indices = np.unique(data[:,0],return_index=True)
    product = np.zeros((len(Es),2),dtype=np.int64)
    for i in range(len(Es)):
        product[i,0] = Es[i]
        product[i,1] = sum(data[j,2] for j in range(indices[i],get_upper_limit(i)))
    return product

def thermo(E,N,beta=1,NObservations=36):
    weights = np.exp(-beta*E) *N
    Emean = np.average(E,weights=weights)
    e = Emean/NObservations
    cV = beta**2 * np.average((E-Emean)**2,weights=weights)/NObservations
    return e, cV

if __name__=='__main__':
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    _,_,data = get_data(args.input)

    E = create_E(data)
    for T in [0.5, 1.0, 1.5, 1.0, 2.5, 3, 3.5,4.0]:
        e,cV = thermo(E[:,0],E[:,1],beta=1/T)
        print (T,e,cV)

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

