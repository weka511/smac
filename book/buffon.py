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

''' Template for Python programs'''

from argparse import ArgumentParser
from unittest import main,TestCase
import numpy as np

def get_n(a,b,x=0,phi=0,epsilon=0.001):
    projection = (a/2) * np.cos(phi) + x
    if projection < b/2 or abs(projection - b/2) < epsilon:
        return 0
    else:
        projection -= (b/2)
        return int(projection//b) + 1

def get_hits(a,b,x=0,phi=0):
    '''
    Used to calculate number of hits at each position in heatmap

    Parameters:
        a       Length of needle
        b       Distance between cracks
        x       x coordinate of centre
        phi     Angle to horizontal
    '''
    if a < b:
        return 1 if x < a/2 and abs(phi) < np.arccos(x/(a/2)) else 0
    else:
        return get_n(a,b,x,phi) + get_n(a,b,b/2-x,phi)

class BuffonTest(TestCase):
    def test12(self):
        self.assertEqual(1,get_hits(1,2,x=0,phi=0))
        self.assertEqual(0,get_hits(1,2,x=2,phi=np.pi/2))

    def testpi_2(self):
        self.assertEqual(4,get_hits(np.pi,1,x=0,phi=0))
        self.assertEqual(0,get_hits(np.pi,1,x=0.5,phi=np.pi/2))
        self.assertEqual(0,get_n(np.pi,1,x=0.5,phi=np.pi/2))

if __name__=='__main__':
    main()
