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


from gray import Gray

# Nbr
#
# Find neighbours in rectangular array indexed: 0, 1, ... m*n-1
#
def Nbr(k,m,n,periodic=False):
    neighbours = []
    def add_periodic(k,incr):
        candidate = k + incr
        if abs(incr)==1:
            while candidate//n < k//n:
                candidate += n
            while candidate//n > k//n:
                candidate -= n            
        else:
            while candidate<0:
                candidate += m*n
            while candidate>=m*n:
                candidate -= m*n
        if candidate != k and not candidate in neighbours:
            neighbours.append(candidate)
        
    def add_if_possible(k,incr):
        candidate = k + incr
        if -1 < candidate and candidate < m*n:
            if abs(incr)==1:
                if candidate//n == k//n:   # Same row?
                    neighbours.append(candidate)   
            else:
                if abs(incr)==n:   # Same column?
                    neighbours.append(candidate)  
     
    def add(k,incr):
        if periodic:
            add_periodic(k,incr)
        else:
            add_if_possible(k,incr)
            
    if k<m*n and k>-1:
        add(k,-n)
        add(k,+n)
        add(k,-1)
        add(k,+1)
        
    return neighbours
    


def flip(ch):
    return '+' if ch =='-' else '-'

def enumerate_ising(m,n,periodic=True,gray = Gray(4)):
    N         = m * n
    Ns        = {}
    sigma     = [-1]  *N
    E         = 2 * sum(sigma)
    M         = - sum(sigma)    # Magnetization
    Ns[(E,M)] = 2
    spins     = ''.join([('+' if sigma[j]>0 else '-') for j in range(N)])
    
    for k in gray:
        k         -= 1
        h         = sum(sigma[j] for j in Nbr(k,m,n,periodic=periodic))
        E         += (2*sigma[k] * h)

        sigma[k]  = -sigma[k]
        M         = 2 * sigma[k]
        if not (E,M) in Ns:
            Ns[(E,M)] = 0        
        Ns[(E,M)] += 2
        spins     = ''.join([('+' if sigma[j]>0 else '-') for j in range(N)])
    return [(E,Ns[E]) for E in sorted(Ns.keys())]



if __name__=='__main__':
    import argparse,sys

    parser = argparse.ArgumentParser(description='Compute statistics for Ising model')
    parser.add_argument('-o', '--output',default='ising.csv',help='File to record results')
    parser.add_argument('-m',type=int,default=4,help='Number of rows')
    parser.add_argument('-n',type=int,default=4,help='Number of columns')
    args = parser.parse_args()
    
    with open(args.output,'w') as f:
        gray      = Gray(args.m*args.n)
        counts = enumerate_ising(args.m,args.n,gray=gray)
        f.write('{0}\n'.format(gray))
        f.write('E,M,Ns\n')        
        for key,Ns in counts:
            E,M=key
            f.write('{0},{1},{2}\n'.format(E,M,Ns))
