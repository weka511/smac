'''Algorithm 2.2: generating a hard disk configuration from another one using a Markov chain'''
from random import choice, uniform

L        = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
sigma    = 0.15
delta    = 0.1
n_steps  = 1000

def markov_step_box(sigma,delta):
    for _ in range(n_steps):
        a           = choice(L)   # choose a disk
        b           = [a[0] + uniform(-delta, delta),   # propose new position
                       a[1] + uniform(-delta, delta)]
        min_dist_squared       = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
        new_positon_within_box = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
        if not (new_positon_within_box or min_dist_squared < 4.0 * sigma ** 2):
            a[:] = b

print (L)
markov_step_box(sigma,delta)
