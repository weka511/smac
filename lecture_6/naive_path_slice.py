from numpy             import exp, linspace, sqrt
from matplotlib.pyplot import figure, hist, legend, plot, show
from random            import random, uniform
from scipy.stats       import norm

def rho_free(x, y, beta):
    return exp(-(x - y) ** 2 / (2.0 * beta))

dtau_prime  = 0.1
dtau_dprime = 0.2
x_prime     = 0.0
x_dprime    = 1.0
delta       = 1.0
n_steps     = 100000
xk          = 0.0
Xs          = []

for step in range(n_steps):
    xk_new      = xk + uniform(-delta, delta)
    old_weight  = (rho_free(x_dprime, xk, dtau_dprime) *  rho_free(xk, x_prime, dtau_prime))
    new_weight  = (rho_free(x_dprime, xk_new, dtau_dprime) * rho_free(xk_new, x_prime, dtau_prime))
    if random() < new_weight / old_weight:
        xk = xk_new
    Xs.append(xk)

mu    = (dtau_dprime*x_prime + dtau_prime*x_dprime)/(dtau_dprime + dtau_prime) #mean(Xs)
sigma = sqrt(1 / (1/dtau_prime+1/dtau_dprime))
dist  = norm(loc   = mu,
             scale = sigma)
xs    = linspace(min(Xs), max(Xs))

figure(figsize=(12,12))
hist(Xs, bins=25, density=True, label = f'$x_k$. n_steps={n_steps}')
plot(xs, dist.pdf(xs),label = fr'Gaussian $\mu=${mu:.2f}, $\sigma=${sigma:.2f}')
legend()
show()
