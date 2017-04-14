import math, random, pylab, os

def rho_free(x, y, beta):        # free off-diagonal density matrix
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

output_dir = 'snapshots_naive_harmonic_path'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def show_path(x, k, x_old, Accepted, step):
    path = x + [x[0]]
    y_axis = range(len(x) + 1)
    if Accepted:
        old_path = x[:]
        old_path[k] = x_old
        old_path = old_path + [old_path[0]]
        pylab.plot(old_path, y_axis, 'ro--', label='old path')
    pylab.plot(path, y_axis, 'bo-', label='new path')
    pylab.legend()
    pylab.xlim(-5.0, 5.0)
    pylab.xlabel('$x$', fontsize=14)
    pylab.ylabel('$\\tau$', fontsize=14)
    pylab.title('Naive path integral Monte Carlo, step %i' % step)
    pylab.savefig(output_dir + '/snapshot_%05i.png' % step)
    pylab.clf()

beta = 4.0
N = 8                                                # number of slices
dtau = beta / N
delta = 1.0                                          # maximum displacement on one slice
n_steps = 30                                         # number of Monte Carlo steps
x = [random.uniform(-1.0, 1.0) for k in range(N)]   # initial path
show_path(x, 0, 0.0, False, 0)
for step in range(n_steps):
    print ('step',step)
    k = random.randint(0, N - 1)                     # randomly choose slice
    knext, kprev = (k + 1) % N, (k - 1) % N          # next/previous slices
    x_old = x[k]
    x_new = x[k] + random.uniform(-delta, delta)     # new position at slice k
    old_weight  = (rho_free(x[knext], x_old, dtau) *
                   rho_free(x_old, x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x_old ** 2))
    new_weight  = (rho_free(x[knext], x_new, dtau) *
                   rho_free(x_new, x[kprev], dtau) *
                   math.exp(-0.5 * dtau * x_new ** 2))
    Accepted= random.uniform(0.0, 1.0) < new_weight / old_weight
    if Accepted:
        x[k] = x_new

    show_path(x, k, x_old, Accepted, step + 1)

