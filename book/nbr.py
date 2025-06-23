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

'''
   Exercise 1.4. Neighbour table. NB I use k instead of -1 if the system remains in state k
   at the end of a step (rejection)
'''


import numpy as np
from numpy.testing import assert_array_equal
from unittest import main,TestCase

class NeighbourTable:
   def __init__(self,m,n):
      self.m = m
      self.n = n

   def get_row(self,row_index):

      def get_index(i,j):
         return i * self.n + j

      i = row_index // self.n
      j = row_index % self.n
      result = row_index * np.ones((4),dtype=int) # One position per move
      k = 0
      for i0 in [i-1,i+1]:
         if 0 <= i0 and i0 < self.m:
            result[k] = get_index(i0,j)
         k += 1
      for j0 in [j-1,j+1]:
         if 0 <= j0 and j0 < self.n:
            result[k] = get_index(i,j0)
         k += 1

      return result

   def create_Table(self):
      '''
      Construct an actual table, rather than simulating one

      '''
      Product = np.empty((self.m*self.n,4),dtype=int)
      for i in range(self.m*self.n):
         Product[i,:] = self.get_row(i)

      return Product

class NeighbourTableTest(TestCase):
   def assert_elements_equal(self,actual, desired, err_msg='', verbose=True, *, strict=False):
      assert_array_equal(np.sort(actual), np.sort(desired), err_msg='', verbose=True,  strict=False)

   def test_3_3(self):
      nbt = NeighbourTable(3,3)
      self.assert_elements_equal(nbt.get_row(0),np.array([1,3,0,0]))
      self.assert_elements_equal(nbt.get_row(1),np.array([2,4,0,1]))
      self.assert_elements_equal(nbt.get_row(2),np.array([2,5,1,2]))
      self.assert_elements_equal(nbt.get_row(3),np.array([4,6,0,3]))
      self.assert_elements_equal(nbt.get_row(4),np.array([5,7,3,1]))
      self.assert_elements_equal(nbt.get_row(5),np.array([5,8,4,2]))
      self.assert_elements_equal(nbt.get_row(6),np.array([ 7,6,6,3]))
      self.assert_elements_equal(nbt.get_row(7),np.array([ 8,7,6,4]))
      self.assert_elements_equal(nbt.get_row(8),np.array([7,5,8,8]))

   def test_create_Table(self):
      nbt = NeighbourTable(3,3)
      Table = nbt.create_Table()
      self.assert_elements_equal(Table[0,:],np.array([1,3,0,0]))
      self.assert_elements_equal(Table[1,:],np.array([2,4,0,1]))
      self.assert_elements_equal(Table[2,:],np.array([2,5,1,2]))
      self.assert_elements_equal(Table[3,:],np.array([4,6,0,3]))
      self.assert_elements_equal(Table[4,:],np.array([5,7,3,1]))
      self.assert_elements_equal(Table[5,:],np.array([5,8,4,2]))
      self.assert_elements_equal(Table[6,:],np.array([ 7,6,6,3]))
      self.assert_elements_equal(Table[7,:],np.array([ 8,7,6,4]))
      self.assert_elements_equal(Table[8,:],np.array([7,5,8,8]))

if __name__=='__main__':
   main()
