import scipy.special, random, math

n_trials = 100000
for trial in xrange(n_trials):
    Upsilon = random.uniform(0.0, 1.0)
    x = math.sqrt(2.0) * scipy.special.erfinv(2.0 * Upsilon - 1.0)
    print x

