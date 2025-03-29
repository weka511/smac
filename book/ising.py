#!/usr/bin/env python

# Copyright (C) 2019-2025 Greenweaves Software Limited
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''
    Various common code for Ising model:
    - Algorithm 5.2: Gray code for spins {1,...N}.
    - Generate neighbours of a spin
    - Calculate energy for a configuration
'''

from unittest import main, TestCase,skip
import numpy as np

def gray_flip(N, tau = []):
    '''
    Generator for Gray code

    Inputs: N
            tau   Used when we restart a long run

    Used to iterate through gray codes, returning
    the coordinate that gets flipped each time (1-based)
    plus tau (to support restarting)

    Usage:
        for k in gray(N):
            ....
    '''
    if len(tau) == 0:
        tau = list(range(1,(N+1)+1))

    while True:
        k = tau[0]         # The next spin to flip (1-based)
        if k > N: return
        tau[k-1] = tau[k]
        tau[k] = k + 1
        if (k != 1): tau[0] = 1
        yield k, tau

class Gray:
    '''Class for Gray code. Permits restarting'''
    def __init__(self,N, tau = None):
        self.N = N
        self.tau = list(range(1,(N+1)+1)) if tau==None else tau

    def __iter__(self):
        return self

    def __next__(self):
        '''The next spin to flip (1-based)'''
        k = self.tau[0]
        if k > self.N: raise StopIteration
        self.tau[k-1] = self.tau[k]
        self.tau[k] = k+1
        if (k != 1): self.tau[0] = 1
        return k

    def __str__(self):
        '''Convert tau to string, so we can save and restart'''
        return f'[{",".join(str(t) for t in self.tau)}]'

def Nbr(index, shape = (4,5), periodic = False):
    '''
    A generator to iterate through neighbours of a spin

    Parameters:
        index    Index of spin (zero based)
        shape    Number of rows, columns, etc.
        periodic Indicates whether or not spins live on a torus
    '''
    def in_range(j,n):
        '''
        Used to eliminate wrapped values if not periodic
        '''
        return periodic or (j>-1 and j < n)

    def get_wrapped(j,i):
        '''
        Used to handle wrap around for periodic
        '''
        if j < 0:
            return shape[i] - 1
        elif j >= shape[i]:
            return  0
        else:
            return j

    def create_neighbour(i,j,coordinates):
        '''
        Constuct one neighbour of a point by taking one step

        Parameters:
            i             Position at which to step
            j             Direction in shich to step
            coordinates   Coordinates of point
        '''
        return tuple(get_wrapped(j,k) if k == i else coordinates[k] for k in range(len(coordinates)))

    coordinates = np.unravel_index(index,shape) # coordinates of index in len(shape) dimensional space.

    for i in range(len(coordinates)):
        for j in [coordinates[i] - 1,coordinates[i] + 1]:
            if in_range(j,shape[i]):  # Can we step in this direction?
                yield np.ravel_multi_index(create_neighbour(i,j,coordinates),shape) # Ravel neighbour back to an index


def get_max_neighbours(shape = (4,5)):
    '''
    Used to determine the maximum number of energy or magnetization steps
    possible

    Parameters:
        shape    Shape of space
    Returns:
        2**d, where d is the dimension of the space
    '''
    d = len(shape)
    return 2**d

class Neighbours:
    '''
    This class allows neighbours to be looked up from a table,
    with one row for each site, comprising the neighbours,
    # and using -1 as the marker for end of neighbours
    '''
    def __init__(self,shape = (4,5), periodic = False):
        N = np.prod(shape)
        d = get_max_neighbours(shape=shape)
        self.neighbours = -1 * np.ones((N,d+1),dtype=int)
        for i in range(N):
            for j,neighbour in enumerate(Nbr(i,shape=shape,periodic=periodic)):
                self.neighbours[i,j] = neighbour

    def __getitem__(self,index):
        return self.neighbours[index]

def generate_edges(shape=(4,4), periodic=False):
    '''
    Used to iterate through all the edges of a matrix of spins

    Parameters:
        shape         Number of rows and columns in space
        periodic      Indicates whether space wraps around
    '''
    m,n = shape
    for i in range(m*n):
        for j in Nbr(i,shape=shape,periodic=periodic):
            if i<j:
                yield i,j

def get_energy_magnetism(sigma, shape=(4,4), periodic=False):
    '''
    Used to calculate energy and magnetization for a configuration

    Parameters:
        sigma         The spins
        shape         Number of rows and columns in space
        periodic      Indicates whether space wraps around

    Returns:
        E                   Energy due to spins
        M                   Magnetization
    '''
    N = len(sigma)
    assert N == shape[0]*shape[1]
    E = -sum([sigma[i] * sigma[j] for i,j in generate_edges(shape=shape,periodic=periodic)])
    M = sum(sigma)
    return E,M

class NeighboursTest(TestCase):
    '''
    Test looking neighbours up from table
    '''
    def setUp(self):
        self.neighbours = Neighbours()
        self.neighboursP = Neighbours(periodic=True)

    def test8(self):
        self.assertCountEqual([3,13,7,9,-1], self.neighbours[8])

    def test14(self):
        self.assertCountEqual([9,19,13,-1,-1], self.neighbours[14])

    def testNbrP14(self):
        self.assertCountEqual([9,19,13,10,-1], self.neighboursP[14])

class NbrTest(TestCase):
    '''
    Test finding neighbours

    Test data correspond to
         15  16  17  18  19
         10  11  12  13  14
          5   6   7   8   9
          0   1   2   3   4
    '''

    def testNbr8(self):
        Nbrs = list(Nbr(8))
        self.assertCountEqual([3,13,7,9], Nbrs)

    def testNbr12(self):
        Nbrs = list(Nbr(12))
        self.assertCountEqual([7,17,11,13], Nbrs)

    def testNbr14(self):
        Nbrs = list(Nbr(14))
        self.assertCountEqual([9,19,13], Nbrs)

    def testNbr15(self):
        Nbrs = list(Nbr(15))
        self.assertCountEqual([10,16], Nbrs)

    def testNbr4(self):
        Nbrs = list(Nbr(4))
        self.assertCountEqual([9,3], Nbrs)

    def testNbrP12(self):
        Nbrs = list(Nbr(12,periodic=True))
        self.assertCountEqual([7,17,11,13], Nbrs)

    def testNbrP14(self):
        Nbrs = list(Nbr(14,periodic=True))
        self.assertCountEqual([9,19,13,10], Nbrs)

    def testNbrP15(self):
        Nbrs = list(Nbr(15,periodic=True))
        self.assertCountEqual([10,0,19,16], Nbrs)

    def testNbrP4(self):
        Nbrs = list(Nbr(4,periodic=True))
        self.assertCountEqual([19,9,3,0], Nbrs)

    def test_max_neighbours(self):
        self.assertEqual(4, get_max_neighbours())

class Nbr3dTest(TestCase):
    '''
    Test finding neighbours in 3D

    Test data correspond to
         15  16  17  18  19
         10  11  12  13  14
          5   6   7   8   9
          0   1   2   3   4

          plus 2 similar matrices stacked on top
    '''
    def testNbr8P(self):
        Nbrs = list(Nbr(8,shape = (3,4,5),periodic=True))
        self.assertCountEqual([3,13,7,9,8+20,8+2*20], Nbrs)

    def testNbr8(self):
        Nbrs = list(Nbr(8,shape = (3,4,5),periodic=False))
        self.assertCountEqual([3,13,7,9,8+20], Nbrs)

    def testNbr28(self):
        Nbrs = list(Nbr(28,shape = (3,4,5),periodic=False))
        self.assertCountEqual([23,33,27,29,48,8], Nbrs)

class EdgeTest(TestCase):
    '''
    Tests for generate_edges(...)
    '''
    def testEdges2(self):
        '''
        Test data corresponds to
             2   3
             0   1
        '''
        Edges = list(generate_edges((2,2)))
        self.assertEqual(4,len(Edges))
        self.assertIn((0,1),Edges)
        self.assertIn((0,2),Edges)
        self.assertIn((1,3),Edges)
        self.assertIn((2,3),Edges)

    def testEdges4(self):
        '''
        Test data corresponds to
              12  13  14  15
               8   9  10  11
               4   5   6   7
               0   1   2   3
        '''
        Edges = list(generate_edges())
        self.assertIn((0,1),Edges)
        self.assertIn((1,2),Edges)
        self.assertIn((2,3),Edges)

        self.assertIn((0,4),Edges)
        self.assertIn((1,5),Edges)
        self.assertIn((2,6),Edges)
        self.assertIn((3,7),Edges)

        self.assertIn((4,5),Edges)
        self.assertIn((5,6),Edges)
        self.assertIn((6,7),Edges)

        self.assertIn((4,8),Edges)
        self.assertIn((5,9),Edges)
        self.assertIn((6,10),Edges)
        self.assertIn((7,11),Edges)

        self.assertIn((8,9),Edges)
        self.assertIn((9,10),Edges)
        self.assertIn((10,11),Edges)

        self.assertIn((8,12),Edges)
        self.assertIn((9,13),Edges)
        self.assertIn((10,14),Edges)
        self.assertIn((11,15),Edges)

        self.assertIn((12,13),Edges)
        self.assertIn((13,14),Edges)
        self.assertIn((14,15),Edges)

        self.assertEqual(24,len(Edges))


class GrayTest(TestCase):
    '''
    Test for Gray class
    '''
    def setUp(self):
        '''Set up test data from Table 3.1'''
        flips = [1,2,1,3,1,2,1]
        self.expected = flips + [1+max(flips)] + flips[::-1]

class GrayGeneratorTest(GrayTest):
    '''
    Verify that the generated values are correct,
    '''
    def testGrayIterator(self):
        gray = Gray(4)
        for i,k in enumerate(gray):
            self.assertEqual(self.expected[i],k)
        self.assertEqual(2**4 - 1,i + 1)
        self.assertListEqual([5,2,3,4,5],gray.tau)
        self.assertEqual('[5,2,3,4,5]',str(gray))

class GrayFlipTest(GrayTest):
    '''
    Test for gray_flip()
    '''
    def testGrayGenerator(self):
        '''
        Verify that the generated values are correct,
        and that the number of iterations is 2**N-1
        '''
        for i,(k,_) in enumerate(gray_flip(4)):
            self.assertEqual(self.expected[i],k)
        self.assertEqual(2**4-1,i+1)


class EM_Test(TestCase):
    def test2_2(self):
        E,M = get_energy_magnetism([-1,-1,-1,-1], shape=(2,2), periodic=False)
        self.assertEqual(-4,E)
        self.assertEqual(-4,M)

        E,M = get_energy_magnetism([-1,-1,+1,-1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(-2,M)

        E,M = get_energy_magnetism([-1,-1,+1,+1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(0,M)

        E,M = get_energy_magnetism([-1,-1,-1,+1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(-2,M)

        E,M = get_energy_magnetism([+1,-1,-1,+1], shape=(2,2), periodic=False)
        self.assertEqual(4,E)
        self.assertEqual(0,M)

        E,M = get_energy_magnetism([+1,-1,+1,+1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(+2,M)

        E,M = get_energy_magnetism([+1,-1,+1,-1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(0,M)

        E,M = get_energy_magnetism([+1,-1,-1,-1], shape=(2,2), periodic=False)
        self.assertEqual(0,E)
        self.assertEqual(-2,M)

if __name__=='__main__':
    main()
