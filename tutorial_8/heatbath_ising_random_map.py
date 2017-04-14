import random, math, os

L = 16
N = L * L
filename = 'data_L%i.txt' % L
if os.path.isfile(filename):
    f = open(filename, 'r')
    S = [int(i) for i in f.read().split()]
    f.close()
    if len(S) != N: exit('wrong input')
    print 'initial config read from', filename
else:
    S = [1] * N
    print 'initial config: all sites up'
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}
nsteps = 100000
beta = 0.5
random.seed('123456')
for step in range(nsteps):
    k = random.randint(0, N - 1)
    Upsilon = random.uniform(0.0, 1.0)
    h = sum(S[nn] for nn in nbr[k])
    S[k] = -1
    if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h)):
        S[k] = 1
