from random import uniform

gamma   = -0.8
list_N  = [1, 10, 100, 1000, 10000]
n_steps = 1000000
for N in list_N:
    print (N)
    x = []
    for step in range(n_steps // N):
        Sigma = sum(uniform(0.0, 1.0) ** gamma for j in range(N))
        x.append(Sigma / float(N))
    print (x)
