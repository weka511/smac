import math, random

beta = 4.0
N = 8
sigma = math.sqrt(beta / N)
x = [0.0]
for k in range(N - 1):
    x.append(random.gauss(x[-1], sigma))
print (x)
