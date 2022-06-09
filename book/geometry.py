# Copyright (C) 2022 Simon Crase

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

'''Support use of periodic and unbounded boundary conditions '''

from math              import isqrt
from numpy             import array, minimum, ones, pi, prod, reshape, sqrt, zeros
from numpy.linalg      import norm
from unittest          import TestCase, main

class Geometry:
    '''This class represents the apce in which the action occurs'''
    def __init__(self,
                 L     = array([1,1]),
                 sigma = 0.25,
                 d     = 2):
        self.L     = L
        self.sigma = sigma
        self.d     = d

    def get_density(self,
                    N     = 4):
        '''Calculate fraction of total volums that will be occupied'''
        return N*pi*self.sigma**2/prod(self.L)

    def create_configuration(self,N=4):
        '''Create an initial configuration, spread uniformly through space'''
        if self.d==2:
            return self.pack_disks(N)
        else:
            raise Exception(f'Not implemented for d={d}')

    def pack_disks(self, N=4):
        '''
            Create an initial configuration of disks, spread uniformly through a rectangle,
            using Lagrange's formula https://en.wikipedia.org/wiki/Circle_packing#Densest_packing
        '''
        def alloc(i,j):
            '''Determine position of one disk'''
            offset = 0 if i%2==0 else 0.5*Delta[1]
            x0 = self.LowerBound[0] +  (i+1) * Delta[0]
            y0 = self.LowerBound[1] + offset + (j+1) * Delta[1]
            x1,y1 = self.move_to((x0,y0))
            return (x1,y1)

        eta = self.get_density(N=N)
        if eta > pi*sqrt(3)/6:
            raise Exception(f'Density of {eta} exceeds {pi*sqrt(3)/6}')

        m = isqrt(N)
        n = N // m
        if  m*n < n:
            n += 1
        assert(m<=n)
        Available   = self.UpperBound - self.LowerBound
        Delta       = [Available[0]/m, Available[1]/n]
        coordinates = [alloc(i,j) for i in range(m) for j in range(n)]
        return array(coordinates[0:N])

    def create_Histograms(self,n=10):
        return [Histogram(n) for _ in range(self.d)]

class Box(Geometry):
    '''This class reprsents a simple box geometry without periodic boundary conditions'''
    def __init__(self,
                 L     = array([1,1]),
                 sigma = 0.25,
                 d     = 2):
        super().__init__(L = L, sigma=sigma, d = d)
        self.LowerBound = sigma*ones(d)
        self.UpperBound =  L - 2*sigma*ones(d)

    def get_distance(self, X0,X1):
        '''Calculate distance between two points using appropriate boundary conditions'''
        return norm(X0-X1)

    def move_to(self,X):
        return X

    def get_description(self):
        return 'without periodic boundary conditions'

class Torus(Geometry):
    '''This class reprsents a  box geometry with periodic boundary conditions, i.e. a torus.'''
    def __init__(self,
                 L     = array([1,1]),
                 sigma = 0.25,
                 d     = 2):
        super().__init__(L = L, sigma=sigma, d = d)
        self.LowerBound = zeros(d)
        self.UpperBound = L

    def get_distance(self, X0,X1):
        '''Calculate distance between two points using appropriate boundary conditions'''
        return norm(self.diff_vec(X0,X1))

    def move_to(self,X):
        return self.box_it(X)

    def box_it(self,X):
        '''Algorithm 2.5'''
        return X%self.L

    def diff_vec(self,X0,X1):
        '''Algorithm 2.6'''
        Delta  = self.box_it(X0 - X1)
        return minimum(Delta, Delta - self.L/2)

    def get_description(self):
        '''Used in titles of plots'''
        return 'with periodic boundary conditions'

def GeometryFactory(periodic = False,
                    L        = array([1,1]),
                    sigma    = 0.25,
                    d        = 2):
    '''Create a periodic or aperiodic Geometry'''
    return Torus(L     = L,
                 sigma = sigma,
                 d     = d) if periodic else Box(L     = L,
                                                 sigma = sigma,
                                                 d     = d)

class Histogram:
    '''
       This class represents a Histogram, to which we can add points dynamically.
       This allows memeory to be saved, as we don;t have to maintain individual
       samples in memory.
    '''
    def __init__(self,
                 n  = 10,
                 x0 = 0,
                 xn = 1):
        self.n  = n
        self.h  = [0] * n
        self.x0 = x0
        self.xn = xn

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        return self.h[i]

    def add(self,x):
        '''Add one value to histogram. This increases the count of the relevant bin by 1'''
        self.h[min(int(self.n * (x-self.x0)/(self.xn-self.x0)),len(self)-1)]+=1

    def get_hist(self):
        '''Retrieve counts and bin boundaries'''
        bins = [self.x0 + i*(self.xn-self.x0)/self.n for i in range(self.n)]
        return self.h,bins+[self.xn]

class TestHistogram(TestCase):
    def setUp(self):
        self.histogram = Histogram()

    def test_init(self):
        self.assertEqual(10,len(self.histogram))

    def test_add(self):
        self.assertEqual(0,self.histogram[0])
        self.histogram.add(0.05)
        self.assertEqual(1,self.histogram[0])
        self.histogram.add(0.15)
        self.assertEqual(1,self.histogram[1])
        self.histogram.add(0.15)
        self.assertEqual(2,self.histogram[1])
        self.histogram.add(1)
        self.assertEqual(1,self.histogram[-1])

if __name__ =='__main__':
    main()
