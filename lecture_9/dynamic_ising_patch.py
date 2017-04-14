import random, math

def naive_tower_sample(weights, sum_w):
    w_cumulative = [0.0]
    for l in range(len(weights)):
        w_cumulative.append(w_cumulative[l] + weights[l])
    eta = sum_w * random.uniform(0.0, 1.0)
    for k in range(1, len(w_cumulative)):
        if eta < w_cumulative[k]:
            return k - 1

def init_classes(S, N, nbr):
    class_to_site = {k:[] for k in range(10)}
    site_to_class = {}
    dict_class = {(1, 4):0, (1, 2):1, (1, 0):2, (1, -2):3, (1, -4):4,
             (-1, 4):5, (-1, 2):6, (-1, 0):7, (-1, -2):8, (-1, -4):9}
    for site in range(N):
        h = sum(S[nn] for nn in nbr[site])
        class_site = dict_class[(S[site], h)]
        site_to_class[site] = class_site
        class_to_site[class_site].append(site)
    return class_to_site, site_to_class

def f_neighb(old_class_neighbour, old_class_site):
    if old_class_neighbour < 5: return (old_class_site + 1)
    else:                       return (old_class_site - 1)

L = 6
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
S = [random.choice([1, -1]) for k in range(N)]
E = -0.5 * sum(S[k] * sum(S[nn] for nn in nbr[k]) for k in range(N))
T = 2.0
beta = 1.0 / T
class_to_site, site_to_class = init_classes(S, N, nbr)
delta_E = [8, 4, 0, -4, -8, -8, -4, 0, 4, 8]
p_metropolis = [min(1.0, math.exp(-beta * delta_E[k])) / float(N) for k in range(10)]
tot_spin_flips = N * 50000
E_tot = 0.0
t = 0
n_spin_flips = 0
while n_spin_flips < tot_spin_flips:
    p = [len(class_to_site[k]) * p_metropolis[k] for k in range(10)]
    delta_t = 1 + int(math.log(random.uniform(0.0, 1.0)) / math.log(1.0 - sum(p)))
    E_tot += delta_t * E
    t += delta_t
    n_spin_flips += 1
    old_class_k = naive_tower_sample(p, sum(p))
    new_class_k = (old_class_k + 5) % 10 
    k = random.choice(class_to_site[old_class_k])
    class_to_site[old_class_k].remove(k)
    class_to_site[new_class_k].append(k)
    site_to_class[k] = new_class_k
    for m in nbr[k]:
        old_class_m = site_to_class[m]
        new_class_m = f_neighb(old_class_k, old_class_m)
        class_to_site[old_class_m].remove(m)
        class_to_site[new_class_m].append(m)
        site_to_class[m] = new_class_m
    E += delta_E[old_class_k]
    S[k] *= -1
print 'T = %f, E_av = %f' %(T, E_tot / float(t) / N)
