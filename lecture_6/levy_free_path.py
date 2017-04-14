import math, random

beta = 1.0
N = 4
dtau = beta / N
nsteps = 10                      # number of paths to be generated
xstart, xend = 0.0, 1.0          # initial and final points
for step in range(nsteps):
    x = [xstart]
    for k in range(1, N):        # loop over internal slices
        dtau_prime = (N - k) * dtau
        x_mean = (dtau_prime * x[k - 1] + dtau * xend) / \
                 (dtau + dtau_prime)
        sigma = math.sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
        x.append(random.gauss(x_mean, sigma))
    x.append(xend)
    print (x)
