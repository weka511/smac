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
from numpy             import array, minimum, ones, pi, prod, reshape, zeros
from numpy.linalg      import norm

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

    def box_it(self,X):
        '''Algorithm 2.5'''
        return X%self.L

    def diff_vec(self,X0,X1):
        '''Algorithm 2.6'''
        Delta  = self.box_it(X0 - X1)
        return minimum(Delta, Delta - self.L/2)

    def get_description(self):
        return 'with periodic boundary conditions'
