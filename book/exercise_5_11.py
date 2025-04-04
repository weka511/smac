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

'''Exercise 5-11/Algorithm 5-9: cluster ising'''

from argparse import ArgumentParser
from collections import defaultdict
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from cluster_ising import ClusterIsing
from ising_db import IsingDatabase

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--periodic', default=False, action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output files')
    parser.add_argument('-d', '--database', default = basename(splitext(__file__)[0]),help='Name of database')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', default=False, action = 'store_true', help='Show plot')
    parser.add_argument('-T', '--T', default=[0.5,4,0.5], nargs='+', type=float, help = 'Range for temperature: [start, ]stop, [step, ]')
    parser.add_argument('--Tc',default=False,action = 'store_true', help   = 'Include critical temperature')
    parser.add_argument('--verbose', default=False, action = 'store_true', help   = 'More messages')
    parser.add_argument('--fresh', default=False, action = 'store_true', help='Start with a fresh database')
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

def get_periodic(periodic):
    '''
    Used to construct title for plot
    '''
    return 'with periodic boundary conditions,' if periodic else ''

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    database = IsingDatabase(args.database,verbose=args.verbose,fresh=args.fresh)
    T_range = get_range(args.T)
    if args.Tc:
        T_range = sorted(list(T_range) + [2/np.log(1+np.sqrt(2))])

    fig = figure(figsize=(12,12))
    fig.suptitle(rf'Cluster Ising {args.m}$\times${args.n}, {get_periodic(args.periodic)}')
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    N = args.m*args.n
    width = 25/len(T_range)  # Established empirically

    for i,T in enumerate(T_range):
        markov = ClusterIsing(rng=np.random.default_rng(args.seed),shape=(args.m,args.n),periodic=args.periodic,beta=1/T)
        nIterations = markov.run(Nsteps=args.Nsteps,database=database)
        E = np.array([[e,n] for e,n in markov.data.generate_E()],dtype=int)
        ax1.bar(E[:,0],E[:,1],width=width,label=f'T={T:.3},Nsteps={nIterations}')
        M = np.array([[m,n] for m,n in markov.data.generate_M()],dtype=int)
        ax2.bar(M[:,0],M[:,1],width=width,label=f'T={T:.3},Nsteps={nIterations}')

    ax1.set_xlim(E[0,0],E[-1,0])
    ax1.set_title('Energy')
    ax2.set_xlim(M[0,0],M[-1,0])
    ax2.set_title('Magnetization')
    ax1.legend()
    ax2.legend()
    fig.tight_layout(pad=2)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
