'''Algorithm 6.1:  direct sampling for N pins'''

from random import uniform

N         = 15
L         = 10.0
sigma     = 0.075
n_configs = 100

for config in range(n_configs):
    while True:
        x = [uniform(sigma, L - sigma) for k in range(N)]
        x.sort()
        min_dist = min(x[k + 1] - x[k] for k in range(N - 1))
        if min_dist > 2.0 * sigma:
            print (x)
            break
