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

from collections import defaultdict
from enum import Enum
from unittest import TestCase, main
import numpy as np
from ising import Nbr,get_energy_magnetism,get_max_neighbours,Neighbours
from enumerate_ising import get_initial_energy

class Datum(Enum):
    '''
    Used when we access energy or momentum counts to specify which one we mwan.
    '''
    ENERGY = 0
    MAGNETIZATION = 1

class IsingData:
    '''
    This class is responsible for keeping track of energies and magnetization
    '''
    def __init__(self,Niterations=5,N=16):
        self.N = N
        self.energies = np.zeros((Niterations,4*N+1,2))
        self.magnetization = np.zeros((Niterations,4*N+1,2))

    def store_data(self,table=Datum.ENERGY,iteration=0,Ns={}):
        '''
        Store value and count for energy or magnetization

        Parameters:
             iteration   Iteration number: specified location of data
             Ns          A dictionary of E or M, accompanied by counts
             table       Datum.ENERGY or Datum.MAGNETIZATION
        '''
        data = self.energies if table == Datum.ENERGY else self.magnetization
        for k,v in Ns.items():
            if v > 0:
                data[iteration,2*self.N+k,0] = k
                data[iteration,2*self.N+k,1] = v

    def get_non_zero(self,table=Datum.ENERGY):
        data = self.energies if table == Datum.ENERGY else self.magnetization
        return np.sum(data[:,:,1],axis=0) > 0

    def get_stats(self):
        '''
        Extract mean and standard deviation for those energies
        that have appeared at least once in MCMC
        '''
        non_zero = self.get_non_zero(table=Datum.ENERGY)
        E = self.energies[0,non_zero,0]
        means = np.mean(self.energies[:,non_zero,1],axis=0)
        stds = np.std(self.energies[:,non_zero,1],axis=0)
        non_zero_magnetization = self.get_non_zero(table=Datum.MAGNETIZATION)
        M = self.magnetization[0,non_zero_magnetization,0]
        magnetization = np.mean(self.magnetization[:,non_zero_magnetization,1],axis=0)
        return E,means, stds,M,magnetization

    def get_data(self,iteration=0):
        non_zero = self.get_non_zero(table=Datum.ENERGY)
        E = self.energies[iteration,non_zero,0]
        N = np.zeros_like(E)
        for i in range(len(E)):
            mask = np.in1d(self.energies[iteration,:,0],E[i])
            N[i] = self.energies[iteration,mask,1].sum()
        return E,N

class Weights:
    '''
    Used to cache values of np.exp(-self.beta*deltaE) to reduce recalculation.
    NB: only a few values of deltaE are possible.
    '''
    def __init__(self,beta,max_neigbbours):
        deltaE =np.array([2*i for i in range(1,max_neigbbours+1)])
        self.cache = np.exp(-beta*deltaE)

    def get_upsilon(self,deltaE):
        '''
        Used to decide whether to accept a proposed move.

        Parameters:
            deltaE   Change in energy
        '''
        return self.cache[deltaE//2-1] if deltaE > 0 else np.inf

class MarkovIsing:
    '''
    This class uses Markov Chain Monte Carlo (MCMC) to sample an Ising Model

    Attributes:
        neighbours     Table used to iterate through neighbours of a location
        m              Number of rows
        n              Number of columns
        N              Number of sites
        periodic       Use periodic boundary conditions
        energies       Store counts for each energy
        magnetization  Store counts for each magnetization
        beta           Inverse temperature
    '''
    def __init__(self,rng=np.random.default_rng(),shape=(4,5),periodic=False,Niterations=5,beta=0.001):
        self.Nbr = lambda k:Nbr(k,shape=shape,periodic=periodic)
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.beta = beta
        self.data = IsingData(Niterations=Niterations,N=self.N)
        self.weights = Weights(beta,get_max_neighbours(shape))
        self.neighbours = Neighbours(shape=shape,periodic=periodic)
        self.accepted_moves = 0


    def step(self,sigma,E,M):
        '''
        Perform one step of MCMC

        Parameters:
            sigma     Spins before step
            E         Energy before step
            M         Magnetization before step

        Returns:
            sigma     Spins after step
            E         Energy after step
            M         Magnetization afterstep
        '''
        k = self.rng.integers(self.N)
        neighbours = [nn for nn in self.neighbours[k,:] if nn > -1]
        h = sum(sigma[i] for i in neighbours)
        deltaE = 2*h*sigma[k]
        Upsilon = self.weights.get_upsilon(deltaE)
        if deltaE <= 0 or self.rng.random() < Upsilon:
            sigma[k] *= -1
            E += deltaE
            M += 2*sigma[k]
            self.accepted_moves += 1
        return sigma,E,M



    def run(self,Nsteps=100000,Nburn=100,frequency=10000,iteration=0):
        '''
        Initialize configuration and carry out a specified number of steps

        Parameters:
             Nsteps     Number of steps to be performed and recorded
             Nburn      Number of steps to be performed at start and not recorded
             frequency  Report to user after this many steps
             iteration  Iteration number: used for storing data and reporting
        '''
        self.accepted_moves = 0
        sigma = self.rng.choice([-1,1],size=self.N)
        E,M = get_energy_magnetism(sigma, shape=(self.m,self.n), periodic=self.periodic)

        Ns = defaultdict(lambda: 0)
        Ns[E] = 1

        NMs = defaultdict(lambda: 0)
        NMs[M] = 1

        for i in range(Nsteps + Nburn):
            sigma,E,M = self.step(sigma,E,M)
            if i < Nburn: continue
            Ns[E] += 1
            NMs[M] += 1
            if frequency > 0 and i%frequency == 0 and i > 0:
                print (f'Iteration {iteration}, step {i}')

        self.data.store_data(table=Datum.ENERGY,iteration=iteration,Ns=Ns)
        self.data.store_data(table=Datum.MAGNETIZATION,iteration=iteration,Ns=NMs)


    def get_stats(self):
        '''
        Extract mean and standard deviation for those energies
        that have appeared at least once in MCMC
        '''
        return self.data.get_stats()


class TestMarkov(TestCase):
    '''
    Using data from Table 5.2, verify that MCMC is consistent with enumeration
    '''

    def test4x4_beta_0(self):
        '''
        Test with beta = 0: should give same results as Table 5.2
        '''
        Niterations = 100
        markov = MarkovIsing(shape=(4,4),
                             periodic=True,
                             Niterations=Niterations,
                             beta=0)
        for i in range(Niterations):
            markov.run(Nsteps=10000,Nburn=1000,frequency=0,iteration=i)
        Es,Ns, _,_,_ = markov.get_stats()
        normalized = ((2**16)*Ns/Ns.sum()).astype(int)
        self.assertAlmostEqual(424,normalized[3],delta=15)
        self.assertAlmostEqual(13568,normalized[6],delta=75)
        self.assertAlmostEqual(20524,normalized[7],delta=75)
        self.assertAlmostEqual(13568,normalized[8],delta=75)
        self.assertAlmostEqual(424,normalized[11],delta=15)

if __name__=='__main__':
    main()
