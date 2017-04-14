import random, math

h = 1.0
beta = 2.0
log_lambda = math.log(1.0 - math.exp(- 2.0 * beta * h))
t_tot = 0
t_max = 100000000
M_tot = 0
while t_tot <= t_max:
    Upsilon = random.uniform(0.0, 1.0)
    delta_t = int(math.log(Upsilon) / log_lambda) + 1
    M_tot += (delta_t - 1)
    t_tot += (delta_t + 1)
print 'magnetization:', M_tot / float(t_tot)
print 'exact result: ', math.tanh(beta * h)