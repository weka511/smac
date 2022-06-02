'''Algorithm 6.2: rejection free sampling'''

from random import uniform
from pylab import hist, savefig, show, title, xlabel, ylabel

N      = 10
L      = 20.0
sigma  = 0.75
n_runs = 800
data   = []

for run in range(n_runs):
    y = [uniform(0.0, L - 2 * N * sigma) for k in range(N)]
    y.sort()
    data += [y[i] + (2 * i + 1) * sigma for i in range(N)]
xlabel('$x$',
       fontsize = 14)
ylabel('$\pi(x)$',
       fontsize = 14)
title(f'Density of {N} clothes-pins, $\sigma$={sigma}, on a line of length L={L}')
hist(data,
     bins    = 200,
     density = True)
savefig('plot-direct_pins_noreject.png')
show()
