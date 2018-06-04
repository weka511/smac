# permutation-test.py

# Copyright (C) 2015,2018 Greenweaves Software Pty Ltd

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

import permutation, math

perms={}
     
for i in range(120000):
    perm0=permutation.ran_perm(5)
    perm = permutation.permutation2str(perm0)
    if perm in perms:
        perms[perm]+=1
    else:
        perms[perm]=1

for kk in perms.keys():
    print (kk,", ",perms[kk])