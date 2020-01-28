# matrix-square-check.py

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

# Exercise 3.4: check Alg 3.3, matrix-squares

import math,matplotlib.pyplot as plt,numpy as np,os
from matplotlib import rc

# Cache some values to speec up calculation

sinh_factor = None
tanh_factor = None
coth_factor = None

@np.vectorize
def density(x, y):
    return sinh_factor *math.exp(-(x+y)**2 * tanh_factor/4 - (x-y)**2 * coth_factor/4)

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
    
    parser = argparse.ArgumentParser('Check results of matrix squaring against exact solution')
    parser.add_argument('--beta',   default=0.1, type=float,                      help='Inverse temperature')
    parser.add_argument('--h',      default=1,   type=float,                      help='Planck\'s constant')
    parser.add_argument('-m','--m', default=1.0, type=float,                      help='Mass of particle')
    parser.add_argument('--omega',  default=1.0, type=float,                      help='Frequency')
    parser.add_argument('--n',      default=100, type=int,                        help='Number of steps')
    parser.add_argument('--L',      default=5,   type=float,                      help='Length')    
    parser.add_argument('--show',                           action='store_true',  help='Show plot')
    parser.add_argument('--plot', default='',                                     help='Name of plot file')
    
    args        = parser.parse_args()
    beta        = args.beta  
    step        = args.L / args.n
    grid_x      = [i * step for i in range(-args.n,args.n+1)]   # grid for plotting
    X,Y         = np.meshgrid(grid_x,grid_x)                    # grid for plotting 
    sinh_factor = math.sqrt(1/(2 * math.pi * math.sinh(beta)))
    tanh_factor = math.tanh(beta/2)
    coth_factor = 1/math.tanh(beta/2)

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    plt.figure(figsize=(5,5))
    plt.pcolor(X,Y,density(X,Y))
    plt.colorbar()
    plt.xlabel('$x$')
    plt.ylabel(r'$x^{\prime}$')
    plt.title(r'$\rho(x,x^{{\prime}},{0:.3f})$'.format(beta))
    plt.savefig(get_plot_file_name(args.plot))   
    if args.show:
        plt.show()    
