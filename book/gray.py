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
    Algorithm 5.2: Gray code for spins {1,...N}.
    Also generate neighbours of a spin
'''

from unittest import main, TestCase

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

def Nbr(k, shape = (4,5), periodic = False):
    '''
    A generator to iterate through neighbours of a spin

    Parameters:
        k        Index of spin (zero based)
        shape    Number of rows, columns, etc.
        periodic Indicates whther or not spins live on a torus
    '''
    assert len(shape)==2,'2 D is the only version implemented'
    m,n = shape
    i,j = k//n,k%n
    if periodic:
        for i0 in [i-1,i+1]:
            yield (i0%m)*n + j
        for j0 in [j-1,j+1]:
            yield i *n + j0%n
    else:
        for i0 in [i-1,i+1]:
            if i0>-1 and i0<m:
                yield i0*n + j
        for j0 in [j-1,j+1]:
            if j0>-1 and j0 < n:
                yield i *n + j0

def generate_edges(shape = (4,4), periodic = False):
    def get_coordinates(i):
        return i//n, i % n

    m,n = shape
    for i in range(m*n):
        for j in Nbr(i,shape=shape,periodic=periodic):
            if j >i: continue
            m0,n0 = get_coordinates(i)
            m1,n1 = get_coordinates(j)
            yield m0,n0,m1,n1


class NbrTest(TestCase):
    '''
    Test for Nbr class

    Test data correspond to
         15  16  17  18  19
         10  11  12  13  14
          5   6   7   8   9
          0   1   2   3   4
    '''
    def testNbr0(self):
        Nbrs = list(Nbr(8))
        self.assertListEqual([3,13,7,9], Nbrs)

    def testNbr1(self):
        Nbrs = list(Nbr(12))
        self.assertListEqual([7,17,11,13], Nbrs)

    def testNbr2(self):
        Nbrs = list(Nbr(14))
        self.assertListEqual([9,19,13], Nbrs)

    def testNbr3(self):
        Nbrs = list(Nbr(15))
        self.assertListEqual([10,16], Nbrs)

    def testNbr4(self):
        Nbrs = list(Nbr(4))
        self.assertListEqual([9,3], Nbrs)

    def testNbrP1(self):
        Nbrs = list(Nbr(12,periodic=True))
        self.assertListEqual([7,17,11,13], Nbrs)

    def testNbrP2(self):
        Nbrs = list(Nbr(14,periodic=True))
        self.assertListEqual([9,19,13,10], Nbrs)

    def testNbrP3(self):
        Nbrs = list(Nbr(15,periodic=True))
        self.assertListEqual([10,0,19,16], Nbrs)

    def testNbrP4(self):
        Nbrs = list(Nbr(4,periodic=True))
        self.assertListEqual([19,9,3,0], Nbrs)

    def testEdges(self):
        for edge in generate_edges():
            print (edge)


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

if __name__=='__main__':
    main()
