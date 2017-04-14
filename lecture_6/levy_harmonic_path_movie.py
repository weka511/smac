import math, random, pylab

beta = 2.0
N = 10
dtau = beta / N
nsteps = 5
xstart, xend = 2.0, 1.0
for step in range(nsteps):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
                 1.0 / math.sqrt(Ups1)))
    x.append(xend)
    # graphics
    pylab.plot(x, [j * dtau for j in range(N + 1)], 'bo-')
    pylab.xlabel('$x$', fontsize=18)
    pylab.ylabel('$\\tau$', fontsize=18)
    pylab.title('Harmonic path %i' % step)
    pylab.xlim(-2.0, 4.0)
    pylab.show()
    pylab.close()

