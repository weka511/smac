# Copyright (C) 2019 Greenweaves Software Limited

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

def  thermo(Ns):
    print (Ns)
    
if __name__=='__main__':
    import argparse,sys

    parser = argparse.ArgumentParser(description='Compute statistics for Ising model')
    parser.add_argument('-i', '--input',default='ising.csv',help='File to record results')
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        i = 0
        Ns = {}
        for line in f:
            if i>1:
                values=[int(s) for s in line.strip().split(',')]
                Ns[(values[0],values[1])] = values[2]
            i+=1
        thermo(Ns)
        