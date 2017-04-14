import random, pylab

def dist(x1, x2, L):
    d_x = abs(x1 - x2) 
    return min(d_x, L - d_x)

N = 450
L = 500.0
sigma = 0.5
density = N * 2.0 * sigma / L
n_runs = 100
x_max = 30.0  # maximum of the histogram range
data, pair_corr = [], []
for run in range(n_runs):
    Lprime = L - 2.0 * sigma
    y_sorted = [random.uniform(0, Lprime - 2.0 * (N - 1.0) * sigma) for k in xrange(N - 1)]
    y_sorted.sort()
    sample = [y_sorted[k] + (2.0 * k + 1.0) * sigma for k in xrange(N - 1) ] + [L - sigma]
    pair_corr += [dist(sample[i], sample[j], L) for i in xrange(N) for j in xrange(i)]
histo, bins, patches = pylab.hist(pair_corr, bins=800, normed=True)
pylab.xlim(0.0, x_max)
pylab.title('Pair-correlation function $\pi(x,y)$\nN=%i, $\sigma$=%.2f, L=%.1f, density=%.2f' % (N, sigma, L, density))
pylab.xlabel('$|x-y|$', fontsize=14)
pylab.ylabel('$\pi(|x-y|)$', fontsize=14)
pylab.savefig('plot-pins_noreject_periodic-N%04i-L%.1f-pair_corr.png' % (N, L))
pylab.show()
pylab.clf()
asymptotic_val = 1.0 / (L / 2.0)   # asymptotic value of the pair correlation function
pylab.semilogy(bins[:-1], [abs(y - asymptotic_val) for y in histo])
pylab.xlim(0.0, x_max)
pylab.title('Deviation of $\pi(x,y)$ from its asymptotic value\nN=%i, $\sigma$=%.2f, L=%.1f, density=%.2f' % (N, sigma, L, density))
pylab.xlabel('$|x-y|$', fontsize=14)
pylab.ylabel('$|\pi(|x-y|)-\pi_\mathrm{asympt}|$', fontsize=14)
pylab.savefig('plot-pins_noreject_periodic-N%04i-L%.1f-pair_corr_deviation.png' % (N, L))
pylab.show()
