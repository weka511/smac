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

L = 12
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
n_spins_to_flip = N * 10000
list_T = [1.0 + 0.2 * i for i in range(15)]
list_av_m = []
S = [random.choice([1, -1]) for k in range(N)]
M = sum(S)
for T in list_T:
    print (T)
    p  = 1.0 - math.exp(-2.0 / T)
    M_tot = 0.0
    n_flipped_spins = 0
    nsteps = 0
    while n_flipped_spins < n_spins_to_flip:
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            j = random.choice(Pocket)
            for l in nbr[j]:
                if S[l] == S[j] and l not in Cluster and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
            Pocket.remove(j)
        for j in Cluster:
            S[j] *= -1
        M -= 2 * len(Cluster) * S[k]
        n_flipped_spins += len(Cluster)
        M_tot += abs(M)
        nsteps += 1
    list_av_m.append(M_tot / float(nsteps) / N)
pylab.plot(list_T, list_av_m, 'bo-', clip_on=False)
pylab.title('%i x %i lattice (periodic boundary conditions)' % (L, L))
pylab.xlabel('$T$', fontsize=16)
pylab.ylabel('$<|M|>/N$', fontsize=16)
pylab.savefig('plot_cluster_av_magnetization_L%i.png' % L)
