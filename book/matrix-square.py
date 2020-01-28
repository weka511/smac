# matrix-square.py

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

# Exercise 3.4: implement Alg 3.3, matrix-square

import math,matplotlib.pyplot as plt,numpy as np,os
from matplotlib import rc

# Helper tables, which speed up calculation by caching exponentials. Index on i and j, not x and y. 
phi_helper = {}
V          = {}

# build_helpers
#
# Construct helper tables

def build_helpers(n,phi_mult=1,m=1,h=1,beta=1,dx=1,omega=1):
   for i in range(-n,n+1):
      for j in range(i,n+1):
         if not (j-i) in phi_helper:
            phi_helper[(j-i)] = phi_mult * math.exp(- (m * (dx*(i-j))**2)/(2 * h**2 * beta))
   for i in range(n+1):
      V[i]= math.exp(-0.5 * beta * 0.5 * m * omega  **2 * (dx * i)**2)

# Calculate density matric from trotter decomposition

@np.vectorize
def trotter(i,j):
   return V[abs(i)] * phi_helper[abs(i-j)] * V[abs(j)]

# Determine plot file name

def get_plot_file_name(plot):
   if len(plot)==0:
      return '{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0])
   base,ext = os.path.splitext(plot)
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
      
   parser = argparse.ArgumentParser('Exercise 3.4: calculate density matrix by matrix squaring')
   parser.add_argument('--beta',   default=0.1, type=float,                      help='Inverse temperature')
   parser.add_argument('--h',      default=1,   type=float,                      help='Planck\'s constant')
   parser.add_argument('-m','--m', default=1.0, type=float,                      help='Mass of particle')
   parser.add_argument('--omega',  default=1.0, type=float,                      help='Frequency')
   parser.add_argument('--n',      default=100, type=int,                        help='Number of dxs')
   parser.add_argument('--L',      default=5,   type=float,                      help='Length')
   parser.add_argument('--show',                            action='store_true', help='Show plot')
   parser.add_argument('--rows',   default=4,   type=int,                        help='Number of rows to plot')
   parser.add_argument('--cols',   default=4,   type=int,                        help='Number of columns to plot')
   parser.add_argument('--plot',   default='',                                   help='Name of plot file')
   parser.add_argument('--N',      default=None, type=int,                       help='Plot last dx only (number of dx)')
   
   args   = parser.parse_args() 
   
   beta   = args.beta  
   dx     = args.L / args.n
   grid_i = [i for i in range(-args.n,args.n+1)]          # integer grid for calculation - allow lookup
   I,J    = np.meshgrid(grid_i,grid_i)
   grid_x = [i * dx for i in range(-args.n,args.n+1)]     # grid for plotting
   X,Y    = np.meshgrid(grid_x,grid_x)                    # grid for plotting
   
   build_helpers(n        = args.n,
                 phi_mult = math.sqrt(args.m/(2*math.pi*args.h*args.h*beta)),
                 m        = args.m,
                 h        = args.h,
                 beta     = args.beta,
                 dx       = dx,
                 omega    = args.omega)
         
   rho = trotter(I,J) # Calculate starting value (good for small beta)

   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   plt.figure(figsize=(5,5))
   N = args.rows*args.cols if args.N==None else args.N  # Number of values to calculate
   for i in range(N):
      if args.N==None:  # i.e. plot for all values of beta
         plt.subplot(args.rows,args.cols,i+1)
         plot_density(X,Y,rho,beta)
         
      if i <N-1:  # Avoid redundant squaring after final plot
         beta *= 2      
         rho = np.dot(rho, rho)   # We have to use .dot, as * does elementwise multiplication
         rho *= dx                # we want an integral, not just a sum 
         
   if args.N==None:       # i.e. plot for all values of beta
      plt.tight_layout()  # Avoid scrunching plots
   else:
      plot_density(X,Y,rho,beta)

        
   plt.savefig(get_plot_file_name(args.plot))   
   
   if args.show:
      plt.show()        
