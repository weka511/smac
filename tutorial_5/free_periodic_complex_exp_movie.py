import math, cmath, pylab

ntot = 21   # odd number
beta = 1.0
nx = 100
L = 10.0
x = [i * L / float(nx - 1) for i in range(nx)]
rho_complex = []
for i in range(nx):
    rho_complex.append([sum(
              math.exp(- 2.0 * beta * (math.pi * n / L) ** 2) *
              cmath.exp(1j * 2.0 * n * math.pi * (x[i] - x[j]) / L) / L
              for n in range(-(ntot - 1) // 2, (ntot + 1) // 2))
              for j in range(nx)])
rho_real = [[rho_complex[i][j].real for i in range(nx)] for j in range(nx)]

# graphics output
pylab.imshow(rho_real, extent=[0.0, L, 0.0, L], origin='lower')
pylab.colorbar()
pylab.title('$\\beta$=%s (complex exp)' % beta)
pylab.xlabel('$x$', fontsize=16)
pylab.ylabel('$x\'$', fontsize=16)
pylab.savefig('plot-periodic-complex.png')
