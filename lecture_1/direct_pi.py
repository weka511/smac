'''Algorithm 1.1 - compute pi using direct sampling'''

from random import uniform

n_trials = 4000
n_hits   = 0
for iter in range(n_trials):
    x, y = uniform(-1.0, 1.0), uniform(-1.0, 1.0)
    if x**2 + y**2 < 1.0:
        n_hits += 1
print (4.0 * n_hits / float(n_trials))
