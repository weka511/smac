#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

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

'''
    This class models the space in which spheres move. It supports the use of both periodic
    and bounded boundary conditions.
'''

from abc import ABC, abstractmethod
from sys import maxsize
from unittest import TestCase, main
import numpy as np

class Geometry(ABC):
    '''
    This class represents the space in which the action occurs

    Attributes:
        L      A vector representing the length of one side of the space
        sigma  Radius of a sphere
        d      Dimension of space
    '''
    @staticmethod
    def create_L(L,d):
        '''
        Create a vector of lengths from a command line parameter

        Parameters:
            L   Either a list of lenghts, or a single number if all lengths are identical
            d   Dimension of space
        '''
        return np.array(L if len(L)==d else L * d)

    @staticmethod
    def get_side_dimensions(N):
        '''
        Determine the sides of a rectangle

        Parameters:
            N     The area of a rectangle
        Returns:
            m, n such that m*n >= N and m <= n
        '''
        m = int(np.sqrt(N))
        n = N // m
        if  m*n < N:
            n += 1
        assert m <= n
        return m,n

    @staticmethod
    def get_coordinate_description(coordinate):
        '''
        Used to display the name of a coordinate

        Parameters:
            coordinate    Index of coordinate
        '''
        match coordinate:
            case 0:
                return 'X'
            case 1:
                return 'Y'
            case 2:
                return 'Z'
        raise ValueError(f'Coordinate index {coordinate} undefined')

    @staticmethod
    def get_coordinate_colour(coordinate):
        '''
        Used to select a colour for plotting data against a coordinate

        Parameters:
            coordinate    Index of coordinate
        '''
        match coordinate:
            case 0:
                return 'xkcd:red'
            case 1:
                return 'xkcd:blue'
            case 2:
                return 'xkcd:green'
        raise ValueError(f'Coordinate index {coordinate} undefined')


    def __init__(self, L  = np.array([1,1]), sigma = 0.25,  d = 2):
        self.L = L
        self.sigma = sigma
        self.d = d

    def get_density(self, N = 4):
        '''
        Calculate fraction of total volums that will be occupied by spheres

        Parameters:
            N      Number of spheres
        '''
        return N * (np.pi * self.sigma**2)/np.prod(self.L)

    def set_sigma(self, eta = 1.0, N   = 4):
        '''
        Calculate the radius of spheres needed to give a specified density

        Parameters:
            eta    The density that we want
            N      Number of spheres
        '''
        self.sigma = np.sqrt(np.prod(self.L)*eta/(N*np.pi))

    def create_configuration(self,N=4):
        '''
        Create an initial configuration, spread uniformly through space

        Parameters:
            N      Number of spheres
        '''
        if self.d == 2:
            return self.pack_disks(N)
        else:
            raise ValueError(f'Not implemented for d={d}')

    def pack_disks(self, N=4):
        '''
            Create an initial configuration of disks, spread uniformly through a rectangle,
            using Lagrange's formula https://en.wikipedia.org/wiki/Circle_packing#Densest_packing

        Parameters:
            N      Number of disks
        '''
        def alloc(i,j):
            '''Determine position of one disk'''
            offset = 0 if i%2==0 else 0.5*Delta[1]
            x0 = self.LowerBound[0] +  i * Delta[0]
            y0 = self.LowerBound[1] + offset + j * Delta[1]
            return self.move_to((x0,y0))

        eta = self.get_density(N=N)
        if eta > np.pi*np.sqrt(3)/6:
            raise ValueError(f'Density of {eta} exceeds {np.pi*np.sqrt(3)/6}')

        m,n = Geometry.get_side_dimensions(N)

        Available = self.UpperBound - self.LowerBound
        Delta = [Available[0]/m, Available[1]/n]
        coordinates = [alloc(i,j) for i in range(m) for j in range(n)]
        return np.array(coordinates[0:N])

    def create_Histograms(self,n=10,HistogramBins=np.zeros(0)):
        '''
        Used to instantiate a dynamic histogram
        '''
        self.HistogramBins = np.zeros((n,self.d), dtype=np.int64) if HistogramBins.size==0 else HistogramBins
        return [Histogram(n, h = self.HistogramBins[:,j]) for j in range(self.d)]

    @abstractmethod
    def get_description(self):
        '''Used in titles of plots'''

    @abstractmethod
    def get_distance(self, X0,X1):
        '''Calculate distance between two points using periodic boundary conditions'''

    @abstractmethod
    def move_to(self,X):
        '''
        This function is used to propose a move
        '''

    def admissable(self,proposed):
        '''Determine whether proposed configuration is admissable, i.e. no two spheres overlap'''
        m,_ = proposed.shape
        for i in range(m):
            for j in range(i+1,m):
                if self.get_distance(proposed[i,:],proposed[j,:]) < 2*self.sigma:
                    return False
        return True

    def direct_disks(self, N = 4, NTrials = maxsize,  rng = np.random.default_rng()):
        '''
        Prepare one admissable configuration of disks

        Parameters:
            N         Number of attempts
            NTrials   Maximum number of attempts to create configuration (tabula rasa)
            rng       Random number generator

        Returns:
            X, an array containing the coordinates of N points such that we can position N
            disks of radius sigma, with the centre of each disk at the corresponding point
            of X.
        '''

        for k in range(NTrials):
            proposed = self.propose(N,rng =rng)
            if self.admissable(proposed): return proposed

        raise RuntimeError(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')


class BoundedGeometry(Geometry):
    '''
    This class represents Boxes, Tori, etc. Any space that is bounded in at least one dimension

    Attributes:
         LowerBound
         UpperBound
    '''
    def __init__(self, L=np.array([1,1]), sigma=0.25,  d=2, LowerBound=0,UpperBound=np.inf):
        '''
        Parameters:
            L           A vector representing the length of one side of the space
            sigma       Radius of a sphere
            d           Dimension of space
            LowerBound  No coordinate is allowed to be less than this value
            UpperBound  No coordinate is allowed to exceed than this value
        '''
        super().__init__(L, sigma, d)
        self.LowerBound = LowerBound
        self.UpperBound = UpperBound

    def is_within_bounds(self,X):
        '''
        Establish whether a proposed move is between lower and upper bounds

        Parameters:
            X        Proposed new position

        Returns:   True iff new position is between lower and upper bounds
        '''
        if any(X < self.LowerBound): return False
        if any(self.UpperBound < X): return False
        return True

    def propose(self,N,rng = np.random.default_rng()):
        '''
        Used to propose a configuration of centroids of spheres,
        which is not guaranteed to be admissable.

        Parameters:
            N     Number of spheres
            rng   Random number generator
        '''
        return self.LowerBound + (self.UpperBound-self.LowerBound) * rng.random(size=(N,self.d))

class Box(BoundedGeometry):
    '''
    This class represents a simple box geometry without periodic boundary conditions
    '''
    def __init__(self, L = np.array([1,1]), sigma = 0.125, d = 2):
        '''
        Parameters:
            L      A vector representing the length of one side of the space
            sigma  Radius of a sphere
            d      Dimension of space
        '''
        super().__init__(L = L, sigma = sigma, d = d,LowerBound = sigma*np.ones(d),UpperBound =  L - sigma*np.ones(d))  #FIXME


    def get_distance(self, X0,X1):
        '''Calculate Euclidean distance between two points'''
        return np.linalg.norm(X0-X1)

    def move_to(self,X):
        '''
        This function is used to propose a move.
        '''
        return X

    def get_description(self):
        '''Used in titles of plots'''
        return 'without periodic boundary conditions'



class Torus(BoundedGeometry):
    '''This class represents a  box geometry with periodic boundary conditions, i.e. a torus.'''
    def __init__(self, L = np.array([1,1]), sigma = 0.125, d = 2):
        '''
        Parameters:
            L      A vector representing the length of one side of the space
            sigma  Radius of a sphere
            d      Dimension of space
        '''
        super().__init__(L = L, sigma = sigma, d = d, LowerBound = np.zeros(d),UpperBound = L)


    def get_distance(self, X0,X1):
        '''Calculate distance between two points using periodic boundary conditions'''
        return np.linalg.norm(self.diff_vec(X0,X1))

    def move_to(self,X):
        '''
        This function is used to propose a move
        '''
        return self.box_it(X)

    def box_it(self,X):
        '''
        Algorithm 2.5   Reduce a vector into a periodic box of size L

        Parameters:
            X       The vector that is to be reduced
        '''
        return X % self.L

    def diff_vec(self,X0,X1):
        '''
        Algorithm 2.6  Determine the distance between two vectors in a box
        with periodic boundary conditions

        Parameters:
            X0      One vector
            X1      The other vector

        '''
        Delta  = self.box_it(X0 - X1)
        return np.minimum(Delta, Delta - self.L/2)

    def get_description(self):
        '''Used in titles of plots'''
        return 'with periodic boundary conditions'

def GeometryFactory(periodic = False,L = np.array([1,1]),sigma = 0.125,d = 2):
    '''
    Create a periodic or aperiodic Geometry

    Parameters:
        periodic Indicates whether geometry is to have periodic boundary conditions
        L        A vector representing the length of one side of the space
        sigma    Radius of a sphere
        d        Dimension of space
    '''
    return Torus(L = L, sigma = sigma, d = d) if periodic else Box(L = L, sigma = sigma, d = d)

class Histogram:
    '''
       This class represents a Histogram, to which we can add samples dynamically.
       This allows memory to be saved, as we don't have to maintain individual
       samples in memory.

    Arrributes:
        n        Number of bins
        h        The collection of counts for all bins
        x0       Lowest sample value expected
        xn       Highest sample value expected
    '''
    def __init__(self,
                 n  = 10,
                 x0 = 0,
                 xn = 1,
                 h  = np.zeros((0,0))):
        self.n = n
        self.h = np.zeros((n)) if h.size == 0 else h
        self.x0 = x0
        self.xn = xn

    def __len__(self):
        '''
        Find number of bins
        '''
        return self.n

    def __getitem__(self, i):
        '''
        Find count of specified bin
        '''
        return self.h[i]

    def add(self,x):
        '''
        Add one value to histogram. This increases the count of the relevant bin by 1

        Parameters:
             x     The value to be added
        '''
        self.h[min(int(self.n * (x-self.x0)/(self.xn-self.x0)),len(self)-1)]+=1

    def get_hist(self):
        '''
        Retrieve counts and bin boundaries
        '''
        Z = sum(self.h)
        bins = [self.x0 + i*(self.xn-self.x0)/self.n for i in range(self.n)]
        return self.h/Z,bins + [self.xn]

    def bins(self):
        '''
        A generator use to iterate through the counts of all bins
        '''
        for i in range(self.n):
            yield(self.h[i])


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
