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

N = 8
nsteps = 100
for step in range(nsteps):
    tmp = list(range(N))
    L = []
    while tmp != []:
        element = random.choice(tmp)
        tmp.remove(element)
        L.append(element)
    print (L[0])
