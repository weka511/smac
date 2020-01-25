# Verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator
import sys
sys.path.append('../')
import math,  matplotlib.pyplot as plt

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
print (max([abs(o-1) for o in ones]), max([abs(z) for z in zeroes]))

for n in range(n_states):
    E       = n + 0.5
    max_del = 0.0
    for i in range(len(grid_x)-2):
        x0      = grid_x[i]
        x1      = grid_x[i+1]
        x2      = grid_x[i+2]
        psi_0   = psi[x0][n]
        psi_1   = psi[x1][n]
        psi_2   = psi[x2][n]
        psi_d2  = (psi_2 - 2 * psi_1 + psi_0)/(step*step)
        lhs     = - (h*h/(2*m)) *psi_d2 + m *omega * omega *x1 *x1 *psi_1 /2
        rhs     = E *  psi_1
        max_del = max(max_del,abs(lhs-rhs))
    print (n,max_del)