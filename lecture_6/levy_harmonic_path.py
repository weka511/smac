'''
Simple Lévy path
'''
from math   import sinh, sqrt, tanh
from random import gauss

beta         = 1.0
N            = 4
dtau         = beta / N
xstart, xend = 0.0, 1.0
x            = [xstart]

for k in range(1, N):
    dtau_prime = (N - k) * dtau
    Ups1 = 1.0 / tanh(dtau) +  1.0 / tanh(dtau_prime)
    Ups2 = x[k - 1] / sinh(dtau) +  xend / sinh(dtau_prime)
    x.append(gauss(Ups2 / Ups1, 1.0 / sqrt(Ups1)))

x.append(xend)
print (x)

