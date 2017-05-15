import math, random, pylab


def z(beta):
    '''
    Compute partition function for a particle with energy levels 0, 1, 2
    
      Parameters:
         beta
    '''    
    return 1.0 / (1.0 - math.exp(- beta))

def pi_two_bosons(x, beta):
    '''
    '''
    def pi(beta):
        return math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
               math.exp(-x ** 2 * math.tanh(beta))
    def weight(beta):
        return z(beta) ** 2 
    return (pi(beta/2) * weight(beta) + pi(beta) * weight(2*beta))/\
           (z(beta) ** 2 + z(2.0 * beta))

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)

beta = 2.0
nsteps = 500000
low = levy_harmonic_path(2)
high = low[:]
data = []

x0s = []
x1s = []

for step in range(nsteps):
    # move 1
    if low[0] == high[0]:
        k = random.choice([0, 1])
        low[k] = levy_harmonic_path(1)[0]
        high[k] = low[k]
    else:
        low[0], low[1] = levy_harmonic_path(2)
        high[1] = low[0]
        high[0] = low[1]
    data += low[:]
    # move 2
    weight_old = (rho_harm_1d(low[0], high[0], beta) *
                  rho_harm_1d(low[1], high[1], beta))
    weight_new = (rho_harm_1d(low[0], high[1], beta) *
                  rho_harm_1d(low[1], high[0], beta))
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        high[0], high[1] = high[1], high[0]
        
    x0s.append(high[0])
    x1s.append(high[1])

_,xs,_ =  pylab.hist([x0s,x1s],label=['Higgs','Ziggs'],bins=50,normed=True)

ys = [pi_two_bosons(x,beta) for x in xs] 

pylab.plot(xs,ys,label='Theoretical')
pylab.xlabel('$x$')
pylab.ylabel('$Probability$')
pylab.legend()
pylab.title('$Two\ Bosons: Higgs\ &\ Ziggs$')
pylab.savefig('A2.png')