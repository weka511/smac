# Copyright (C) 2019 Greenweaves Software Limited
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

#   grey
#
#   Generator for Gray code
#
#   Inputs: N
#
#   Used to iterate through grey codes, returning
#   the coordinate that gets flipped each time (1-based) 
#
#   Usage:
#          for k in gray(N):
#               ....

def gray(N):
    tau = list(range(1,(N+1)+1))
    for i in range(2**(N-1)-1):
        k = tau[0]
        if k>N: return
        tau[k-1] = tau[k]
        tau[k]   = k+1
        if (k != 1): tau[0] = 1
        yield k
        
if __name__=='__main__':
    import unittest
    
    class GrayTest(unittest.TestCase):
        def testGray(self):
            flips    = [1,2,1,3,1,2,1]
            expected = flips+[1+max(flips)]+flips[::-1]
            i        = 0
            for k in gray(5):
                self.assertEqual(expected[i],k)
                i+=1
                
    unittest.main()