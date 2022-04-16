from matplotlib.pyplot import hist, show
from numpy import arccos, dot, mean, sqrt, std, zeros
from numpy.linalg import norm
from numpy.random import normal

d     = 100
N     = 10000
x0    = zeros(d)
x0[0] = 1
sigma = 1/ sqrt(d)
X0    = []
Theta = []
for i in range(N):
    x = normal(scale=sigma,size=d)
    x = x/norm(x)
    projection = dot(x,x0)
    X0.append(projection)
    Theta.append(arccos(projection))

hist(X0)
hist(Theta)
show()
