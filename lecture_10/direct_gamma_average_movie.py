'''Histogram of Integral of x**gamma, illustrating need for importance sampling'''
from random import uniform
from matplotlib.pyplot import axvline, hist, legend, savefig, show, title, xlabel, xlim, ylabel

gamma   = -0.8
list_N  = [1, 10, 100, 1000, 10000]
n_steps = 1000000

for N in list_N:
    print (N)
    x = []
    for step in range(n_steps // N):
        Sigma = sum(uniform(0.0, 1.0) ** gamma for j in range(N))
        x.append(Sigma / float(N))
    hist(x, bins=125, density=True, alpha=0.5, range=[0.0, 10.0], label='N=%i' % N)

axvline(5.0,
        c  = 'k',
        lw = 2.0,
        ls = '--')
legend()
xlim(1.0, 10.0)
xlabel('average $\Sigma_N / N$', fontsize=18)
ylabel('histogram $\pi(\Sigma_N / N)$', fontsize=18)
title('$\gamma=%f$' % gamma, fontsize=18)
savefig('histo_direct_gamma_average.png')
show()
