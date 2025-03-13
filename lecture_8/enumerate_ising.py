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

def gray_flip(tau, N):
    ''''
    Determine which bit is to be flipped
      Parameters:
        tau
        N     Lenght of t
      Returns:
        tau   New value for next iteration
        k     Bit that is to be flipped
    '''
    k          = tau[0]
    #if k > N: return tau, k #Guard - appears not to happen
    tau[k - 1] = tau[k]
    tau[k]     = k + 1
    if k != 1: tau[0] = 1
    return tau, k

L = 4
N = L * L
# Neighbours, assuming table wrapped
#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
# e.g. nbr[0] = (1, 4, 3, 12) - this doesn't match 5-2 in textbook

nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
S = [-1] * N
E = -2 * N
tau = list(range(1, N + 2))
M = -1 * N               #magnetization
pi = {}

for i in range(1, 2 ** N):
    tau, k = gray_flip(tau, N) # k-1 is index whose content gets flipped
    h = sum(S[n] for n in nbr[k - 1])
    E += 2 * h * S[k - 1]
    S[k - 1] *= -1
    M += 2*S[k - 1]
    if M in pi:
        pi[M]+=1
    else:
        pi[M] = 1

print (pi)
