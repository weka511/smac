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

if __name__=='__main__':
    import argparse,sys

    parser = argparse.ArgumentParser(description='Compute statistics for Ising model')
    parser.add_argument('-o', '--output',default='ising.csv',help='File to record results')
    parser.add_argument('-m',type=int,default=4,help='Number of rows')
    parser.add_argument('-n',type=int,default=4,help='Number of columns')
    parser.add_argument('-p','--progress',type=int,default=0,help='Record progress')
    args = parser.parse_args()
    
    with open(args.output,'w') as f:
        gray      = Gray(args.m*args.n,progress=args.progress)
        counts,pi = enumerate_ising(args.m,args.n,gray=gray)
        f.write('{0}\n'.format(gray))
        f.write('E,M,Ns\n')        
        for E,M,Ns in sorted(pi):
            f.write('{0},{1},{2}\n'.format(E,M,Ns))
