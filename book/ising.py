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
from enumerate_ising import enumerate_ising

#def enumerate_ising(m,n,periodic=True,gray = Gray(4)):
    #N         = m * n
    #Ns        = {}
    #sigma     = [-1]  *N
    #E         = 2 * sum(sigma)
    #M         = - sum(sigma)    # Magnetization
    #Ns[E] = 2  
    #L         = m
    #nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
                #(i // L) * L + (i - 1) % L, (i - L) % N)
                                        #for i in range(N)}    
    #for k in gray:
        #h          = sum(sigma[j] for j in nbr[k-1])
        #E         += (2*sigma[k] * h)
        #sigma[k-1]  = -sigma[k-1]
        #M         = - sum(sigma)    # Magnetization
        #if not E in Ns:
            #Ns[E] = 0        
        #Ns[E] += 2

    #return [(E,Ns[E]) for E in sorted(Ns.keys())]



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
        for E,Ns in counts:
            f.write('{0},{1}\n'.format(E,Ns))
