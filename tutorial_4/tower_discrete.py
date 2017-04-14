import random

# bisection search to find the bin corresponding to eta
def bisection_search(eta, w_cumulative):
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

# sample an integer number according to weights
def tower_sample(weights):
    sum_w = sum(weights)
    w_cumulative = [0.0]
    for l in xrange(len(weights)):
        w_cumulative.append(w_cumulative[l] + weights[l])
    eta = random.random() * sum_w
    sampled_choice = bisection_search(eta, w_cumulative)
    return sampled_choice

weights = [0.4, 0.3, 0.8, 0.1, 0.2]
n_samples = 20
for sample in xrange(n_samples):
    print tower_sample(weights)

