import random, math

gamma = -0.8
x_mean = 1.0 / (gamma + 1.0)
n_steps = 10000
tot = 0.0
tot_sq = 0.0
for step in xrange(n_steps):
    x = random.uniform(0.0, 1.0)
    tot += x ** gamma
    tot_sq += (x ** gamma) ** 2
av = tot / float(n_steps)
av_sq = tot_sq / float(n_steps)
err = math.sqrt((av_sq - av ** 2) / n_steps)
print '%f +/- %f (exact: %f)' % (av, err, x_mean)
