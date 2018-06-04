import random

N = 8
nsteps = 100
L = list(range(N))
for step in range(nsteps):
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)
    L[i], L[j] = L[j], L[i]
    print (L[0])