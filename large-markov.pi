# large-markov.pi

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

import markovdiscretepebble as mdp


def explore_space(m,n,max_iterations):
    def getK(i,j):
        def helper(j,values):
            if j<1:
                return values[0]
            elif j<n-1:
                return values[1]
            else:
                return values[2]        
        if i<1:
            return helper(j,[1,2,3])
        elif i<m-1:
            return helper(j,[4,5,6])
        else:
            return helper(j,[7,8,9])

    counts=[]
    for i in range(m*n):
        counts.append(0)
        
    i=0
    j=0
    iteration=0
    while iteration<max_iterations:
        k=getK(i,j)
        k_new=mdp.markov_discrete_pebble(k,mdp.neighbour_table)
 #       print i,j,k,k_new
        (i_step,j_step)=mdp.step(k,k_new)
        i+=i_step
        j+=j_step
        counts[n*i+j]+=1
        iteration+=1
    
    mean=1.0/(m*n)    
    sum_sq=0.0    

    for i in range(m*n):
        diff=counts[i]/float(max_iterations)-mean
        sum_sq+=(diff*diff)
        
    print sum_sq
    
explore_space(200,100,100000)