import random

N = 3
statistics = {}
L = list(range(N))
nsteps = 10000
for step in range(nsteps):
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)
    L[i], L[j] = L[j], L[i]
    if tuple(L) in statistics: 
        statistics[tuple(L)] += 1
    else:
        statistics[tuple(L)] = 1
    print (L)
    print (list(range(N)))
    print ()

for item in statistics:
    print (item, statistics[item])
