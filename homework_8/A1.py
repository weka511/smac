import random, math

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 6
MULT = 10000000
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}

T = 2.0
S = [random.choice([1, -1]) for k in range(N)]
nsteps = N * MULT
beta = 1.0 / T
Energy = energy(S, N, nbr)
E = []

for step in range(nsteps):
    k = random.randint(0, N - 1)
    delta_E = 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
    if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
        S[k] *= -1
        Energy += delta_E
    E.append(Energy)
    
print('nsteps={0}, mean energy per spin: {1}'.format(
    nsteps,
    sum(E) / float(len(E) * N)))