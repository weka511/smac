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

# Gray
#
# Class for Gray code. Permits restarting

class Gray:
    def __init__(self,N,tau=None,i=0,progress=0):
        self.N        = N
        self.tau      = list(range(1,(N+1)+1)) if tau==None else tau
        self.i        = i
        self.max      = 2**(N-1)-1
        self.progress = progress
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i<self.max:
            self.i        += 1
            k             = self.tau[0]
            if self.progress>0 and self.i%self.progress==0:
                print ('{0:.4f}%'.format(100*self.i/self.max))
            if k>self.N: raise StopIteration
            self.tau[k-1] = self.tau[k]
            self.tau[k]   = k+1
            if (k != 1): self.tau[0] = 1
            return k            
        else:
            raise StopIteration
   
    def __str__(self):
        return '['+','.join(str(t) for t in self.tau)+']'
            
        
if __name__=='__main__':
    import unittest
    
    class GrayTest(unittest.TestCase):
        def setUp(self):
            flips    = [1,2,1,3,1,2,1]
            self.expected = flips+[1+max(flips)]+flips[::-1]
            
        def testGrayGenerator(self):
            i        = 0
            for k in gray(4):
                self.assertEqual(self.expected[i],k)
                i+=1
                
        def testGrayIterator(self):
            i        = 0
            grey     = Gray(4)
            for k in grey:
                self.assertEqual(self.expected[i],k)
                i+=1
                
    unittest.main()