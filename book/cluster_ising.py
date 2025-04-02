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


import numpy as np
from ising import Nbr, get_energy_magnetism, Neighbours
from unittest import main,TestCase


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
        E           Used to store counts for energy
        M           Used to store counts for magnetization
    '''
    def __init__(self,rng=np.random.default_rng(),shape=(4,5),periodic=False,beta=0.001):
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.beta = beta
        self.p  = 1.0 - np.exp(-2.0*beta) # Makes acceptance probability == 1 - (5.22)
        self.E = np.zeros((2*self.N+1),dtype=np.int64)
        self.M = np.zeros((2*self.N+1),dtype=np.int64)
        self.neighbours = Neighbours(shape=shape,periodic=periodic)

    def step(self,sigma):
        '''
        Construct Cluster and the Pocket, a subset that will be used to expand the Cluster.
        Initially each of them contains the same randomly selected spin. We extend the Cluster
        by selecting one element from the pocket repeatedly, and growing both sets by randomly selecting
        neighbours with the same spin.
        '''
        j = self.rng.integers(self.N)
        Pocket, Cluster = [j], [j]
        while Pocket != []:
            k = self.rng.choice(Pocket)
            for l in self.neighbours[k,:]:
                if l == -1: break
                if (sigma[l] == sigma[k]
                    and l not in Cluster
                    and self.rng.uniform() < self.p):
                    Pocket.append(l)
                    Cluster.append(l)
            Pocket.remove(k)
        for k in Cluster:
            sigma[k] *= -1

    def get_energy_magnetism(self,sigma):
        E = 0
        for i in range(self.N):
            E -= sum([sigma[i] * sigma[j] for j in self.neighbours[i,:] if j > i])

        return E, sum(sigma)

    def run(self,Nsteps=1000):
        '''
        Construct one chain
        '''
        sigma = self.rng.choice([-1,1],size=self.N)
        E,M = self.get_energy_magnetism(sigma)
        self.E[self.N + E] += 1
        self.M[self.N + M] += 1
        for i in range(Nsteps):
            self.step(sigma)
            E,M = self.get_energy_magnetism(sigma)
            self.E[self.N + E] += 1
            self.M[self.N + M] += 1

class ClusterIsingTests(TestCase):
    def test1(self):
        cluster_ising = ClusterIsing(shape=(6,6),periodic=True,beta=2)
        sigma = -1 *np.ones((36))
        E,M = cluster_ising.get_energy_magnetism(sigma)
        self.assertEqual(-72,E)

if __name__=='__main__':
    main()

