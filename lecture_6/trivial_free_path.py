from math   import sqrt
from random import gauss

beta    = 1.0
N       = 8
sigma   = sqrt(beta / N)
xend    = 1.0
Upsilon = [0.0]

for k in range(N):
    Upsilon.append(gauss(Upsilon[-1], sigma))
x = [0.0] + [Upsilon[k] + (xend - Upsilon[-1]) * k / float(N) for k in range(1, N + 1)]
print (x)
