import math, random, pylab

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

dtau_prime  = 0.1
dtau_dprime = 0.2
x_prime  = 0.0
x_dprime = 1.0
delta = 1.0                 # maximum displacement of xk
n_steps = 100000            # number of Monte Carlo steps
data_hist = []
xk = 0.0                    # initial value of xk
for step in range(n_steps):
    xk_new = xk + random.uniform(-delta, delta)
    old_weight  = (rho_free(x_dprime, xk, dtau_dprime) *
                   rho_free(xk, x_prime, dtau_prime))
    new_weight  = (rho_free(x_dprime, xk_new, dtau_dprime) * 
                   rho_free(xk_new, x_prime, dtau_prime))
    if random.random() < new_weight / old_weight:
        xk = xk_new
    data_hist.append(xk)

def pi_analytic(xk, x_prime, x_dprime, dtau_prime, dtau_dprime):
    mean = (dtau_dprime * x_prime + dtau_prime * x_dprime) / (dtau_prime + dtau_dprime)
    sigma = 1.0 / math.sqrt(1.0 / dtau_prime + 1.0 / dtau_dprime)
    return math.exp(-(xk - mean) ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi) / sigma

pylab.title('Distribution on slice k', fontsize=18)
histo, bin_edges, dummy = pylab.hist(data_hist, bins=100, normed=True)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
pylab.plot(bin_centers, [pi_analytic(x, x_prime, x_dprime, dtau_prime, dtau_dprime) for x in bin_centers], 'r-', lw=3)
pylab.xlabel('$x_k$', fontsize=18)
pylab.ylabel('$\pi(x_k)$', fontsize=18)
pylab.savefig('plot-path_slice.png')
