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

# Helper tables, which speed up calculation by caching exponentials. Index on i and j, not x and y. 
phi_helper = {}
V          = {}

# build_helpers
#
# Construct helper tables

def build_helpers(n,phi_mult=1,m=1,h=1,beta=1,dx=1,chi=1.1,lambda0=1.1):
    for i in range(n+1):
        for j in range(i,n+1):
            if not (j-i) in phi_helper:
                phi_helper[(j-i)] = phi_mult * math.exp(- (m * (dx*(i-j))**2)/(2 * h**2 * beta))
    for i in range(n):
        V[i] = poeschl_teller((0.5+i)*dx, chi=chi, lambda0=lambda0)
                
def poeschl_teller(x,chi=1.1,lambda0=1.1):
    return 0.5 *chi*(chi-1)/math.sin(x)**2 * lambda0*(lambda0-1)/math.cos(x)**2

def E(n,chi=1.1,lambda0=1.1):
    return 0.5*(chi+lambda0+2*n)**2

@np.vectorize
def trotter(i,j):
    return V[i] * phi_helper[abs(i-j)] * V[j]

# Determine plot file name

def get_plot_file_name(plot):
    if len(plot)==0:
        return '{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0])
    _,ext = os.path.splitext(plot)
    if len(ext)==0:
        return '{0}.png'.format(plot)
    return plot

# plot_density
#
# Plot density_matrix
#
def plot_density(X,Y,rho,beta):
    plt.pcolor(X,Y,rho)
    plt.colorbar()
    plt.title(r'$\rho(x,x^{{\prime}},{0:.4f})$'.format(beta))
    
if __name__=='__main__':
    import argparse
    
    parser = argparse.ArgumentParser('Plot Poeschl-Teller potential and investigate density matrix and partition function')
    parser.add_argument('--beta',   default=0.01, type=float,                      help='Inverse temperature')
    parser.add_argument('--h',      default=1,   type=float,                      help='Planck\'s constant') 
    parser.add_argument('-m','--m', default=1.0, type=float,                      help='Mass of particle')
    parser.add_argument('--n',      default=100, type=int,                        help='Number of dxs')
    parser.add_argument('--show',                           action='store_true', help='Show plot')
    parser.add_argument('--plot', default='',                                    help='Name of plot file')

    args   = parser.parse_args()
    beta   = args.beta
    dx     = math.pi/(2 * args.n)
    grid_i = [i for i in range(0,args.n)]          # integer grid for calculation - allow lookup
    I,J    = np.meshgrid(grid_i,grid_i)
    xs     = [(0.5 + i) * dx for i in grid_i ]
    X,Y    = np.meshgrid(xs,xs)                    # grid for plotting
    
    build_helpers(n       = args.n,
                 phi_mult = math.sqrt(args.m/(2*math.pi*args.h*args.h*beta)),
                 m        = args.m,
                 h        = args.h,
                 beta     = args.beta,
                 dx       = dx,
                 chi      = 1.1,
                 lambda0  = 1.1)
    
    rc('text', usetex=True)
    plt.figure(figsize=(10,10))
    plt.subplot(3,3,1)
    params=[(1.01,1.01),(1.1,1.1),(1.1,1.2),(1.2,1.2)]
    for i in range(len(params)):
        chi,lambda0=params[i]
        plt.plot(xs,[poeschl_teller(x,chi,lambda0) for x in xs],label=r'$\chi={0},\lambda={1}$'.format(chi,lambda0))
    plt.legend()
    plt.title(r'P\"oschl-Teller Potential')
    
    plt.subplot(3,3,2)
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
    
    plt.subplot(3,3,3)
    rho = trotter(I,J)
    plot_density(X,Y,np.log(rho),beta)
    
    for i in range(6):
        plt.subplot(3,3,i+4)
        beta *= 2      
        rho = np.dot(rho, rho)   # We have to use .dot, as * does elementwise multiplication
        rho *= dx                # we want an integral, not just a sum 
        plot_density(X,Y,np.log(rho),beta)
    
    plt.tight_layout()
    plt.savefig(get_plot_file_name(args.plot))   
    if args.show:
        plt.show()    
