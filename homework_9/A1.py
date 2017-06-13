import random, math

def prob(x):
    s1 = math.exp(-(x + 1.2) ** 2 / 0.72)
    s2 = math.exp(-(x - 1.5) ** 2 / 0.08)
    return (s1 + 2.0 * s2) / math.sqrt(2.0 * math.pi)

delta = 10.0
nsteps = 10000
acc_tot = 0
x = 0.0
x_av = 0.0
for step in range(nsteps):
    xnew = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < prob(xnew) / prob(x):
        x = xnew
        acc_tot += 1
    x_av += x

print ('global acceptance ratio: {0}'.format(acc_tot / float(nsteps)))
print ('<x> = {0}'.format(x_av / float(nsteps)))