'''
Construct path using a simple random walk (endpoint is not held fixed)
'''
from math   import sqrt
from random import gauss

beta  = 4.0
N     = 8
sigma = sqrt(beta / N)
x     = [0.0]

for k in range(N - 1):
    x.append(gauss(x[-1], sigma))
print (x)
