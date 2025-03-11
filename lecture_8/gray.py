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
    Generate Gray Codes
'''

def gray(N):
    '''
        Recursive algorithm for k-bit Gray code, from
        http://cacs.usc.edu/education/phys516/01-4AdvancedMC.pdf
    '''
    k = 1
    g=[[0],[1]]
    while k < N:
        g = [[0] + gg for gg in g] + [[1] + gg for gg in g[::-1]]
        k+= 1
    return g

if __name__ == '__main__':
    for gray_code in gray(4):
        print (gray_code)
