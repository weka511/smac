import math, random

def levy_harmonic_1d(start, end, dtau):
    x = [start]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               end / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
                 1.0 / math.sqrt(Ups1)))
    x.append(end)
    return x

beta = 1.0
N = 20
dtau = beta / float(N)
[xstart, ystart, zstart] = [1.0, -2.0, 1.5]
[xend, yend, zend] = [-2.5, 0.0, -0.5]
x = levy_harmonic_1d(xstart, xend, dtau)
y = levy_harmonic_1d(ystart, yend, dtau)
z = levy_harmonic_1d(zstart, zend, dtau)
for i in range(N + 1):
    print ('slice %2i:  ' % i, x[i], y[i], z[i])
