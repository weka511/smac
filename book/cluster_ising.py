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

'''Algorithm 5.9 Cluster Ising'''


import numpy as np
from ising import  Neighbours
from unittest import main,TestCase

class IsingData:
    '''
    This class stores the Energy and Magnetization

    Attributes:
        E   Array of counts, one for each energy.
            Energies are all even, so we need only half as many
        M   Array of counts, one for each Magnetization
        N   Number of points in lattice
    '''
    def __init__(self,N):
        self.N = N
        self.E = np.zeros((2*self.N+1),dtype=np.int64)
        self.M = np.zeros((2*self.N+1),dtype=np.int64)

    def generate_E(self):
        '''
        Support iteration through energy values and counts
        '''
        for i in range(0,2*self.N+1):
            yield 2*(i-self.N),self.E[i]

    def generate_M(self):
        '''
        Support iteration through magnetization values and counts
        '''
        for i in range(0,2*self.N+1):
            yield i-self.N,self.M[i]

    def store(self,E,M):
        '''
        Update counts of energy and magnetization

        Parameters:
            E       Energy to be updated
            M       Magnetization to be updated
        '''
        self.E[self.N + E//2] += 1
        self.M[self.N + M] += 1

    def initialize(self,E,M):
        '''
        Used at the start of a run to initialize data from stored values
        '''
        np.copyto(self.E,E[:,1])
        np.copyto(self.M,M[:,1])

class ClusterIsing:
    '''
    Algorithm 5.9 Cluster Ising

    Attributes:
        rng         Generator for
        neighbours  Table used to iterate through neighbours of a location
        m           Number of rows
        n           Number of columns
        N           Number of sites
        periodic    Use periodic boundary conditions
        beta        Inverse temperature
        p           See discussion following (5.22)
        data        Used to store counts for energy and magnetization
    '''
    def __init__(self,rng=np.random.default_rng(),shape=(4,5),periodic=False,beta=0.001):
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.beta = beta
        self.p  = 1.0 - np.exp(-2.0*beta) # Makes acceptance probability == 1 - (5.22)
        self.data = IsingData(self.N)
        self.neighbours = Neighbours(shape=shape,periodic=periodic)

    def step(self,sigma):
        '''
        Construct Cluster and the Pocket, a subset that will be used to expand the Cluster.
        Initially each of them contains the same randomly selected spin. We extend the Cluster
        by selecting one element from the Pocket repeatedly, and growing both sets by randomly selecting
        neighbours with the same spin.
        '''
        j = self.rng.integers(self.N)    # Start with this randomly selected site
        Pocket, Cluster = [j], [j]
        while Pocket != []:
            k = self.rng.choice(Pocket)  # Process one site from pocket
            Pocket.remove(k)
            for l in self.neighbours[k,:]:             # Consider all neighbours
                if l == -1: break                      # Sentinel indicates that we have exhausted neighbours
                if (sigma[l] == sigma[k]               # Only add if spins match
                    and l not in Cluster               # Don't match if already in Cluster
                    and self.rng.uniform() < self.p):  # Add tocluster with probabiilty p
                    Pocket.append(l)
                    Cluster.append(l)

        for k in Cluster:        # Flip the completed cluster
            sigma[k] *= -1
        return sigma

    def get_energy_magnetism(self,sigma):
        '''
        Calculate eneryy and magnetizaion using neighbours
        '''
        def get_energy():
            E = 0
            for i in range(self.N):
                E -= sum([sigma[i] * sigma[j] for j in self.neighbours[i,:] if j > i])
            return E

        return get_energy(), sum(sigma)

    def run(self,Nsteps=1000,database=None):
        '''
        Construct one chain
        '''
        if database != None:
            try :
                NIterations,sigma,E0,M0 = database[1/self.beta, self.m, self.n]
                self.data.initialize(E0,M0)
            except KeyError:
                NIterations = 0
                sigma = self.rng.choice([-1,1],size=self.N)
        else:
            NIterations = 0
            sigma = self.rng.choice([-1,1],size=self.N)

        E,M = self.get_energy_magnetism(sigma)
        self.data.store(E,M)
        for i in range(Nsteps):
            self.step(sigma)
            E,M = self.get_energy_magnetism(sigma)
            self.data.store(E,M)

        if database != None:
            database[1/self.beta, self.m, self.n] = (Nsteps+NIterations,
                                                     sigma,
                                                     np.array([[e,n] for e,n in self.data.generate_E()],dtype=int),
                                                     np.array([[m,n] for m,n in self.data.generate_M()],dtype=int))

        return Nsteps + NIterations



class ClusterIsingTests(TestCase):
    def test_all_down(self):
        cluster_ising = ClusterIsing(shape=(6,6),periodic=True,beta=2)
        sigma = -1 *np.ones((36))
        E,M = cluster_ising.get_energy_magnetism(sigma)
        self.assertEqual(-72,E)
        self.assertEqual(-36,M)

    def test_all_up(self):
        cluster_ising = ClusterIsing(shape=(6,6),periodic=True,beta=2)
        sigma = np.ones((36))
        E,M = cluster_ising.get_energy_magnetism(sigma)
        self.assertEqual(-72,E)
        self.assertEqual(+36,M)

    def test_all_mixed(self):
        cluster_ising = ClusterIsing(shape=(6,6),periodic=True,beta=2)
        sigma = np.array([
            1, -1, 1, -1, 1, -1,
            -1, 1, -1, 1, -1, +1,
            1, -1, 1, -1, 1, -1,
            -1, 1, -1, 1, -1, +1,
            1, -1, 1, -1, 1, -1,
            -1, 1, -1, 1, -1, +1,
        ])
        E,M = cluster_ising.get_energy_magnetism(sigma)
        self.assertEqual(+72,E)
        self.assertEqual(0,M)

    def test_data_generate(self):
        '''
        Verify that IsingData.generate_E() starts at the correct place
        '''
        data = IsingData(36)
        for e,c in data.generate_E():
            self.assertEqual(-72,e)
            break

if __name__=='__main__':
    main()
