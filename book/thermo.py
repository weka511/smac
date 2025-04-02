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

''' Exercise 5-11: calculate thermodynamic quantities'''

from unittest import TestCase, main
import numpy as np

def thermo(E,N,beta=1.0):
    '''
    Algorithm 5.4 Calculate thermodynamic quantities

    Parameters:
        E             Energies that are present in data
        N             Count of each energy
        beta          Inverse temperature
        NObservations Total number of States (exact enumeration) or data points (MCMC)

    Returns:
        Z      Partition function
        Emean  Mean energy
        cV     Specific heat capacity
    '''
    Emin = E.min()
    Eprime = E - Emin
    weights = np.exp(-beta*Eprime) *N
    Z = np.sum(weights)
    Emean = np.average(Eprime,weights=weights)
    EVariance = np.average((Eprime-Emean)**2,weights=weights)

    NObservations = len(N) - 1
    return (
         Z*np.exp(-beta*Emin),                # Partition function
          (Emean + Emin)/NObservations,        # Mean energy e.g. 37-1!
          beta**2 * EVariance/NObservations    # Specific heat capacity
     )

class TestThermo(TestCase):
    '''
    Using data from Table 5.2, replicate <e> and cV from Table 5.3
    '''
    def setUp(self):
        '''
        Table 5.2
        '''
        self.density = np.array([
            [-72,2],
            [-68,0],
            [-64,72],
            [-60,144],
            [-56,1620],
            [-52,6048],
            [-48,35148],
            [-44,159840],
            [-40,804078],
            [-36,3846576],
            [-32,17569080],
            [-28,71789328],
            [-24,260434986],
            [-20,808871328],
            [-16,2122173684],
            [-12,4616013408],
            [-8,8196905106],
            [-4,11674988208],
            [0,13172279424],
            [4,11674988208],
            [8,8196905106],
            [12,4616013408],
            [16,2122173684],
            [20,808871328],
            [24,260434986],
            [28,71789328],
            [32,17569080],
            [36,3846576],
            [40,804078],
            [44,159840],
            [48,35148],
            [52,6048],
            [56,1620],
            [60,144],
            [64,72],
            [68,0],
            [72,2]])

    def test0_5(self):
        '''
        T = 0.5
        '''
        _,e,cV =thermo(self.density[:,0],self.density[:,1],beta=2)
        self.assertAlmostEqual(-1.999, e,delta=0.001)
        self.assertAlmostEqual(0.00003,cV,places=5)

    def test4_0(self):
        '''
        T = 2.0
        '''
        _,e,cV =thermo(self.density[:,0],self.density[:,1],beta=1/4)
        self.assertAlmostEqual(-0.566, e,delta=0.001)
        self.assertAlmostEqual(0.18704,cV,places=5)

    def test2_5(self):
        '''
        T = 2.5
        '''
        _,e,cV =thermo(self.density[:,0],self.density[:,1],beta=2/5)
        self.assertAlmostEqual(-1.280, e,delta=0.001)
        self.assertAlmostEqual(1.00623,cV,places=5)

    def test2_0(self):
        '''
        T = 4.0
        '''
        _,e,cV =thermo(self.density[:,0],self.density[:,1],beta=1/2)
        self.assertAlmostEqual(-1.747, e,delta=0.001)
        self.assertAlmostEqual(0.68592,cV,places=5)

if __name__=='__main__':
    main()
