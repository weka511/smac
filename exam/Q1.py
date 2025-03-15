#!/usr/bin/env python

# Copyright (C) 2018-2025 Greenweaves Software Limited
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

import random

L = 3
t_max = 1000
counts = {}
transitions = {}

for i in range(1024):
    site = [0, 0]
    for t in range(t_max):
        delta = random.choice([[1, 0], [0, 1], [-1, 0], [0, -1]])
        s0 = site[0]
        s1 = site[1]
        site[0] = (site[0] + delta[0]) % L
        site[1] = (site[1] + delta[1]) % L
        if (site[0],site[1]) in counts:
            counts [(site[0],site[1])]+=1
        else:
            counts [(site[0],site[1])]=1
        if (s0,s1,site[0],site[1]) in transitions:
            transitions[(s0,s1,site[0],site[1])]+=1
        else:
            transitions[(s0,s1,site[0],site[1])]=0

    #print (site)

#for i in range(L):
    #for j in range(L):
        #if (i,j) in counts:
            #print (i,j,counts[i,j])
        #else:
            #print (i,j,'-')
print (transitions)
