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

from math import exp

def thermo(Ns,beta=1.0):
    def extract(E):
        return [Ns[(e,m)] for (e,m) in Ns.keys() if e==E]
    Es     = sorted(list(set([E for (E,M) in Ns.keys()])))
    NsE    = [sum(extract(E)) for E in Es]
    N      = sum(n for n in Ns.values())
    Emin   = min(Es)
    Eprime = [E-Emin for E in Es]
    Z      = sum([N*exp(-beta*E) for (N,E) in zip(NsE,Eprime)])
    Emean  = sum([N*E*exp(-beta*E) for (N,E) in zip(NsE,Eprime)])/Z
    Esq    = sum([N*E*E*exp(-beta*E) for (N,E) in zip(NsE,Eprime)])/Z
    Z      = Z*exp(-beta*Emin)
    return (Z,beta*beta*(Esq-Emean*Emean)/N,(Emean + Emin)/N)
    
if __name__=='__main__':
    import argparse,sys,numpy
    import matplotlib.pyplot as plt
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
        T  = []
        cv = []
        E  = []
        for t in numpy.arange(0.8, 5.2, 0.05):
            Z,cc,ee=thermo(Ns,beta=1/t)
            T.append(t)
            cv.append(cc)
            E.append(ee)
        plt.plot(T,cv)
        plt.xlabel('T')
        plt.ylabel('cv')
        plt.show()
        