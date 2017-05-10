import math, random, pylab

'''
Compute partition function for a particle with energy levels 0, 1, 2
'''

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
    if low[0]!=high[0] or low[1]!=high[1]: print (low,high)
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    x0s.append(low[0])
    x1s.append(low[1])

_,xs,_ =  pylab.hist([x0s,x1s],label=['Alice','Bob'],bins=50,normed=True)

ys = [pi_x(x,beta) for x in xs] 

pylab.plot(xs,ys,label='Theoretical')
pylab.xlabel('$x$')
pylab.ylabel('$Probability$')
pylab.legend()
pylab.title('$Two\ Distinguishable\ Quantum\ Particles:\ Alice\ &\ Bob$')
pylab.savefig('A1.png')