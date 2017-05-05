import math, random, pylab

def pi_x(x, beta):
    sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return math.exp(-x ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi) / sigma

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
x0s = []
x1s = []

high = low[:]
data = []
for step in range(nsteps):
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    x0s.append(low[0])
    x1s.append(low[1])

#xs = [0.1 * a for a in range(-30,31)]
#ys = [nsteps*pi_x(x,beta) for x in xs]

_, xs, _ =  pylab.hist([x0s,x1s],label=['0','1'],bins=25)
print (xs)
ys = [nsteps*pi_x(x,beta)/3 for x in xs]  # 3?

pylab.plot(xs,ys,label='pi_x')
pylab.xlabel('position')
pylab.ylabel('count')
pylab.legend()
pylab.title('A1')
