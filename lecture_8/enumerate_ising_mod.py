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

def gray_flip(t, N):
    k        = t[0]
    if k > N: return t, k
    t[k - 1] = t[k]
    t[k]     = k + 1
    if k != 1: t[0] = 1
    return t, k

L = 4
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
S      = [-1] * N
E      = -2 * N
dos    = {}
dos[E] = 1
tau    = list(range(1, N + 2))
for i in range(1, 2 ** N):
    tau, k   = gray_flip(tau, N)
    h        = sum(S[n] for n in nbr[k - 1])
    E        += 2 * h * S[k - 1]
    S[k - 1] *= -1
    if E in dos: dos[E] += 1
    else:        dos[E] = 1
for E in sorted(dos.keys()):
    print (E, dos[E])
