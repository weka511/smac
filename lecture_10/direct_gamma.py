'''Integral of x**gamma, illustrating need for importance sampling'''
from random import uniform
from math   import sqrt

gamma   = -0.8
x_mean  = 1.0 / (gamma + 1.0)
n_steps = 10000
tot     = 0.0
tot_sq  = 0.0

for step in range(n_steps):
    x       = uniform(0.0, 1.0)
    tot    += x ** gamma
    tot_sq += (x ** gamma) ** 2

av    = tot / float(n_steps)
av_sq = tot_sq / float(n_steps)
err   = sqrt((av_sq - av ** 2) / n_steps)
print(f'{av} +/- {err} (exact: {x_mean})')
