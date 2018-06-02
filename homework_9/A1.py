import random, math

def prob(x):
    s1 = math.exp(-(x + 1.2) ** 2 / 0.72)
    s2 = math.exp(-(x - 1.5) ** 2 / 0.08)
    return (s1 + 2.0 * s2) / math.sqrt(2.0 * math.pi)

delta = 0.001
nsteps = 10000
acc_tot = 0
x = 0.0
x_av = 0.0
acc_tmp = 0

for step in range(nsteps):
    xnew = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < prob(xnew) / prob(x):
        x = xnew
        acc_tot += 1
        acc_tmp+=1
    x_av += x
    if step%100 ==0:
        if acc_tmp>60:
            delta*=1.1
        if acc_tmp<40:
            delta/=1.1
        acc_tmp = 0
            
print ('nsteps={0:,d}, delta={1}, <x> = {2}, global acceptance ratio: {3}'.\
       format(nsteps, delta,x_av / float(nsteps),acc_tot / float(nsteps)))