import random, math

def tower_sample(weights):
    sum_w = sum(weights)
    w_cumulative = [0.0]
    for l in range(len(weights)):
        w_cumulative.append(w_cumulative[l] + weights[l])
    eta = sum_w * random.uniform(0.0, 1.0)
    kmin = 0
    kmax = len(w_cumulative)
    while True:
        k = int((kmin + kmax) / 2)
        if w_cumulative[k] < eta:
            kmin = k
        elif w_cumulative[k - 1] > eta:
            kmax = k
        else:
            return k - 1

L = 6
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
S = [random.choice([1, -1]) for k in range(N)]
E = -0.5 * sum(S[k] * sum(S[nn] for nn in nbr[k]) for k in range(N))
tot_spin_flips = N * 10000
T = 3.0
beta = 1.0 / T
E_tot = 0.0
t_tot = 0
n_spin_flips = 0
p = [0] * N
while n_spin_flips < tot_spin_flips:
    for j in range(N):
        h = sum(S[nn] for nn in nbr[j])
        delta_E = 2.0 * h * S[j]
        p[j] = min(1.0, math.exp(- beta * delta_E)) / float(N)
    log_lambda = math.log(1.0 - sum(p))
    Upsilon = random.uniform(0.0, 1.0)
    delta_t = 1 + int(math.log(Upsilon) / log_lambda)
    k = tower_sample(p)
    E_tot += delta_t * E
    t_tot += delta_t
    n_spin_flips += 1
    E += 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
    S[k] *= -1
print 'T = %f, E_av = %f' %(T, E_tot / float(t_tot) / N)
