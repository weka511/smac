# harmonic_wavefunction.py

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
import math

n_states = 17
n_steps  = 100000
L        = 500
step     = L / n_steps
omega    = 1
m        = 1
h        = 1

grid_x   = [i * step for i in range(-n_steps, n_steps+1)]
psi      = {}

for x in grid_x:
    psi[x] = [math.exp(-(m * omega**2 /2 )*x ** 2 ) / math.pi ** 0.25]  # ground state
    psi[x].append(math.sqrt(2.0) * x * psi[x][0])         # first excited state
    # other excited states (through recursion):
    for n in range(2, n_states):
        psi[x].append(math.sqrt(2.0 / n) * x * psi[x][n - 1] -
                      math.sqrt((n - 1.0) / n) * psi[x][n - 2])

ones   = [step*sum(psi[x][i]*psi[x][i] for x in grid_x) for i in range(n_states)]
zeroes = [sum(psi[x][i]*psi[x][j] for x in grid_x) for i in range(n_states) for j in range(i)]
print (
    'Maximum deviation: from normalization={0}, from orthogonality {1}'.format(
    max([abs(o-1) for o in ones]), 
    max([abs(z) for z in zeroes])))

for n in range(n_states):
    E       = n + 0.5
    max_del = 0.0
    for i in range(len(grid_x)-2):
        x0               = grid_x[i]
        x1               = grid_x[i+1]
        x2               = grid_x[i+2]
        psi_0            = psi[x0][n]
        psi_1            = psi[x1][n]
        psi_2            = psi[x2][n]
        psi_d2           = (psi_2 - 2 * psi_1 + psi_0)/(step*step) # 2nd derivative
        schroedinger_lhs = - (h*h/(2*m)) *psi_d2 + m *omega * omega *x1 *x1 *psi_1 /2
        schroedinger_rhs = E *  psi_1
        max_del          = max(max_del,abs(schroedinger_lhs-schroedinger_rhs))
    print ('Maximum deviation from Schroedinger, Energy {0} is {1}'.format(E,max_del))