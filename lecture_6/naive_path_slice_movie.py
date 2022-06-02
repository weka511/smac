from math   import exp, pi, sqrt
from pylab  import hist, legend, plot, savefig, show, title, xlabel, xlim, ylabel
from random import random, uniform

def rho_free(x, y, beta):
    return exp(-(x - y) ** 2 / (2.0 * beta))

def pi_analytic(xk, x_prime, x_dprime, dtau_prime, dtau_dprime):
    mean  = (dtau_dprime * x_prime + dtau_prime * x_dprime) / (dtau_prime + dtau_dprime)
    sigma = 1.0 / sqrt(1.0 / dtau_prime + 1.0 / dtau_dprime)
    return exp(-(xk - mean) ** 2 / (2.0 * sigma ** 2)) / sqrt(2.0 * pi) / sigma

dtau_prime  = 0.1
dtau_dprime = 0.2
x_prime     = 0.0
x_dprime    = 1.0
delta       = 1.0                 # maximum displacement of xk
n_steps     = 100000            # number of Monte Carlo steps
data_hist   = []
xk          = 0.0                    # initial value of xk

for step in range(n_steps):
    xk_new      = xk + uniform(-delta, delta)
    old_weight  = (rho_free(x_dprime, xk, dtau_dprime) * rho_free(xk, x_prime, dtau_prime))
    new_weight  = (rho_free(x_dprime, xk_new, dtau_dprime) * rho_free(xk_new, x_prime, dtau_prime))
    if random() < new_weight / old_weight:
        xk = xk_new
    data_hist.append(xk)

title('Distribution on slice k', fontsize=18)
histo, bin_edges, dummy = hist(data_hist, bins=100, density=True)
bin_centers             = 0.5 * (bin_edges[1:] + bin_edges[:-1])
plot(bin_centers, [pi_analytic(x, x_prime, x_dprime, dtau_prime, dtau_dprime) for x in bin_centers], 'r-', lw=3)
xlabel('$x_k$', fontsize=18)
ylabel('$\pi(x_k)$', fontsize=18)
savefig('plot-path_slice.png')
show()
