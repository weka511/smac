import random, math

h = 1.0
beta = 2.0
p = math.exp(- 2.0 * beta * h)
sigma = 1
tmax = 10000000
M_tot = 0
for t in range(tmax):
    if sigma == -1:
        sigma = 1
    elif random.uniform(0.0, 1.0) < p:
        sigma = -1
    M_tot += sigma
print 'magnetization:', M_tot / float(tmax)
print 'exact result: ', math.tanh(beta * h)