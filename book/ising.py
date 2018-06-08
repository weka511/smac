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


def Nbr(k,m,n):
    neighbours = []
    def add_if_possible(k,incr):
        candidate = k + incr
        if -1 < candidate and candidate < m*n:
            if abs(incr)==1:
                if candidate//n == k//n:
                    neighbours.append(candidate)   
            else:
                neighbours.append(candidate)    
    if k<m*n and k>0-1:
        add_if_possible(k,-n)
        add_if_possible(k,+n)
        add_if_possible(k,-1)
        add_if_possible(k,+1)
    return neighbours
    
def gray_flip(tau,N):
    k = tau[0]
    if k<=N:
        tau[k-1] = tau[k]
        tau[k] = k+1
        if (k != 1): tau[0] = 1
    return k,tau

def flip(ch):
    return '+' if ch =='-' else '-'

def enumerate_ising(m,n):
    N         = m * n
    Ns        = [0]*(4*N+1)
    sigma     = [-1]*N
    tau       = list(range(1,N+1+1))
    E         = -2*N
    Ns[E+2*N] = 2
    for i in range(2**(N-1)-1):
        k,tau=gray_flip(tau,N)
        k-=1
        h = sum(sigma[j] for j in Nbr(k,m,n))
        E += 2*sigma[k] * h
        Ns[E+2*N] += 2
        sigma[k] = -sigma[k]
    return [(E-2*N,Ns[E]) for E in range(len(Ns)) if Ns[E]>0]

if __name__=='__main__':
    #for i in range(9):
        #print (i,Nbr(i,3,3))
    N = 4
    for E,Ns in enumerate_ising(4,4):
        print (E,Ns)
    
    #N=4
    #tau = list(range(1,N+1+1))
    #spins = '-'*N
 
    #for i in range(2**N):
        #k,tau=gray_flip(tau,N)
        #print (i+1,spins,k,tau)
        #spins = ''.join([flip(spins[j]) if j==k-1 else spins[j] for j in range(N)])