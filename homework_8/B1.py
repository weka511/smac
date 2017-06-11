import random, math, numpy as np

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 6
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}

T = 2.0
p  = 1.0 - math.exp(-2.0 / T)
nsteps = 100000

def mean_energy_per_spin(replace=True):
    S = [random.choice([1, -1]) for k in range(N)]
    E = [energy(S, N, nbr)]
    for step in range(nsteps):
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            j = random.choice(Pocket) if replace else Pocket.pop()
            for l in nbr[j]:
                if S[l] == S[j] and l not in Cluster \
                       and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
            if replace: Pocket.remove(j)
        for j in Cluster:
            S[j] *= -1
        E.append(energy(S, N, nbr))
    return sum(E) / float(len(E) * N)

for replace in [False,True]:
    if replace:
        print ('Replace: nsteps={0}'.format(nsteps))
    else:
        print ('Not replacing: nsteps={0}'.format(nsteps))
    Es = []
    random.seed(666)
    for i in range(100):
        Es.append(mean_energy_per_spin(replace))
    print ('mean energy per spin: {0}({1})'.format(np.mean(Es),np.std(Es)))

# 25 iterations

# Not replacing: nsteps=100000
#mean energy per spin: -1.7471661727827168(0.0013039725134781827)
#Replace: nsteps=100000
#mean energy per spin: -1.7471622617107163(0.0010715419957611307)
