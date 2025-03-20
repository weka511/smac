#!/usr/bin/env python

# Copyright (C) 2018-2025 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''Algorithm 5.3: single flip enumeration for the Ising model.'''

from collections import defaultdict
from gray import gray_flip, Nbr
from unittest import main, TestCase

def enumerate_ising(shape, periodic = True):
    '''
    Algorithm 5.3: single flip enumeration for the Ising model.

    Inputs: shape    Dimension of array
            periodic Indicates whether to use periodic boundary conditions

    Returns:
           Energy         Pairs (E,Count) for all possible energies
           Magnetization  Pairs (M,Count) for all possible energies
    '''
    N = shape[0] * shape[1]
    sigma = [-1]  *N
    M = sum(sigma)
    E = - 1 * N     # FIXME
    Ns = defaultdict(lambda: 0)
    Ns[E] = 1
    Ms = defaultdict(lambda: 0)
    Ms[E,M] = 1

    # Visit all configuraions and adjust E and M

    for i, (k,_) in enumerate(gray_flip(N)):
        if i > 2**(N-1) - 2:
            return [(E,Ns[E]) for E in sorted(Ns.keys())], [(M,Ms[M]) for M in sorted(Ms.keys())]
        k -= 1                                #k starts at 1 (following The Book), convert to 0-based
                                              # so we can use as an array index
        # Calculate field on site k and use it to update E
        h = sum(sigma[j] for j in Nbr(k, shape = shape, periodic = periodic))
        E += 1*sigma[k]*h   # FIXME
        Ns[E] += 1

        M -= 2 *sigma[k]
        Ms[E,M] += 1

        sigma[k] *= -1  # Flip this site

    raise ValueError(f'{i} not reached its limit')

class TestIsing(TestCase):
    '''Tests for enumerate_ising'''

    def test2(self):
        Expected   = {  # From Figure 5.5
            -8:1,
            0:6,
            8:1
        }
        Energies,Magnetization = enumerate_ising((2,2))

        # Energies and Expected each contain one entry for zero energy. All other energies
        # that have a non-zero count exist in pairs, positive and negative, in Energies,
        # but appear only once in Expected. This is captured in the following comparison
        self.assertEqual(len(Expected), len(Energies))
        for E,Ns in Energies:
            self.assertEqual(Expected[abs(E)],Ns)

    # def test4(self):
        # Expected   = {  # From Table 5.2
            # 0:  20524,
            # 4:  13568,
            # 8:  6688,
            # 12: 1728,
            # 16: 424,
            # 20: 64,
            # 24: 32,
            # 32: 2
        # }
        # Energies,_ = enumerate_ising((4,4))
        # self.assertEqual(2*len(Expected)-1, len(Energies))
        # for E,Ns in Energies:
            # self.assertEqual(Expected[abs(E)],Ns)

if __name__=='__main__':
    main()
