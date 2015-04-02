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

import random, math, pylab

neighbour_table =[
    [2,4],
    [3,5,1],
    [6,2],
    [5,7,1],
    [6,8,4,2],
    [9,5,3],
    [8,4],
    [9,7,5],
    [8,6]
]

def row(cell):
   return (cell-1) /3;
    
def column(cell):
   return (cell-1)%3

def step(from_cell,to_cell):
   return (row(to_cell)-row(from_cell),column(to_cell)-column(from_cell))

def markov_discrete_pebble(k,table):
    return random.choice(table[k-1])

if __name__=="__main__":
   ns=[]
   sds=[]
   n=10
   for i in range(7):
       visits=[0,0,0,0,0,0,0,0,0]
       k=1
       for iteration in range(n):
           visits[k-1]+=1
           k=markov_discrete_pebble(k,neighbour_table)
       visits[k-1]+=1
       
       sum_sq=0
       mean=1.0/len(visits)
       
       for v in visits:
           freq= v/float(n)
           diff=freq-mean
           print freq, abs(diff)
           sum_sq+=diff*diff
       n*=10
       ns.append(i)
       sds.append(math.log(sum_sq))
                  
   pylab.plot(ns, sds, 'o')
   pylab.xlabel('Log N trials')
   pylab.ylabel('Log Error')
   pylab.title('Error vs iteration number')
   pylab.savefig('markov-discrete-pebble.png')
   pylab.show()