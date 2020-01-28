# poschl-teller.py

# Copyright (C) 2020 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

# Exercise 3.5: plot Poeschl-Teller potential and investigate density matrix and partition function

import math,matplotlib.pyplot as plt,numpy as np,os
from matplotlib import rc

def V(x,chi=1.1,lambda0=1.1):
    return 0.5 *(chi*(chi-1)/math.sin(x)**2) * (lambda0*(lambda0-1)/math.cos(x)**2)

def E(n,chi=1.1,lambda0=1.1):
    return 0.5*(chi+lambda0+2*n)**2

# Determine plot file name

def get_plot_file_name(plot):
    if len(plot)==0:
        return '{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0])
    base,ext = os.path.splitext(plot)
    if len(ext)==0:
        return '{0}.png'.format(plot)
    return plot

if __name__=='__main__':
    import argparse
    
    parser = argparse.ArgumentParser('Plot Poeschl-Teller potential and investigate density matrix and partition function')
    parser.add_argument('--show',                           action='store_true', help='Show plot')
    parser.add_argument('--plot', default='',                                    help='Name of plot file')
    parser.add_argument('--dx',   default=0.01, type=float,                      help='Interval for plotting')
    args   = parser.parse_args()
    
    rc('text', usetex=True)
    
    xs = np.arange(args.dx,math.pi/2,args.dx)[:-1]
    
    plt.figure(figsize=(5,5))
    plt.subplot(2,1,1)
    params=[(1.01,1.01),(1.1,1.1),(1.1,1.2),(1.2,1.2)]
    for i in range(len(params)):
        chi,lambda0=params[i]
        plt.plot(xs,[V(x,chi,lambda0) for x in xs],label=r'$\chi={0},\lambda={1}$'.format(chi,lambda0))
    plt.legend()
    plt.title(r'P\"oschl-Teller Potential')
    
    plt.subplot(2,1,2)
    ns = range(25)
    markers = ['.', 'v', '^', '<', '>']
    for i in range(len(params)):
        chi,lambda0=params[i]    
        plt.scatter(ns,
                    [E(n,chi,lambda0) for n in ns],
                    s=15,
                    marker = markers[i%len(markers)],
                    label=r'$E_{{n}}^{{P-T}}({0},{1})$'.format(chi,lambda0))
    plt.xlabel('n')
    plt.ylabel('E')
    plt.legend()
    plt.title(r'Energy eigenvalues for P\"oschl-Teller potential')
    plt.tight_layout()
    plt.savefig(get_plot_file_name(args.plot))   
    if args.show:
        plt.show()    
