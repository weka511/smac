import math,  matplotlib.pyplot as plt

def orthonormality_check(n, m):
    integral_n_m = sum(psi[n][i] * psi[m][i] for i in range(nx)) * dx
    return integral_n_m

nx = 1000
L = 10.0
dx = L / (nx - 1)
x = [- L / 2.0 + i * dx for i in range(nx)]
n_states = 4
psi = [[math.exp(-x[i] ** 2 / 2.0) / math.pi ** 0.25 for i in range(nx)]]  
psi.append([math.sqrt(2.0) * x[i] * psi[0][i] for i in range(nx)])         
for n in range(2, n_states):
    psi.append([math.sqrt(2.0 / n) * x[i] * psi[n - 1][i] - \
                math.sqrt((n - 1.0) / n) * psi[n - 2][i] for i in range(nx)])
n = n_states - 1
print ('checking energy level', n)
H_psi = [0.0] +  [(- 0.5 * (psi[n][i + 1] - 2.0 * psi[n][i] + psi[n][i - 1]) /
          dx ** 2 + 0.5 * x[i] ** 2 * psi[n][i]) for i in range(1, nx - 1)]
for i in range(1, nx - 1):  
    print (n, x[i],  H_psi[i] / psi[n][i])

plt.plot([x[i] for i in range(1, nx - 1)],[H_psi[i] / psi[n][i] for i in range(1, nx - 1)] )
plt.xlabel('x')
plt.ylabel(r'$\frac{H(\psi)}{\psi}$')