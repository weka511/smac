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


def per_to_str(perm):
    result=""
    for el in perm:
        result+=str(el)
    return result
    
perms={}
    
for i in range(1200000):
    perm0=permutation.ran_perm(5)
    perm = per_to_str(perm0)
    if perm in perms:
        perms[perm]+=1
    else:
        perms[perm]=1
    
count= len(perms.keys())
print count

sum=0
for kk in perms.keys():
    sum+=perms[kk]

average=sum/count

var=0
for kk in perms.keys():
    var+=((perms[kk]-average)*(perms[kk]-average))


sigma=math.sqrt(var/count)

print average, sigma
