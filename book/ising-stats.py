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

from math import exp,sqrt,log

def thermo(N,Es,Ns,beta=1.0):
    Emin   = min(Es)
    Eprime = [E-Emin for E in Es]
    Z      = sum([N         * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])
    Emean  = sum([N * E     * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])/Z
    Esq    = sum([N * E * E * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])/Z
    Z      = Z*exp(-beta*Emin)
    return (Z, beta*beta*(Esq-Emean*Emean)/N, (Emean + Emin)/N)
    
if __name__=='__main__':
    import argparse,numpy
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser(description='Compute statistics for Ising model')
    parser.add_argument('-i', '--input',default='ising.csv',help='File to record results')
    args = parser.parse_args()
    
    with open(args.input) as f:
        def agg(m0):
            return sum([n for (m,n) in zip(Ms,Ns) if m0==m])        
        i  = 0
        Es = []
        Ms = []
        Ns = []
        N  = None
        pi = {}
        for line in f:
            if i==0:
                N = len(line.strip().split(','))-1
            elif i==1:
                pass
            else:
                values=[int(s) for s in line.strip().split(',')]
                Es.append(values[0])
                Ms.append(values[1])
                Ns.append(values[2])
                if not values[0] in pi:
                    pi[values[0]]=[]
                pi[values[0]].append((values[1],values[2]))
            i+=1
        Ts  = []
        cvs = []
        for t in numpy.arange(0.8, 6.0, 0.05):
            Z,cv,E=thermo(N,Es,Ns,beta=1/t)
            Ts.append(t)
            cvs.append(cv)

        plt.plot(Ts,cvs,color='b')
        plt.axvline(x=2/log(1+sqrt(2)),color='r',linestyle='--')
        plt.xlabel('Temperature')
        plt.ylabel('Specific Heat Capacity')
        plt.title('Thermodynamic quantities')
        
        plt.figure(figsize=(10,10))
        colours     = ['r','g','b','m','y','c','k']
        line_styles = ['--',':','-.']
        index       = 0
        for E in sorted(pi.keys()):
            stats         = sorted(pi[E])
            magnetization = [m for m,_ in stats]
            counts        = [n for _,n in stats]
            total         = sum(counts)
            frequency     = [n/total for n in counts]
            plt.plot(magnetization,frequency,
                     color=colours[index%len(colours)],
                     label='{0}'.format(E),ls=line_styles[index//len(colours)])
            index+=1
        plt.xlabel('Magnetization')
        plt.ylabel('Frequency')
        plt.title('Frequency of Magnetization as a function of Energy')
        plt.legend(title='Energy')
        plt.show()
        