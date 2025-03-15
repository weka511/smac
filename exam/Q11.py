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

import math, random

def energy(sigma, h, J):
    E = - h * sigma[0] - h * sigma[1] - J * sigma[0] * sigma[1]
    return E

beta = 1.0
h = 1.0
J = 1.0
nsteps = 10000
sigma = [1, 1]
for step in range(nsteps):
    site = random.choice([0, 1])
    sigma_new = sigma[:]
    sigma_new[site] *= (-1)
    delta_E = energy(sigma_new, h, J) - energy(sigma, h, J)
    if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
        sigma = sigma_new[:]
