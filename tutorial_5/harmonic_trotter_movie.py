import math, pylab

# density matrix for a free particle (exact)
def funct_rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

beta = 0.1
nx = 300
L = 10.0
x = [-L / 2.0 + i * L / float(nx - 1) for i in range(nx)]
rho_free, rho_harm = [], []
for i in range(nx):
    rho_free.append([funct_rho_free(x[i], x[j], beta) for j in range(nx)])
    rho_harm.append([rho_free[i][j] * math.exp(- beta * x[i] ** 2 / 4.0 -
                     beta * x[j] ** 2 / 4.0) for j in range(nx)])

# graphics output (free particle)
pylab.imshow(rho_free, extent=[0.0, L, 0.0, L], origin='lower')
pylab.xlabel('$x$', fontsize=16)
pylab.ylabel('$x\'$', fontsize=16)
pylab.colorbar()
pylab.title('$\\beta$=%s (free)' % beta)
pylab.savefig('plot-trotter-free.png')
pylab.clf()
# graphics output (harmonic potential)
pylab.imshow(rho_harm, extent=[0.0, L, 0.0, L], origin='lower')
pylab.xlabel('$x$', fontsize=16)
pylab.ylabel('$x\'$', fontsize=16)
pylab.colorbar()
pylab.title('$\\beta$=%s (harmonic)' % beta)
pylab.savefig('plot-trotter-harmonic.png')
