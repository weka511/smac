import random

gamma = -0.5
n_trials = 10000
for trial in xrange(n_trials):
    x = (random.uniform(0.0, 1.0)) ** (1.0 / (gamma + 1.0))
    print x
