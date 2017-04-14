import pylab

def binomialCoeff(n, k):
    result = 1
    for i in range(1, k+1):
        result = result * (n-i+1) / i
    return result

def Z(N, L, sigma):
    freespace = L - 2.0 * N * sigma
    if freespace > 0.0:
        result = freespace ** N
    else:
        result = 0.0
    return result

def pi(x, N, L, sigma):
    tot = 0.
    for k in range(0, N):
        Z1 = Z(k, x - sigma, sigma)
        Z2 = Z(N - k - 1, L - x - sigma, sigma)
        tot += binomialCoeff( N - 1, k) * Z1 * Z2
    Ztotal = Z(N, L, sigma)
    return tot / Ztotal

L = 20.0
N = 10
sigma = 0.75
xr = pylab.linspace(0.0, L, 201)
yr = [pi(x, N, L, sigma) for x in xr]
pylab.plot(xr, yr, 'red', linewidth=2.0)
pylab.xlabel('$x$', fontsize=14)
pylab.ylabel('$\pi(x)$', fontsize=14)
pylab.title('Exact density of %i clothes-pins ($\sigma$=%s)\non a line of length L=%s' % (N, sigma, L))
pylab.savefig('plot-direct_pins_density.png')
pylab.show()
