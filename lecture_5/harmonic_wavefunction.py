# Plot solutions to Schroedinger's equation for Simple Harmonic Oscillator
import sys
sys.path.append('../')
import math,  matplotlib.pyplot as plt

n_states = 17
n_steps  = 100
step     = 5.0/n_steps

grid_x   = [i * step for i in range(-n_steps, n_steps+1)]
psi      = {}

for x in grid_x:
    psi[x] = [math.exp(-x ** 2 / 2.0) / math.pi ** 0.25]  # ground state
    psi[x].append(math.sqrt(2.0) * x * psi[x][0])         # first excited state
    # other excited states (through recursion):
    for n in range(2, n_states):
        psi[x].append(math.sqrt(2.0 / n) * x * psi[x][n - 1] -
                      math.sqrt((n - 1.0) / n) * psi[x][n - 2])
for n in range(n_states):
    print ('level %i:' % n, [psi[x][n] for x in grid_x])    
    g,=plt.plot(grid_x,[psi[x][n] for x in grid_x],label=str(n))

plt.grid()    
plt.legend([str(n)for n in range(n_states) ])
plt.xlabel('x')
plt.ylabel(r'$\psi$')
plt.title('Harmonic wave function')
plt.savefig('harmonic.png')
plt.show()