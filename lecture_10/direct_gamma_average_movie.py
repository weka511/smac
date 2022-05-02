import random, pylab

gamma = -0.8
list_N = [1, 10, 100, 1000, 10000]
n_steps = 1000000
for N in list_N:
    print N
    x = []
    for step in xrange(n_steps / N):
        Sigma = sum(random.uniform(0.0, 1.0) ** gamma for j in xrange(N))
        x.append(Sigma / float(N))
    pylab.hist(x, bins=125, normed=True, alpha=0.5, range=[0.0, 10.0], label='N=%i' % N)
pylab.axvline(5.0, c='k', lw=2.0, ls='--')
pylab.legend()
pylab.xlim(1.0, 10.0)
pylab.xlabel('average $\Sigma_N / N$', fontsize=18)
pylab.ylabel('histogram $\pi(\Sigma_N / N)$', fontsize=18)
pylab.title('$\gamma=%f$' % gamma, fontsize=18)
pylab.savefig('histo_direct_gamma_average.png')
