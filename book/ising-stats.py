# Copyright (C) 2019-2022 Greenweaves Software Limited

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

''' 	Figure 6.6 - plot data from ising.py'''

from argparse          import ArgumentParser
from math              import exp,sqrt,log
from matplotlib.pyplot import axvline, figure, legend, plot, show, title, xlabel, ylabel
from numpy             import arange


def thermo(N,Es,Ns,beta=1.0):
    Emin   = min(Es)
    Eprime = [E-Emin for E in Es]
    Z      = sum([N         * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])
    Emean  = sum([N * E     * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])/Z
    Esq    = sum([N * E * E * exp(-beta*E) for (N,E) in zip(Ns,Eprime)])/Z
    Z      = Z*exp(-beta*Emin)
    return (Z, beta*beta*(Esq-Emean*Emean)/N, (Emean + Emin)/N)


parser = ArgumentParser(description='Compute statistics for Ising model')
parser.add_argument('-i', '--input',
                    default = 'ising.csv',
                    help    = 'File to record results')
args = parser.parse_args()

with open(args.input) as f:
    # def agg(m0):
        # return sum([n for (m,n) in zip(Ms,Ns) if m0==m])
    # i  = 0
    Es = []
    Ms = []
    Ns = []
    N  = None
    pi = {}
    for i,line in enumerate(f):
        if i==0:
            continue
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
    for t in arange(0.8, 6.0, 0.05):
        _,cv,E = thermo(N,Es,Ns,beta=1/t)
        Ts.append(t)
        cvs.append(cv)

    plot(Ts,cvs,color='b')
    axvline(x=2/log(1+sqrt(2)),color='r',linestyle='--')
    xlabel('Temperature')
    ylabel('Specific Heat Capacity')
    title('Thermodynamic quantities')

    figure(figsize=(10,10))
    colours     = ['r','g','b','m','y','c','k']
    line_styles = ['--',':','-.']
    index       = 0

    for E in sorted(pi.keys()):
        stats         = sorted(pi[E])
        magnetization = [m for m,_ in stats]
        counts        = [n for _,n in stats]
        total         = sum(counts)
        frequency     = [n/total for n in counts]
        plot(magnetization,frequency,
                 color=colours[index%len(colours)],
                 label='{0}'.format(E),ls=line_styles[index//len(colours)])
        index+=1

    xlabel('Magnetization')
    ylabel('Frequency')
    title('Frequency of Magnetization as a function of Energy')
    legend(title='Energy')
    show()
