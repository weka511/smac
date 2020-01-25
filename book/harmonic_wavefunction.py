# Verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator
import sys
sys.path.append('../')
import math,  matplotlib.pyplot as plt

n_states = 17
n_steps  = 10000
L        = 500
step     = L / n_steps
omega    = 1
m        = 1
grid_x   = [i * step for i in range(-n_steps, n_steps+1)]
psi      = {}

for x in grid_x:
    psi[x] = [math.exp(-(m * omega**2 /2 )*x ** 2 ) / math.pi ** 0.25]  # ground state
    psi[x].append(math.sqrt(2.0) * x * psi[x][0])         # first excited state
    # other excited states (through recursion):
    for n in range(2, n_states):
        psi[x].append(math.sqrt(2.0 / n) * x * psi[x][n - 1] -
                      math.sqrt((n - 1.0) / n) * psi[x][n - 2])

print (list(step*sum(psi[x][i]*psi[x][i] for x in grid_x) for i in range(n_states)))
print (list(sum(psi[x][i]*psi[x][j] for x in grid_x) for i in range(n_states) for j in range(i)))

