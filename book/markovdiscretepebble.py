# markov-discrete-pebble.py

# Copyright (C) 2015 Greenweaves Software Pty Ltd

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

import random, math, numpy as np, matplotlib.pyplot as plt

# Table 1.3 (0-8 instead of 1-9)

neighbour_table =[
    [ 1,  3, -1, -1],
    [ 2,  4,  0, -1],
    [-1,  5,  1, -1],
    [ 4,  6, -1,  0],
    [ 5,  7,  3,  1],
    [-1,  8,  4,  2],
    [ 7, -1, -1,  3],
    [ 8, -1,  6,  4],
    [-1, -1,  7,  5]
]

def row(cell):
   return cell //3
    
def column(cell):
   return cell%3

def step(from_cell,to_cell):
   return (row(to_cell)-row(from_cell),column(to_cell)-column(from_cell))

def markov_discrete_pebble(k,table):
   k_next=random.choice(table[k])
   if k_next==-1:
      return k
   else:
      return k_next

def markov_visits(m,n,i,j,N):
   def index(i,j):
      def index(ii,mm):
         if ii==0:
            return 0
         elif ii==mm-1:
            return 2
         else:
            return 1
      row_index=index(i,m)
      col_index=index(j,n)
      return row_index*3+col_index   
   visits=np.zeros((m,n),dtype=int)
   k=index(i,j)
   for trial in range(N):
      k_next = markov_discrete_pebble(k,neighbour_table)
      r = row(k)
      col = column(k)
      di,dj = step(k,k_next)
      i+=di
      j+=dj
      visits[i,j]+=1
      k=index(i,j)
   frequencies=np.zeros((m,n),dtype=float)
   for i in range(m):
      for j in range(n):
         frequencies[i,j]=visits[i,j]/N
   return frequencies
 
     
if __name__=="__main__":
   m=51
   n=91   
   N=1
   ns=[]
   sds=[]
   for i in range(7):
      N*=10
      frequencies=markov_visits(m,n,0,0,N)
      ns.append(math.log(N))
      sds.append(math.log(np.std(frequencies)/np.mean(frequencies)))
      
   plt.plot(ns, sds, 'o')
   plt.xlabel('Log N trials')
   plt.ylabel('Log Error')
   plt.title('Error vs iteration number')
   plt.savefig('markov-discrete-pebble.png')
   plt.show()