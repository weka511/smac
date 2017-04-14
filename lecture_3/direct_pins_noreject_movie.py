import random, pylab

N = 10
L = 20.0
sigma = 0.75
n_runs = 800
data = []
for run in range(n_runs):
    y = [random.uniform(0.0, L - 2 * N * sigma) for k in range(N)]
    y.sort()
    data += [y[i] + (2 * i + 1) * sigma for i in range(N)]
pylab.xlabel('$x$', fontsize=14)
pylab.ylabel('$\pi(x)$', fontsize=14)
pylab.title('Density of %i clothes-pins ($\sigma$=%s) on a line of length L=%s' % (N, sigma, L))
pylab.hist(data, bins=200, normed=True)
pylab.savefig('plot-direct_pins_noreject.png')
pylab.show()
