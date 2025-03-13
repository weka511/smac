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

import random, math, pylab

L = 8
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}
nsteps = 10000 * N
list_T = [1.0 + 0.2 * i for i in range(15)]
list_av_m = []
S = [random.choice([1, -1]) for k in range(N)]
M = sum(S)
for T in list_T:
    print ('T = {0}'.format( T))
    beta = 1.0 / T
    M_tot = 0.0
    n_measures = 0
    for step in range(nsteps):
        k = random.randint(0, N - 1)
        delta_E = 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
        if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
            S[k] *= -1
            M += 2 * S[k]
        if step % N == 0 and step > nsteps / 2:
            M_tot += abs(M)
            n_measures += 1
    list_av_m.append(abs(M_tot) / float(n_measures * N))

pylab.title('$%i\\times%i$ lattice' % (L, L))
pylab.xlabel('$T$', fontsize=16)
pylab.ylabel('$<|M|>/N$', fontsize=16)
pylab.plot(list_T, list_av_m, 'bo-', clip_on=False)
pylab.ylim(0.0, 1.0)
pylab.savefig('plot_local_av_magnetization_L%i.png' % L)
