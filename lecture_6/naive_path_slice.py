import math, random

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

dtau_prime  = 0.1
dtau_dprime = 0.2
x_prime  = 0.0
x_dprime = 1.0
delta = 1.0
n_steps = 100
xk = 0.0
for step in range(n_steps):
    xk_new = xk + random.uniform(-delta, delta)
    old_weight  = (rho_free(x_dprime, xk, dtau_dprime) *
                   rho_free(xk, x_prime, dtau_prime))
    new_weight  = (rho_free(x_dprime, xk_new, dtau_dprime) * 
                   rho_free(xk_new, x_prime, dtau_prime))
    if random.random() < new_weight / old_weight:
        xk = xk_new
    print (xk)
