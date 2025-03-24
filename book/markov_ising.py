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
from ising import Nbr,get_energy_magnetism
from enumerate_ising import get_initial_energy

class MarkovIsing:
    '''
    This class uses Markov Chain Monte Carlo (MCMC) to sample a Ising Model

    Attributes:
        Nbr Used to iterate through neighbours of a location
        m         Number of rows
        n         Number of columns
        N         Number of sites
        periodic  Use periodic boundary conditions
        data      Store counts
    '''
    def __init__(self,Nbr=Nbr,rng=np.random.default_rng(),shape=(4,5),periodic=False,Niterations=5):
        self.Nbr = lambda k:Nbr(k,shape=shape,periodic=periodic)
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.data = np.zeros((Niterations,4*self.N+1,2))
        self.magnetization = np.zeros((Niterations,4*self.N+1,2))

    def step(self,sigma,E,M,beta=0.001):
        '''
        Perform one step of MCMC

        Parameters:
            sigma
            E
            beta
        '''
        k = self.rng.integers(self.N)
        h = sum(sigma[i] for i in self.Nbr(k))
        deltaE = 2*h*sigma[k]
        if self.rng.random() < np.exp(-beta*deltaE):
            sigma[k] *= -1
            E += deltaE
            M += 2*sigma[k]
        return sigma,E,M

    def run(self,Nsteps=100000,Nburn=100,frequency=10000,iteration=0,lowest=False):
        '''
        Initialize configuration and carry out a specified number of steps

        Parameters:
             Nsteps
             Nburn
             frequency
             iteration
        '''
        def initialize():
            '''
            Set Spins, Energy, and Magnetization at the start of a run
            '''
            if lowest:
                E = get_initial_energy(self.N,self.m,self.n,periodic=self.periodic)
                sigma = [-1] *self.N
                M = - self.N
            else:
                sigma = rng.choice([-1,1],size=self.N)
                E,M = get_energy_magnetism(sigma, shape=(self.m,self.n), periodic=self.periodic)
            return sigma,E,M

        sigma,E,M = initialize()

        Ns = defaultdict(lambda: 0)
        Ns[E] = 1

        NMs = defaultdict(lambda: 0)
        NMs[M] = 1

        for i in range(Nsteps + Nburn):
            sigma,E,M = self.step(sigma,E,M)
            if i < Nburn: continue
            Ns[E] += 1
            NMs[M] += 1
            if frequency > 0 and i%frequency == 0:
                print (f'Iteration {iteration}, step {i}')

        for k,v in Ns.items():
            if v > 0:
                self.data[iteration,2*self.N+k,0] = k
                self.data[iteration,2*self.N+k,1] = v

        for k,v in NMs.items():
            if v > 0:
                self.magnetization[iteration,2*self.N+k,0] = k
                self.magnetization[iteration,2*self.N+k,1] = v


    def get_stats(self):
        '''
        Extract mean and standard deviation for those energies
        that have appered at least once in MCMC
        '''
        non_zero= np.sum(self.data[:,:,1],axis=0) > 0
        E = self.data[0,non_zero,0]
        means = np.mean(self.data[:,non_zero,1],axis=0)
        stds = np.std(self.data[:,non_zero,1],axis=0)
        non_zero_magnetization= np.sum(self.magnetization[:,:,1],axis=0) > 0
        M = self.magnetization[0,non_zero_magnetization,0]
        magnetization = np.mean(self.magnetization[:,non_zero_magnetization,1],axis=0)
        return E,means, stds,M,magnetization

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--periodic', default=False, action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('--Nburn', type = int, default = 0, help = 'Number of steps for burn in')
    parser.add_argument('--Niterations', type = int, default = 5, help = 'Number of iterations of Markov chain')
    parser.add_argument('-f', '--frequency',type = int, default = 100, help = 'Number of columns')
    parser.add_argument('-T', '--T', default=[0.8,6], nargs='+', type=float, help = 'Range for temperature')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', default=False, action = 'store_true', help = 'Show plot')
    parser.add_argument('--lowest', default=False, action = 'store_true', help = 'Initialize to all spins down at the start of each run')
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

def get_boundary_conditions(periodic):
    '''
    Used to format suptitle
    '''
    return 'Periodic boundary conditions' if periodic else 'Bounded'

def get_initial_conditions(lowest):
    '''
    Used to format suptitle
    '''
    return 'Start at lowest energy' if lowest else 'Random starting configuration'

def get_scaled_means(means,m=4,n=4):
    '''
    Used for comparison with Table5.2 - scale mean
    so total is number of states
    '''
    N = m*n
    NStates = 2**N
    return NStates*means/means.sum()

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    rng = np.random.default_rng(args.seed)
    T_range = get_range(args.T)

    markov = MarkovIsing(Nbr=Nbr,rng = rng,shape=(args.m,args.n),periodic=args.periodic,Niterations=args.Niterations)
    for i in range(args.Niterations):
        markov.run(Nsteps=args.Nsteps,Nburn=args.Nburn,frequency=args.frequency,iteration=i,lowest=args.lowest)

    Es,means, stds,M,magnetization = markov.get_stats()

    fig = figure(figsize=(12,12))
    fig.suptitle(fr'{get_boundary_conditions(args.periodic)}, {get_initial_conditions(args.lowest)}: {args.m}$\times${args.n} sites.')

    ax1 = fig.add_subplot(2,1,1)
    ax1.bar(Es,get_scaled_means(means,m=args.m,n=args.n),color='blue')
    ax1.set_xlabel('$E$')
    ax1.set_ylabel('$N(E)$')
    ax1.set_title(f'After {args.Niterations} iterations, {args.Nsteps} steps, and a burn in of {args.Nburn} steps.')

    ax2 = fig.add_subplot(2,1,2)
    ax2.bar(M,magnetization,width=0.8,color='red',label=r'Magnetization')
    ax2.set_xlabel('$M$')
    ax2.set_ylabel('Magnetization')
    ax2.set_title('Magnetization')
    ax2.legend(loc='upper left')

    fig.tight_layout(h_pad=4,pad=2)
    fig.savefig(get_file_name(args))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
