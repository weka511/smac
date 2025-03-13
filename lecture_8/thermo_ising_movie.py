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

import math, os, pylab

L = 6
N = L * L
filename = 'data_dos_L%i.txt' % L
if os.path.isfile(filename):
    dos = {}
    f = open(filename, 'r')
    for line in f:
        E, N_E = line.split()
        dos[int(E)] = int(N_E)
    f.close()
else:
    exit('input file missing')
list_T = [0.5 + 0.01 * i for i in range(500)]
list_cv = []
for T in list_T:
    Z = 0.0
    E_av = 0.0
    M_av = 0.0
    E2_av = 0.0
    for E in dos.keys():
        weight = math.exp(- E / T) * dos[E]
        Z += weight
        E_av += weight * E
        E2_av += weight * E ** 2
    E2_av /= Z
    E_av /= Z
    cv = (E2_av - E_av ** 2) / N / T ** 2
    list_cv.append(cv)
pylab.title('Specific heat capacity ($%i\\times%i$ lattice, PBC\'s)' % (L, L))
pylab.xlabel('$T$', fontsize=20)
pylab.ylabel('$c_V$', fontsize=20)
pylab.plot(list_T, list_cv, 'k-', lw=3)
pylab.show()
