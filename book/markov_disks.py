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
    Exercise 2.8 and Algorithm 2.9. Generating a hard disk configuration
    from an earlier valid configuration using MCMC
'''

from os.path import  exists
from shutil import copyfile
from unittest import TestCase,main
import numpy as np
from numpy.random import default_rng
from geometry import GeometryFactory

def markov_disks(X, rng = default_rng(), delta = np.array([0.01,0.01]), geometry = GeometryFactory()):
    '''
    Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC

    Parameters:
        X
        rng
        delta
        geometry

    Returns:
        k,X, where
            k = index of the disk that was moved if we obtained a valid cofiguration
                -1 otherwise
            X is the new configuration (old if no move)
    '''

    def can_move(k,X_proposed):
        '''
            Verify that proposed new position is within the geometry,
            and that the resulting new configuration will be acceptable.
        '''
        if not geometry.is_within_bounds(X_proposed): return False

        for i in range(N):
            if i != k and geometry.get_distance(X[i,:],X_proposed) < 2*geometry.sigma:
                return False

        return True

    N,d = X.shape
    k = rng.integers(0,high=N)
    Delta = -delta + 2* delta*rng.random(size=d)
    X_proposed = geometry.move_to(X[k,:]+Delta)
    if can_move(k,X_proposed):
        X[k,:] = X_proposed
        return k,X
    else:
        return -1,X


class Checkpointer:
    '''
    Used to save a configuration to a checkpoint, and restore from saved checkpoint
    '''
    def __init__(self,file='check'):
        self.path = f'{file}.npz'
        self.backup = f'{self.path}~'

    def load(self):
        with load(self.path) as data:
            X = data['X']
            HistogramBins = data['HistogramBins']
            return X,HistogramBins

    def save(self, X = [], geometry = None):

        if exists(self.path):
            copyfile(self.path,self.backup)

        np.savez(self.path,
              X = X, HistogramBins = geometry.HistogramBins)


if __name__=='__main__':
    main()
