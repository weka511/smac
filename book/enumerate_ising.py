# Copyright (C) 2018-2019 Greenweaves Software Limited

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


from gray import gray

# Nbr
#
# Find neighbours in rectangular array indexed: 0, 1, ... m*n-1
#
# Inputs: k        Index of point whose neighbours are to be found
#         m        Dimension of array
#         n        Dimension of array
#         periodic Indicates whether to use peridica boundary conditions
#
# Returns: List of neighbours

def Nbr(k,m,n,periodic=False):
 
    #   add_periodic
    #
    #   Add one neighbour for periodic boundary conditions
    #
    #   Inputs:
    #       k      Element whose neighbour is to be added
    #       incr   Offset of neighbour   
    def add_periodic(k,incr):
        candidate = k + incr
        if abs(incr)==1:
            while candidate//n < k//n:
                candidate += n
            while candidate//n > k//n:
                candidate -= n            
        else:
            while candidate<0:
                candidate += m*n
            while candidate>=m*n:
                candidate -= m*n
        if candidate != k and not candidate in neighbours:
            neighbours.append(candidate)

    #   add_if_possible
    #
    #   Add one neighbour without boundary conditions,
    #   so attempt may be rejected
    #
    #   Inputs:
    #       k      Element whose neighbour is to be added
    #       incr   Offset of neighbour        
    def add_if_possible(k,incr):
        candidate = k + incr
        if -1 < candidate and candidate < m*n:
            if abs(incr)==1:
                if candidate//n == k//n:   # Same row?
                    neighbours.append(candidate)   
            else:
                if abs(incr)==n:   # Same column?
                    neighbours.append(candidate)  
     
    neighbours = []
    add = add_periodic if periodic else add_if_possible
               
    if k<m*n and k>-1:
        for incr in [-n,+n,-1,+1]:
            add(k,incr)
        
    return neighbours
    
# enumerate_ising
#
# Inputs: m        Dimension of array
#         n        Dimension of array
#         periodic Indicates whether to use peridica boundary conditions
def enumerate_ising(m,n,periodic=True):
    N         = m * n
    E         = -2 * N
    Ns        = {}
    Ns[E]     = 2
    sigma     = [-1]  *N
    L         = m
    nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
                (i // L) * L + (i - 1) % L, (i - L) % N)
                                        for i in range(N)}
    for k in gray(N):
        k         -= 1   # grey return 1-based index
        #h         = sum(sigma[j] for j in Nbr(k,m,n,periodic=periodic))
        h          = sum(sigma[j] for j in nbr[k])
        E         += (2*sigma[k] * h)
        if not E in Ns:
            Ns[E] = 0
        Ns[E] += 2
        sigma[k]  = -sigma[k]

    return [(E,Ns[E]) for E in sorted(Ns.keys())]

if __name__=='__main__':
    import unittest
    class TestIsing(unittest.TestCase):
        def test2(self):
            expected = {0:12,8:2}
            for E,Ns in enumerate_ising(2,2):
                self.assertEqual(expected[abs(E)],Ns)
        def test4(self):
            expected = {0:20524, 4:13568, 8:6688, 12:1728, 16:424, 20:64, 24:32, 28:0, 32:2}
            for E,Ns in enumerate_ising(4,4):
                self.assertEqual(expected[abs(E)],Ns)        
    
                
    unittest.main()
