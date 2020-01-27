# template.py

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

m          = 1
h          = 1
beta       = 1
omega      = 1
step       = 1
phi_mult   = math.sqrt(m/(2*math.pi*h*h*beta)) #FIXME
phi_helper = {}
V          = {}


@np.vectorize
def trotter(i,j):
   rho_free = phi_mult if i==j else phi_mult*phi_helper[abs(i-j)]
   return V[abs(i)] * rho_free * V[abs(j)]
   
def matrix_square(X,Y,beta=1,V=lambda x:0):
    pass

if __name__=='__main__':
   import argparse
      
   parser = argparse.ArgumentParser('Template')
   parser.add_argument('--beta',default=0.1,type=float,help='Inverse temperature')
   parser.add_argument('-m','--m',default=1.0,type=float,help='Mass of particle')
   parser.add_argument('--omega',default=1.0,type=float,help='Frequency')
   parser.add_argument('--n',default=100,type=int,help='Number of steps')
   parser.add_argument('--L',default=3,type=float,help='Length')
   parser.add_argument('--show',action='store_true',help='Show plot')
   args   = parser.parse_args()
   m         = args.m
#   h         = 1
   beta      = args.beta
   omega     = args.omega   
   step     = args.L / args.n
   grid_i   = [i for i in range(-args.n,args.n+1)]
   I,J      = np.meshgrid(grid_i,grid_i)
   grid_x   = [i * step for i in range(-args.n,args.n+1)]
   X,Y      = np.meshgrid(grid_x,grid_x)
   for i in range(-args.n,args.n+1):
      for j in range(i+1,args.n+1):
         if not (j-i) in phi_helper:
            phi_helper[(j-i)] = math.exp(- (m *step*step*(i-j)*(i-j))/(2*h*h*beta))
   for i in range(args.n+1):
      V[i]= math.exp(-0.5 * beta * 0.5 * m * omega * omega * step * step *i * i)
      
   rho_free = trotter(I,J)
   #Z= matrix_square(X,Y,beta=args.beta,V=lambda x:0.5*args.m*args.omega*args.omega)
   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   plt.figure(figsize=(5,5))
   plt.pcolor(X,Y,rho_free)
   plt.colorbar()
   plt.savefig('{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0]))    
   if args.show:
      plt.show()        
