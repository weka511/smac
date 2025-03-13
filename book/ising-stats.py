#!/usr/bin/env python

# Copyright (C) 2019-2025 Greenweaves Software Limited

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

'''Figure 6.6 - plot data from ising.py'''

from argparse import ArgumentParser
from matplotlib.pyplot import  figure, show
import numpy as np

def parse_arguments():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input',
                        default = 'ising.csv',
                        help  = 'File to read data from')
    return parser.parse_args()

def read_data(input_file):
    data = np.genfromtxt(input_file, delimiter=',')[1:,:]
    m,_ = data.shape
    E = np.unique(data[:,0])
    N  = np.zeros_like(E)
    for i in range(len(E)):
        for j in range(m):
            if E[i] == data[j,0]:
                N[i] += data[j,2]
    return data,E,N

def thermo(N,E,beta=1.0):
    '''Algorithm 5.4 Calculate thermodynamic quantities'''
    Emin = E.min()
    Eprime = E - Emin
    weights = np.exp(-beta*Eprime)
    Z = np.dot(N, weights)
    Emean = np.dot(N,Eprime*weights)/Z
    Esq = np.dot(N,Eprime*Eprime*weights)/Z
    Z = Z*np.exp(-beta*Emin)
    return (Z, (Emean + Emin)/len(N), beta**2*(Esq - Emean**2)/len(N) ) # Z, <e>, cV

def get_magnetization(data,Energy):
    mask = np.in1d(data[:,0],Energy)
    M = data[mask,1]
    N = data[mask,2]
    total = N.sum()
    if total == 0: total += 1
    frequency = N/total
    return M,frequency

if __name__=='__main__':
    args = parse_arguments()
    data,E,N = read_data(args.input)
    T = np.linspace(0.8,6.0)
    cV = np.array([thermo(N,E,beta=1/t)[2] for t in T])

    fig = figure(figsize=(10,10))
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(T,cV,color='b',label='$c_V$')
    ax1.axvline(x=2/np.log(1+np.sqrt(2)),color='r',linestyle='--')
    ax1.set_xlabel('Temperature')
    ax1.set_ylabel('Specific Heat Capacity')
    ax1.set_title('Thermodynamic quantities')
    ax1.legend()

    colours = ['r','g','b','m','y','c','k']
    line_styles = ['--',':','-.']
    index = 0
    ax2 = fig.add_subplot(2,1,2)
    for Energy in sorted(E):
        M,frequency = get_magnetization(data,Energy)
        ax2.plot(M,frequency,
                    color=colours[index%len(colours)],
                    label='{0}'.format(Energy),
                    ls=line_styles[index//len(colours)])
        index+=1

    ax2.set_xlabel('Magnetization')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Frequency of Magnetization as a function of Energy')
    ax2.legend(title='Energy')

    show()
