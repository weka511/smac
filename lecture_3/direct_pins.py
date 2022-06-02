'''Algorithm 6.1:  direct sampling for N pins'''

from random import uniform

N         = 15
L         = 10.0
sigma     = 0.1
n_configs = 100

for config in range(n_configs):
    x = []
    while len(x) < N:
        x.append(uniform(sigma, L - sigma))
        for k in range(len(x) - 1):
            if abs(x[-1] - x[k]) < 2.0 * sigma:
                x = []
                break
    print (x)
