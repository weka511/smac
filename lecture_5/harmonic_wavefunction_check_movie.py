import math, pylab

nx = 300  # nx is even, to avoid division by zero
L = 10.0
dx = L / (nx - 1)
x = [- L / 2.0 + i * dx for i in range(nx)]
# construct wavefunctions:
n_states = 4
psi = [[math.exp(-x[i] ** 2 / 2.0) / math.pi ** 0.25 for i in range(nx)]]  # ground state
psi.append([math.sqrt(2.0) * x[i] * psi[0][i] for i in range(nx)])         # first excited state
for n in range(2, n_states):
    psi.append([math.sqrt(2.0 / n) * x[i] * psi[n - 1][i] - \
                math.sqrt((n - 1.0) / n) * psi[n - 2][i] for i in range(nx)])
# local energy check:
H_psi_over_psi = []
for n in range(n_states):
    H_psi = [(- 0.5 * (psi[n][i + 1] - 2.0 * psi[n][i] + psi[n][i - 1])
             / dx ** 2 + 0.5 * x[i] ** 2 * psi[n][i]) for i in range(1, nx - 1)]
    H_psi_over_psi.append([H_psi[i] / psi[n][i+1] for i in range(nx - 2)])

# graphics output:
for n in range(n_states):
    pylab.plot(x[1:-1], [n + 0.5 for i in x[1:-1]], 'k--', lw=1.5)
    pylab.plot(x[1:-1], H_psi_over_psi[n], '-', lw=1.5)
    pylab.xlabel('$x$', fontsize=18)
    pylab.ylabel('$H \psi_%i(x)/\psi_%i(x)$' % (n, n), fontsize=18)
    pylab.xlim(x[0], x[-1])
    pylab.ylim(n, n + 1)
    pylab.title('Schroedinger equation check (local energy)')
    pylab.savefig('plot-check_schroedinger_energy-%i.png' % n)
    pylab.show()
