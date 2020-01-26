# harmonic_density.py

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

# Verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator

import sys
sys.path.append('../')
import math,matplotlib.pyplot as plt,numpy as np
from matplotlib import rc

# density
#
# Calculate values of density matrix
@np.vectorize
def density(a, b):
    psi_x       = psi[a]
    psi_x_prime = psi[b]
    return sum([psi_x[i] * psi_x_prime[i] * math.exp(- beta * (i+0.5)) for i in range(n_states)])
        
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

n_states = 17
n_steps  = 100
L        = 5
step     = L / n_steps
omega    = 1
m        = 1
h        = 1
beta     = 2
M        = 4
N        = 4
grid_x   = [i * step for i in range(-n_steps, n_steps+1)]
X,Y      = np.meshgrid(grid_x,grid_x)
psi      = {}


for x in grid_x:
    psi[x] = [math.exp(-(m * omega**2 /2 )*x ** 2 ) / math.pi ** 0.25]  # ground state
    psi[x].append(math.sqrt(2.0) * x * psi[x][0])         # first excited state
    # other excited states (through recursion):
    for n in range(2, n_states):
        psi[x].append(math.sqrt(2.0 / n) * x * psi[x][n - 1] -
                      math.sqrt((n - 1.0) / n) * psi[x][n - 2])
        
plt.figure(figsize=(20,20))
for i in range(M*N):
    plt.subplot(M,N,i+1)
    plt.pcolor(X,Y,density(X,Y))
    plt.colorbar()
    plt.xlabel('$x$')
    plt.ylabel(r'$x^{\prime}$')
    plt.title(r'$\rho(x,x^{{\prime}},{0:.3f})$'.format(beta))
    beta /= 2

plt.savefig('harmonic-density.png')    
plt.show()