import math, pylab

# symmetric wavefunctions
def psi_s(x, L, n):
    return math.sqrt(2.0 / L) * math.cos(2.0 * n * math.pi * x / L)

# antisymmetric wavefunctions
def psi_a(x, L, n):
    return math.sqrt(2.0 / L) * math.sin(2.0 * n * math.pi * x / L)

def rho_term(x_i,x_j,n):
    return math.exp(- beta * 2.0 * (math.pi * n / L) ** 2) * \
           (psi_s(x_i, L, n) * psi_s(x_j, L, n) +           \
            psi_a(x_i, L, n) * psi_a(x_j, L, n) ) 

ntot = 21     # odd number
beta = 0.1
nx = 100
L = 10.0
x = [i * L / float(nx - 1) for i in range(nx)]
rho = []
for i in range(nx):
    rho.append([1.0 / L +\
                sum(rho_term(x[i],x[j],n) for n in range(1, (ntot + 1) // 2)) for j in range(nx)])

# graphics output
pylab.imshow(rho, extent=[0.0, L, 0.0, L], origin='lower')
pylab.colorbar()
pylab.title('$\\beta$=%s (sine/cosine)' % beta)
pylab.xlabel('$x$', fontsize=16)
pylab.ylabel('$x\'$', fontsize=16)
pylab.savefig('plot-periodic-sine_cosine.png')
