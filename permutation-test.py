# permutation-test.py

# Copyright (C) 2015 Greenweaves Software Oty Ltd

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

import permutation
import math
  
for i in range(10):    
    perms={}
        
    for i in range(12000):
        perm0=permutation.ran_perm(5)
        perm = permutation.permutation2str(perm0)
        if perm in perms:
            perms[perm]+=1
        else:
            perms[perm]=1
        
    count= len(perms.keys())
    
    sum=0
    for kk in perms.keys():
        sum+=perms[kk]
    
    average=sum/count
    
    chi_squared=0
    for kk in perms.keys():
        chi_squared+=((perms[kk]-average)*(perms[kk]-average))
    
    ss=math.sqrt(2*chi_squared)
    print count, average, chi_squared, ss, math.sqrt(2*count-1)
