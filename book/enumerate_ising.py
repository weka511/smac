# Copyright (C) 2018-2022 Greenweaves Software Limited

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
from gray        import gray, Nbr

# enumerate_ising
#
#
def enumerate_ising(shape, periodic = True):
    '''
    Algorithm 5.3: single flip enumeration for the Ising model.

    Inputs: m        Dimension of array
            n        Dimension of array
            periodic Indicates whether to use periodic boundary conditions
    '''
    N         = shape[0] * shape[1]
    Ns        = defaultdict(lambda: 0)
    sigma     = [-1]  *N
    E         = 2 * sum(sigma)
    Ns[E]     = 2

    for i, k in enumerate(gray(N)):
        if i>2**(N-1)-2: break
        k0         = k - 1 #1=based -> 0-based
        h          = sum(sigma[j] for j in Nbr(k0,
                                               shape    = shape,
                                               periodic = periodic))
        E          = E + 2 * sigma[k0] * h
        Ns[E]     += 2
        sigma[k0] *= -1

    return [(E,Ns[E]) for E in sorted(Ns.keys())]

    # pi        = {}
    # sigma     = [-1]  *N
    # E         = 2 * sum(sigma)
    # M         = 1 * sum(sigma)              #magnetization
    # Ns[E]     = 2
    # pi[(E,M)] = 2
    # L         = m
    # nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
                # (i // L) * L + (i - 1) % L, (i - L) % N)
                                        # for i in range(N)}
    # for i,k in enumerate(gray):
        # if i>=2**(N-1)-2: break
        # k         -= 1   # gray return 1-based index
        # h          = sum(sigma[j] for j in nbr[k])
        # E         += (2*sigma[k] * h)
        # if not E in Ns:
            # Ns[E] = 0
        # Ns[E]    += 2
        # sigma[k]  = -sigma[k]
        # M += 2*sigma[k]
        # if (E,M) in pi:
            # pi[(E,M)]+=2
        # else:
            # pi[(E,M)] = 2

    # return [(E,Ns[E]) for E in sorted(Ns.keys())],[(E,M,pi[(E,M)]) for (E,M) in sorted(pi.keys())]

if __name__=='__main__':
    print (enumerate_ising((4,4)))
    # import unittest
    # class TestIsing(unittest.TestCase):
        # def test2(self):
            # expected   = {0:12, 8:2}
            # Energies = enumerate_ising((2,2))
            # for E,Ns in Energies:
                # self.assertEqual(expected[abs(E)],Ns)
        # # def test4(self):
            # # expected = {0:20524, 4:13568, 8:6688, 12:1728, 16:424, 20:64, 24:32, 28:0, 32:2}
            # # Energies,_=enumerate_ising(4,4,gray = Gray(16))
            # # for E,Ns in Energies:
                # # self.assertEqual(expected[abs(E)],Ns)


    # unittest.main()
