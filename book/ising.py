# Copyright (C) 2018 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

N = 4

def gray_flip(tau):
    k = tau[0]
    if k<=N:
        tau[k-1] = tau[k]
        tau[k] = k+1
        if (k != 1): tau[0] = 1
    return k,tau

def flip(ch):
    return '+' if ch =='-' else '-'

if __name__=='__main__':
    tau = list(range(1,N+1+1))
    spins = '-'*N
    for i in range(2**N):
        k,tau=gray_flip(tau)
        print (i+1,spins,k,tau)
        spins = ''.join([flip(spins[j]) if j==k-1 else spins[j] for j in range(N)])