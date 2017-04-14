import random

N = 10
L = 20.0
sigma = 0.75
n_runs = 800
for run in range(n_runs):
    y = [random.uniform(0.0, L - 2 * N * sigma) for k in range(N)]
    y.sort()
    print ([y[i] + (2 * i + 1) * sigma for i in range(N)])
