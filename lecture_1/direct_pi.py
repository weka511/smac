#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

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

'''
   Algorithm 1.1 - compute pi using direct sampling
'''

from random import uniform

n_trials = 4000
n_hits   = 0
for iter in range(n_trials):
    x, y = uniform(-1.0, 1.0), uniform(-1.0, 1.0)
    if x**2 + y**2 < 1.0:
        n_hits += 1
print (4.0 * n_hits / float(n_trials))
