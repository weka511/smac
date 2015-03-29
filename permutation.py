# permutation.py

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

import random

def ran_perm(K):
    perm = range(K)
    for k in range(K):
        l=random.randint(k,K-1)
        perm[k],perm[l]=perm[l],perm[k]
    return perm

def ran_combination(K,M):
    perm = range(K)
    for k in range(M):
        l=random.randint(k,K-1)
        perm[k],perm[l]=perm[l],perm[k]
    return perm[0:2]    
 
if __name__=='__main__':
    for i in range(100):
        print ran_combination(4,2)
