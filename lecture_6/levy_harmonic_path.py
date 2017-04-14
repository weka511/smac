import math, random

beta = 1.0
N = 4
dtau = beta / N
xstart, xend = 0.0, 1.0
x = [xstart]
for k in range(1, N):
    dtau_prime = (N - k) * dtau
    Ups1 = 1.0 / math.tanh(dtau) + \
           1.0 / math.tanh(dtau_prime)
    Ups2 = x[k - 1] / math.sinh(dtau) + \
           xend / math.sinh(dtau_prime)
    x.append(random.gauss(Ups2 / Ups1, \
             1.0 / math.sqrt(Ups1)))
x.append(xend)
print (x)

