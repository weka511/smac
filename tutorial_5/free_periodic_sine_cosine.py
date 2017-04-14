import math

# simmetric wavefunctions
def psi_s(x, L, n):
    return math.sqrt(2.0 / L) * math.cos(2.0 * n * math.pi * x / L)

# antysimmetric wavefunctions
def psi_a(x, L, n):
    return math.sqrt(2.0 / L) * math.sin(2.0 * n * math.pi * x / L)

ntot = 21     # odd number
beta = 1.0
nx = 100
L = 10.0
x = [i * L / float(nx - 1) for i in range(nx)]
rho = []
for i in range(nx):
    rho.append([1.0 / L + sum(
              math.exp(- beta * 2.0 * (math.pi * n / L) ** 2) *
              (psi_s(x[i], L, n) * psi_s(x[j], L, n) + 
              psi_a(x[i], L, n) * psi_a(x[j], L, n) )
              for n in range(1, (ntot + 1) // 2))
              for j in range(nx)])
