from numpy             import linspace
from matplotlib.pyplot import plot, xlabel, savefig, show, title, xlabel, ylabel

def binomialCoeff(n, k):
    result = 1
    for i in range(1, k+1):
        result *= (n-i+1) / i
    return result

def Z(N, L, sigma):
    freespace = L - 2.0 * N * sigma
    if freespace > 0.0:
        return freespace ** N
    else:
        return 0.0

def pi(x, N, L, sigma):
    return sum([binomialCoeff( N - 1, k) * Z(k, x - sigma, sigma) * Z(N - k - 1, L - x - sigma, sigma) for k in range(0, N)]) / Z(N, L, sigma)

L     = 20.0
N     = 10
sigma = 0.75

xr     = linspace(0.0, L, 201)
yr     = [pi(x, N, L, sigma) for x in xr]

plot(xr, yr, 'red', linewidth=2.0)
xlabel('$x$', fontsize=14)
ylabel('$\pi(x)$', fontsize=14)
title('Exact density of %i clothes-pins ($\sigma$=%s)\non a line of length L=%s' % (N, sigma, L))
savefig('plot-direct_pins_density.png')
show()
