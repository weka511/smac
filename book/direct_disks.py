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
    Exercise 2.6: directly sample the positions of 4 disks in a square box without
    periodic boundary conditions, for different covering densities.
    Exercise 2.7: directly sample the positions of 4 disks in a square box with
    periodic boundary conditions
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import maxsize, exit
from time import time
from unittest import main, TestCase
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from geometry import GeometryFactory

def direct_disks(N = 4, NTrials = maxsize,  geometry = None, rng = np.random.default_rng()):
    '''
    Prepare one admissable configuration of disks

    Parameters:
        N         Number of attempts
        NTrials   Maximum number of attempts to create configuration (tabula rasa)
        geometry  The space in which the action occurs--bounded or unbounded
        rng       Random number generator

    Returns:
        X, an array containing the coordinates of N points such that we can position N
        disks of radius sigma, with the centre of each disk at the corresponding point
        of X.
    '''

    for k in range(NTrials):
        proposed = geometry.propose(N,rng =rng)
        if geometry.admissable(proposed): return proposed

    raise RuntimeError(f'Failed to place {N} spheres within {NTrials} attempts for sigma={sigma}')

def get_file_name(name,default_ext='png',seq=None):
    '''
    Used to create file names

    Parameters:
        name          Basis for file name
        default_ext   Extension if non specified
        seq           Used if there are multiple files
    '''
    base,ext = splitext(name)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    qualified_name = f'{base}.{ext}'
    if ext == 'png':
        return join(args.figs,qualified_name)
    else:
        return qualified_name



if __name__=='__main__':
    main()
