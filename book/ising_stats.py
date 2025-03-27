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
import matplotlib.patches as mpatches

def get_file_name():
     return join(args.figs,basename(splitext(__file__)[0]))

def parse_arguments():
     parser = ArgumentParser(description=__doc__)
     parser.add_argument('-i', '--input', default = 'ising.csv', help  = 'File to read data from')
     parser.add_argument('--figs', default = './figs')
     parser.add_argument('-T', '--T', default=[0.5,4,0.5], nargs='+', type=float, help = 'Range for temperature: [start, ]stop, [step, ]')
     parser.add_argument('--show', default=False, action = 'store_true', help = 'Show plot')
     return parser.parse_args()

def read_data(input_file):
     '''
     Read Counts by Energy and Magnetization prepared by ising.py
     '''
     data = np.genfromtxt(input_file, delimiter=',')[1:,:]
     m,n = data.shape
     E = np.unique(data[:,0])
     N = np.zeros_like(E)
     for i in range(len(E)):
          mask = np.in1d(data[:,0],E[i])
          N[i] = data[mask,-1].sum()

     for i in range(len(E)):
          for j in range(m):
               if E[i] == data[j,0]:
                    N[i] += data[j,-1]
     return data,E,N,n>2

def thermo(E,N,beta=1.0,NObservations= None):
     '''
     Algorithm 5.4 Calculate thermodynamic quantities

     Parameters:
         E             Energies that are present in data
         N             Count of each energy
         beta          Inverse temperature
         NObservations Total number of States (exact enumeration) or data points (MCMC)

     Returns:
         Z      Partition function
         Emean  Mean energy
         cV     Specific heat capacity
     '''
     Emin = E.min()
     Eprime = E - Emin
     weights = np.exp(-beta*Eprime) *N
     Z = np.sum(weights)
     Emean = np.average(Eprime,weights=weights)
     EVariance = np.average((Eprime-Emean)**2,weights=weights)
     if NObservations == None:
          NObservations = len(N)-1
     return (
          Z*np.exp(-beta*Emin),                # Partition function
          (Emean + Emin)/NObservations,        # Mean energy e.g. 37-1!
          beta**2 * EVariance/NObservations    # Specific heat capacity
     )

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

def get_range(T,deltaT=0.1):
     '''
     Used to convert temperature (specified in args) to a range

     Parameters:
         T       [start, ]stop, [step, ]
     '''
     match (len(T)):
          case 1:
               return T
          case 2:
               return np.arange(T[0],T[1],deltaT)
          case 3:
               return np.arange(T[0],T[1]+T[2],T[2])

     raise ValueError(f'Parameter T must have length of 1,2, or 3')

if __name__=='__main__':
     args = parse_arguments()
     data,E,N,magnetization_data_is_present = read_data(args.input)
     T_range = get_range(args.T)

     cV = np.zeros((len(T_range)))
     mean_energies = np.zeros((len(T_range)))
     Z = np.zeros((len(T_range)))
     for i,T in enumerate(T_range):
          Z[i],mean_energies[i],cV[i] = thermo(E,N,beta=1.0/T)


     Tc = 2/np.log(1+np.sqrt(2))
     fig = figure(figsize=(10,10))
     fig.suptitle(f'{args.input}')

     ax1 = fig.add_subplot(2,2,1)
     ax1.plot(T_range,cV,color='b',label='$c_V$')
     ax1.axvline(x=Tc,color='r',linestyle='--')
     ax1.set_xlabel('Temperature')
     ax1.set_ylabel('Specific Heat Capacity')
     ax1.set_title('Thermodynamic quantities')
     ax1.legend(title='$c_V$',
                handles=[mpatches.Patch(color='none',
                                        label=f'{T:.1f}: {cV[i]:.5f}') for i,T in enumerate(T_range)])

     ax2 = fig.add_subplot(2,2,2)
     if magnetization_data_is_present:
          for t in sorted([Tc] + args.Temperatures):
               M,frequency = get_magnetization(data,beta=1/t)
               sTc = ' $(T_C)$' if t == Tc else ''
               ax2.plot(M,frequency,label=f'$T={t:.02f}$' + sTc)

          ax2.set_xlabel('Magnetization')
          ax2.set_ylabel('Frequency')
          ax2.set_title('Distribution of Magnetization')
          ax2.legend(title='Temperature')
     else:
          ax2.set_title('Magnetization data unavailable')

     ax3 = fig.add_subplot(2,2,3)
     ax3.plot(T_range,Z,color='b',label='$Z$')
     ax3.set_xlabel('Temperature')
     ax3.set_ylabel('Partition Function')
     ax3.set_title('Partition Function')
     ax3.legend()

     ax4 = fig.add_subplot(2,2,4)
     ax4.plot(T_range,mean_energies,color='b')
     ax4.set_xlabel('Temperature')
     ax4.set_ylabel('Energy')
     ax4.set_title('Mean Energy')
     ax4.legend(title='E',
           handles=[mpatches.Patch(color='none',
                                   label=f'{T:.1f}: {mean_energies[i]:.3f}') for i,T in enumerate(T_range)])

     fig.tight_layout(pad=2)
     if not exists(args.figs):
          makedirs(args.figs)
     fig.savefig(get_file_name())

     if args.show:
          show()
