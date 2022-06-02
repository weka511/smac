'''
Generate a random walk, then pull back as described in Lecture 6, 20:12.
Compare result with Lévy free path
'''
from math              import sqrt
from matplotlib.pyplot import figure, legend, plot, savefig, show
from random            import gauss, seed
from timeit            import time

beta         = 1.0
N            = 1024
sigma        = sqrt(beta / N)
dtau         = beta / N
xstart, xend = 0.0, 1.0          # initial and final points
seed_value   = 42                #Seed for random number generator, to ensure that random walk and
                                 #Lévy free path see the same sequence of random numbers

seed(seed_value)

def pull_back(k):
    '''Scale The Upsilons to get Lévy path'''
    return Upsilon[k] + (xend - Upsilon[-1]) * k / float(N)

# Random walk

Upsilon      = [0.0]
for k in range(N):
    Upsilon.append(gauss(Upsilon[-1], sigma))

# Pull back to get Lévy flight

x =  [pull_back(k) for k in range(0, N + 1)]

# Now calculate Lévy flight directly, resetting random number generator

seed(seed_value)

x_levy_free = [xstart]
for k in range(1, N):        # loop over internal slices
    dtau_prime = (N - k) * dtau
    x_mean     = (dtau_prime * x[k - 1] + dtau * xend) / (dtau + dtau_prime)
    sigma      = sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
    x_levy_free.append(gauss(x_mean, sigma))
x_levy_free.append(xend)

figure(figsize=(12,12))

plot (Upsilon,
      label = r'$\upsilon$ Random Walk',
      c     = 'xkcd:green')
plot( x,
      label     = f'Pulled back to xend={xend}, len={len(x)}',
      linestyle = (5, (5, 10)),
      c         = 'xkcd:red')
plot( x_levy_free,
      label     = r'$L\acute{e}vy$',
      linestyle = (0, (5, 10)),
      c         = 'xkcd:blue')

legend()
savefig('trivial_free_path')
show()
