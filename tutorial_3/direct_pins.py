import random

N = 15
L = 10.0
sigma = 0.2
n_configs = 100
for config in range(n_configs):
    n_rejected=0
    x = []
    while len(x) < N:
        x.append(random.uniform(sigma, L - sigma))
        for k in range(len(x) - 1):
            if abs(x[-1] - x[k]) < 2.0 * sigma:
                x = []
                n_rejected+=1
                break
    print (n_rejected, x)
