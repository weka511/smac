import math, random

def energy(sigma, h, J):
    E = - h * sigma[0] - h * sigma[1] - J * sigma[0] * sigma[1]
    return E

beta = 1.0
h = 1.0
J = 1.0
nsteps = 10000
sigma = [1, 1]
for step in range(nsteps):
    site = random.choice([0, 1])
    sigma_new = sigma[:]
    sigma_new[site] *= (-1)
    delta_E = energy(sigma_new, h, J) - energy(sigma, h, J)
    if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
        sigma = sigma_new[:]
