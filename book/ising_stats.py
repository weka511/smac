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
from os import makedirs
from os.path import basename, exists, join, splitext
from matplotlib.pyplot import  figure, show
import numpy as np

def get_file_name():
     return join(args.figs,basename(splitext(__file__)[0]))

def parse_arguments():
     parser = ArgumentParser(description=__doc__)
     parser.add_argument('-i', '--input',
                         default = 'ising.csv',
                         help  = 'File to read data from')
     parser.add_argument('--figs', default = './figs')
     parser.add_argument('-e', '--energies',
                         default = [],
                         type = int,
                         nargs = '+',
                         help  = 'File to read data from')
     parser.add_argument('-T','--Temperatures',
                         default=[2.5,5],
                         type=float,
                         nargs='+',
                         help='Temperatures to be plotted')
     return parser.parse_args()

def read_data(input_file):
     '''
     Read Counts by Energy and Magnetization prepared by ising.py
     '''
     data = np.genfromtxt(input_file, delimiter=',')[1:,:]
     m,_ = data.shape
     E = np.unique(data[:,0])
     N = np.zeros_like(E)
     for i in range(len(E)):
          mask = np.in1d(data[:,0],E[i])
          N[i] = data[mask,2].sum()

     for i in range(len(E)):
          for j in range(m):
               if E[i] == data[j,0]:
                    N[i] += data[j,2]
     return data,E,N

def thermo(N,E,beta=1.0):
     '''
     Algorithm 5.4 Calculate thermodynamic quantities

     Parameters:
         N
         E
         beta
     '''
     Emin = E.min()
     Eprime = E - Emin
     weights = np.exp(-beta*Eprime)
     Z = np.dot(N, weights)
     Emean = np.dot(N,Eprime*weights)/Z
     Esq = np.dot(N,Eprime*Eprime*weights)/Z
     return (Z*np.exp(-beta*Emin),                # Partition function
             (Emean + Emin),#/len(N),               # Mean energy
             beta**2 * (Esq - Emean**2)/len(N) )  # Specific heat capacity

def get_magnetization(data,beta):
     '''
     Get frequency of each magnetization given energy

     Parameters:
         data
         Energy

     Returns:
        (M,frequency), where:
            M is an array of magnetizations
            frequency is an array of the same length
     '''
     Emin = data[:,0].min()
     EPrime = data[:,0] - Emin
     N = data[:,2]
     M = data[:,1]
     N_weighted= np.exp(-beta*EPrime)*N
     M_index = np.unique(M)
     frequency = np.zeros_like(M_index)

     for i in range(len(M_index)):
          for j in range(len(M)):
               if M[j] == M_index[i]:
                    frequency[i] += N_weighted[j]

     return M_index,frequency/frequency.sum()

if __name__=='__main__':
     args = parse_arguments()
     data,E,N = read_data(args.input)
     T = np.linspace(0.8,6.0)

     specific_heat_capacities = []
     mean_energies = []
     Z = []
     for t in T:
          z,mean_energy,cV = thermo(N,E,beta=1/t)
          Z.append(z)
          specific_heat_capacities.append(cV)
          mean_energies.append(mean_energy)

     Tc = 2/np.log(1+np.sqrt(2))
     fig = figure(figsize=(10,10))
     fig.suptitle(f'{args.input}')

     ax1 = fig.add_subplot(2,2,1)
     ax1.plot(T,specific_heat_capacities,color='b',label='$c_V$')
     ax1.axvline(x=Tc,color='r',linestyle='--',label=f'$T_C={Tc:.02f}$')
     ax1.set_xlabel('Temperature')
     ax1.set_ylabel('Specific Heat Capacity')
     ax1.set_title('Thermodynamic quantities')
     ax1.legend()

     ax2 = fig.add_subplot(2,2,2)
     for t in sorted([Tc] + args.Temperatures):
          M,frequency = get_magnetization(data,beta=1/t)
          sTc = ' $(T_C)$' if t == Tc else ''
          ax2.plot(M,frequency,label=f'$T={t:.02f}$' + sTc)

     ax2.set_xlabel('Magnetization')
     ax2.set_ylabel('Frequency')
     ax2.set_title('Distribution of Magnetization')
     ax2.legend(title='Temperature')

     ax3 = fig.add_subplot(2,2,3)
     ax3.plot(T,Z,color='b',label='$Z$')
     ax3.set_xlabel('Temperature')
     ax3.set_ylabel('Partition Function')
     ax3.set_title('Partition Function')
     ax3.legend()

     ax4 = fig.add_subplot(2,2,4)
     ax4.plot(T,mean_energies,color='b',label=r'$\bar{E}$')
     ax4.set_xlabel('Temperature')
     ax4.set_ylabel('Energy')
     ax4.set_title('Mean Energy')
     ax4.legend()

     fig.tight_layout(pad=2)
     if not exists(args.figs):
          makedirs(args.figs)
     fig.savefig(get_file_name())
     show()
