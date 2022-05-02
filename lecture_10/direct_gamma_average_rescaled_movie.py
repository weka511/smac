import random, math, cmath, pylab

def pi_exact(x, gamma, c0, c1):
    alpha = -1.0 / gamma
    t_min, t_max = -20.0, 20.0
    n_t = 1000
    delta_t = (t_max - t_min) / float(n_t)
    tot = 0.0
    for j in range(n_t):
        t = t_min + j * delta_t
        tot += cmath.exp(-1j * x * t - (c0 * abs(t) ** alpha + 1j * c1 * t * abs(t) ** (alpha - 1.0)))
    tot *= delta_t
    tot /= (2.0 * math.pi)
    return tot.real
        
# Warning: the values of the coefficients c0 and c1 used here are specific for the case of gamma=-0.8
gamma = -0.8
c0, c1 = 1.8758, 4.5286
x_mean = 5.0
list_N = [10, 100, 1000, 10000]
n_steps = 10000000
for N in list_N:
    print N
    x = []
    for step in xrange(n_steps / N):
        Sigma = sum(random.uniform(0.0, 1.0) ** gamma for j in xrange(N))
        x.append((Sigma / float(N) - x_mean) * float(N) ** (1.0 + gamma))
    pylab.hist(x, bins=100, normed=True, alpha=0.5, range=[-10.0, 10.0], label='N=%i' % N)
x_stable = [-10.0 + i * 0.1 for i in range(200)]
y_stable = [pi_exact(x, gamma, c0, c1) for x in x_stable]
pylab.plot(x_stable, y_stable, 'r', lw=2.5, label='Levy stable distr.')
pylab.legend()
pylab.axis([-10.0, 10.0, 0.0, 0.3])
pylab.xlabel('rescaled average $\Upsilon$', fontsize=18)
pylab.ylabel('histogram $\pi(\Upsilon)$', fontsize=18)
pylab.title('$\gamma=%f$' % gamma, fontsize=18)
pylab.savefig('histo_direct_gamma_average_rescaled.png')
