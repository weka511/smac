from math   import sinh, sqrt, tanh
from pylab  import legend, plot, show, title, xlabel, xlim, ylabel
from random import gauss

beta         = 2.0
N            = 100
dtau         = beta / N
xstart, xend = 2.0, 1.0
colours      = ['r','g','b','y','c','m','k']

for step in range(len(colours)):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / tanh(dtau) + 1.0 / tanh(dtau_prime)
        Ups2 = x[k - 1] / sinh(dtau) + xend / sinh(dtau_prime)
        x.append(gauss(Ups2 / Ups1, 1.0 / sqrt(Ups1)))
    x.append(xend)

    plot(x,
         [j * dtau for j in range(N + 1)],
         'o-',
         color=colours[step],
         label='{}'.format(step))
xlabel('$x$', fontsize=18)
ylabel('$\\tau$', fontsize=18)
title('Harmonic paths')
legend()
xlim(-2.0, 4.0)

show()
