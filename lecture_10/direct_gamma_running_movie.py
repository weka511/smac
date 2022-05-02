import random, pylab

gamma = -0.8
n_steps = 5000000
tot = 0.0
running = []
for step in xrange(n_steps):
    tot += random.uniform(0.0, 1.0) ** gamma
    av = tot / float(step + 1)
    running.append(av)
pylab.plot(running)
pylab.axhline(1.0 / (1.0 + gamma), c='r', ls='--', lw=2.5, label='value of the $\gamma$-integral')
pylab.ylim(2.0, 8.0)
pylab.ylabel('running average $\Sigma_n/n$', fontsize=18)
pylab.xlabel('number of samples $n$', fontsize=18)
pylab.legend()
pylab.savefig('running_average.png')
