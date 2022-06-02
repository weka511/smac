'''
Construct path using direct sanpling (inefficient)
'''
from math   import exp
from random import randint, random, uniform

def rho_free(x, y, beta):    # free off-diagonal density matrix
    return exp(-(x - y) ** 2 / (2.0 * beta))

beta    = 4.0
N       = 8                  # number of slices
dtau    = beta / N
delta   = 1.0                # maximum displacement of one bead
n_steps = 20                 # number of Monte Carlo steps
x       = [0.0] * N          # initial path

for step in range(n_steps):
    k            = randint(0, N - 1)                  # random slice
    knext, kprev = (k + 1) % N, (k - 1) % N           # next/previous slices
    x_new        = x[k] + uniform(-delta, delta)      # proposed new position at slice k
    old_weight   = (rho_free(x[knext], x[k], dtau) *
                    rho_free(x[k], x[kprev], dtau) *
                    exp(-0.5 * dtau * x[k] ** 2))
    new_weight   = (rho_free(x[knext], x_new, dtau) *
                    rho_free(x_new, x[kprev], dtau) *
                    exp(-0.5 * dtau * x_new ** 2))
    if random() < new_weight / old_weight:
        x[k] = x_new
    print (x)
