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

'''Exercise 5-11/Algorithm 5-9-cluster ising'''

from argparse import ArgumentParser
from collections import defaultdict
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from ising import Nbr, get_energy_magnetism, Neighbours

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('--periodic', default=False, action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', default=False, action = 'store_true', help   = 'Show plot')
    parser.add_argument('-T', '--T', default=[0.5,4,0.5], nargs='+', type=float, help = 'Range for temperature: [start, ]stop, [step, ]')
    parser.add_argument('--Tc',default=False,action = 'store_true', help   = 'Include critical temperature')
    parser.add_argument('--nocache',default=False,action = 'store_true', help='Do not Cache Neighbours')
    return parser.parse_args()

def get_range(T,deltaT=0.1):
    '''
    Used to convert temperature (specified in args) to a range

    Parameters:
        T       [start, ]stop, [step, ]
    '''
    match (len(T)):
        case 1:
            return [T]
        case 2:
            return np.arange(T[0],T[1],deltaT)
        case 3:
            return np.arange(T[0],T[1]+T[2],T[2])

    raise ValueError(f'Parameter T must have length of 1,2, or 3')


class ClusterIsing:
    '''
    Algorithm 5.9 Cluster Ising
    '''
    def __init__(self,Nbr=Nbr,rng=np.random.default_rng(),shape=(4,5),periodic=False,beta=0.001,cache=False):
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.beta = beta
        self.p  = 1.0 - np.exp(-2.0*beta)
        self.E = np.zeros((4*self.N+1))
        self.M = np.zeros((2*self.N+1))
        self.cache = cache
        if cache:
            self.neighbours = Neighbours(shape=shape,periodic=periodic)
        else:
            self.Nbr = lambda k:Nbr(k,shape=shape,periodic=periodic)


    def step(self,sigma):
        '''
        Construct Cluster and the Pocket, a subset that will be used to expand the Cluster.
        Initially each of them contains the same randomly selected spin. We extend the Cluster
        by selecting one element from the pocket repeatedly, and growing both sets by randomly selecting
        neighbours with the same spin.
        '''
        def get_neighbours(k):
            if self.cache:
                return [l for l in self.neighbours[k,:] if l > -1]
            else:
                return self.Nbr(k)
        j = self.rng.integers(self.N)
        Pocket, Cluster = [j], [j]
        while Pocket != []:
            k = self.rng.choice(Pocket)
            for l in get_neighbours(k):
                if (sigma[l] == sigma[k]
                    and l not in Cluster
                    and self.rng.uniform() < self.p):
                    Pocket.append(l)
                    Cluster.append(l)
            Pocket.remove(k)
        for k in Cluster:
            sigma[k] *= -1

    def run(self,Nsteps=1000):
        '''
        Construct one chain
        '''
        get_em = lambda sigma:get_energy_magnetism(sigma, shape=(self.m,self.n), periodic=self.periodic)
        sigma = self.rng.choice([-1,1],size=self.N)
        E,M = get_em(sigma)
        self.E[2*self.N + E] += 1
        self.M[self.N + M] += 1
        for i in range(Nsteps):
            self.step(sigma)
            E,M = get_em(sigma)
            self.E[2*self.N + E] += 1
            self.M[self.N + M] += 1

def get_file_name(args,default_ext='.png',seq=None):
    '''
    Used to create file names

    Parameters:
        args
        default_ext
        seq
    '''
    base,ext = splitext(args.out)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    return join(args.figs,f'{base}{ext}')

def get_periodic(periodic):
    '''
    Used to construct tile for plot
    '''
    return 'with periodic boundary conditions,' if periodic else ''

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    T_range = get_range(args.T)
    fig = figure(figsize=(12,12))
    fig.suptitle(rf'Cluster Ising {args.m}$\times${args.n}, {get_periodic(args.periodic)} after {args.Nsteps} Steps')
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    N = args.m*args.n
    width = 5/len(T_range)
    if args.Tc:
        T_range = sorted(list(T_range) + [2/np.log(1+np.sqrt(2))])
    for i,T in enumerate(T_range):
        markov = ClusterIsing(rng=np.random.default_rng(args.seed),shape=(args.m,args.n),periodic=args.periodic,beta=1/T,cache=not args.nocache)
        markov.run(Nsteps=args.Nsteps)
        ax1.bar(np.array(list(range(-2*N,2*N+1)))+i*width,markov.E,width=width,label=f'T={T:.3}')
        ax2.bar(np.array(list(range(-N,N+1)))+i*width,markov.M,width=width,label=f'T={T:.3}')

    ax1.set_title('Energy')
    ax2.set_title('Magnetization')
    ax1.legend()
    ax2.legend()
    fig.tight_layout(pad=2)
    fig.savefig(get_file_name(args))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
