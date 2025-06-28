#!/usr/bin/env python

# Copyright (C) 2015-2022 Greenweaves Software Limited
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

'''
    Useful functions from Chapter 1: BoxMuller, CircleThrowing, and SphereGenerator
'''

import numpy as np
from matplotlib.pyplot import figure, hist, show, subplot, suptitle, title, xlabel, ylabel

class BoxMuller:
    '''Algorithm 1.19'''
    def __init__(self,sigma=1.0,rng = np.random.default_rng()):
        self.even = True
        self.next_value = 0
        self.sigma = sigma
        self.rng = rng

    def box_muller(self):
        upsilon1 = 2
        while upsilon1==0 or upsilon1>1:
            x,y = 2*self.rng.random((2))-1
            upsilon1 = x**2 + y**2
        upsilon = - np.log(upsilon1)
        upsilon2 = self.sigma * np.sqrt(2*upsilon/upsilon1)
        return (x*upsilon2,y*upsilon2)

    def gauss(self,):
        if self.even:
            (value,self.next_value)=self.box_muller()
        else:
            value=self.next_value
        self.even= not self.even
        return value

class CircleThrowing:
    '''Algorithm 1.18'''
    def __init__(self,sigma,rng = np.random.default_rng()):
        self.sigma = sigma
        self.rng = rng

    def gauss(self):
        phi = random()*2*np.pi
        while phi==2*np.pi:
            phi = random()*2*np.pi
        rr = self.rng.random()
        while rr==0:
            rr = self.rng.random()
        upsilon = -np.log(rr)
        r = self.sigma*np.sqrt(2*upsilon)
        x = r*cos(phi)
        y = r*sin(phi)
        return (x,y)

class SphereGenerator:
    '''Algorithm 1.21 and 1.22'''
    def __init__(self,d,n, sigma = 1.0, gauss = BoxMuller(1.0),rng = np.random.default_rng()):
        self.d = d
        self.n = n
        self.gauss = gauss
        self.rng = rng

    def root_sigma(self,xs):
        return np.sqrt(sum(sum(el*el for el in x) for x in xs))


    def direct_sphere(self):
        '''Algorithm 1.21'''
        xs = [tuple([self.gauss.gauss() for j in range(self.d)]) for i in range(self.n)]
        upsilon = rng.random()**(1.0/(self.d*self.n))
        RootSigma = self.root_sigma(xs)
        return [tuple(el*upsilon/RootSigma for el in x) for x in xs]

    def direct_surface(self):
        '''Algorithm 1.22'''
        sigma = 1.0/np.sqrt(self.d)
        xs = [gauss.gauss() for k in range(self.d)]
        Sigma = sum(x*x for x in xs)
        return [x/Sigma for x in xs]

    def extract_points(self, xs, n):
        '''Convert a list of scalars to a list of n-dimenional vectors'''
        if len(xs)%n==0:
            i      = 0
            result = []
            point  = []
            while i<len(xs):
                for k in range(n):
                    point.append(xs[i])
                    i += 1
                result.append(tuple(point))
                point = []
            return result
        else:
            raise ValueError('Dimension {0} does not divide {1} length exactly'.format(n,len(xs)))

if __name__=='__main__':
    rng = np.random.default_rng()
    N = 1000000
    sg = SphereGenerator(3,N,rng=rng)
    energies = [x*x+y*y+z*z for (x,y,z) in sg.direct_sphere()]

    figure(figsize = (12,6))
    subplot(1,2,1)
    hist(energies,bins='sqrt')
    title('Bolzmann Histogram')
    xlabel('Frequency')
    ylabel('Energy')

    gauss = BoxMuller(rng=rng)
    subplot(1,2,2)
    hist([gauss.gauss() for _ in range(1000000)], bins = 'sqrt', density = True)
    title('Gaussian Histogram')
    xlabel('Value')
    ylabel('Frequency')

    suptitle('SMAC tests')
    show()

