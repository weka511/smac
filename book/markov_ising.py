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

''' Local Metropolis algorithm for the Ising model'''

from argparse import ArgumentParser
from collections import defaultdict
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
import seaborn as sns
from gray import Nbr
from enumerate_ising import get_initial_energy

def markov_ising(sigma,E,N,Nbr=Nbr,rng=np.random.default_rng(),shape=(4,5),periodic=False,beta=0.001):
    k = rng.integers(N)
    h = sum(sigma[i] for i in Nbr(k,shape=shape,periodic=periodic))
    deltaE = 2*h*sigma[k]
    Upsilon = np.exp(-beta*deltaE)
    if rng.random() < Upsilon:
        sigma[k] *= -1
        E += deltaE
    return E,sigma


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--periodic', default=False,action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('--Nburn', type = int, default = 1000, help = 'Number of steps for burn in')
    parser.add_argument('--Niterations', type = int, default = 5, help = 'Number of iterations of Markov chain')
    parser.add_argument('-f', '--frequency',type = int, default = 100, help = 'Number of columns')
    parser.add_argument('-T', '--T', default=[0.8,6], nargs='+', type=float, help = 'Range for temperature')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help = 'Show plot')
    return parser.parse_args()


def get_file_name(args,default_ext='.png'):
    base,ext = splitext(args.out)
    if len(ext)==0:
        ext = default_ext
    return join(args.figs,f'{base}{ext}')

def get_range(T,deltaT=0.1):
    match (len(T)):
        case 1:
            return T
        case 2:
            return np.arange(T[0],T[1],deltaT)
        case 3:
            return np.arange(T[0],T[1]+T[2],T[2])
    raise ValueError(f'Parameter T must have length of 1,2, or 3')

def markov(m,n,periodic=False,Nsteps=100000,Nburn=100,rng = np.random.default_rng(),frequency=0):
    N =m*n
    E = get_initial_energy(N,m,n,periodic=periodic)
    sigma = [-1] *N
    Ns = defaultdict(lambda: 0)
    Ns[E] = 1

    for i in range(Nsteps + Nburn):
        E,sigma = markov_ising(sigma,E,N,Nbr=Nbr,rng = rng,shape=(m,n),periodic=periodic)
        if i < Nburn: continue
        Ns[E] += 1
        if frequency > 0 and i%frequency == 0:
            print (E,sigma)

    Sum = sum([v for _,v in Ns.items()])
    data = np.zeros((len(Ns),2))
    for i,(k,v) in enumerate(Ns.items()):
        data[i,0] = k
        data[i,1] = v
    return np.sort(data,axis=1)

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    rng = np.random.default_rng(args.seed)
    T_range = get_range(args.T)

    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    width = 0.75
    for i in range(args.Niterations):
        data = markov(args.m,args.n,periodic=args.periodic,Nsteps=args.Nsteps,Nburn=args.Nburn,rng = rng,frequency=args.frequency)
        ax.bar(data[:,0] + i*width,data[:,1],width,label=f'{i}')
    ax.legend()

    fig.savefig(get_file_name(args))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
