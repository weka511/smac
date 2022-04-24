'''
Generate a random walk, then pull back as described in Lecture 6, 20:12.
Compare result with Lévy free
'''
from math              import sqrt
from matplotlib.pyplot import figure, legend, plot, savefig, show
from random            import gauss, seed

beta         = 1.0
N            = 32
sigma        = sqrt(beta / N)
dtau         = beta / N
xstart, xend = 0.0, 1.0          # initial and final points
Upsilon      = [0.0]
seed_value   = 42

seed(seed_value)

def pull_back(k):
    return Upsilon[k] + (xend - Upsilon[-1]) * k / float(N)

for k in range(N):
    Upsilon.append(gauss(Upsilon[-1], sigma))

x =  [pull_back(k) for k in range(0, N + 1)]

figure(figsize=(12,12))
plot (Upsilon, label='Random Walk')
plot( x, label = f'Pulled back to xend={xend}, len={len(x)}')


seed(seed_value)

x_levy_free = [xstart]
for k in range(1, N):        # loop over internal slices
    dtau_prime = (N - k) * dtau
    x_mean     = (dtau_prime * x[k - 1] + dtau * xend) / (dtau + dtau_prime)
    sigma      = sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
    x_levy_free.append(gauss(x_mean, sigma))
x_levy_free.append(xend)
plot( x_levy_free, label = r'$L\acute{e}vy$')
legend()
savefig('trivial_free_path')
show()
