import math, random, pylab

'''
Compute partition function for a particle with energy levels 0, 1, 2

  Parameters:
     beta
'''
def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

def pi_two_bosons(x, beta):
    pi_x_1 = math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta / 2.0))
    pi_x_2 = math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta))
    weight_1 = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    weight_2 = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))
    return pi_x_1 * weight_1 + pi_x_2 * weight_2

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


def calculate_probabilities(beta = 2.0,nsteps = 5000): #00
    low = levy_harmonic_path(2)
    high = low[:]
    data = []
    
    x0s = []
    x1s = []
    
    N1 = 0
    N2 = 0
    same = False
    
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
            same = not same
            high[0], high[1] = high[1], high[0]
            
        x0s.append(high[0])
        x1s.append(high[1])
        
        if same:
            N1 += 1
        else:
            N2 += 1
            
    return (N1,N2)

betas = []
p1s   = []
p2s   = []
tp1s  = []
tp2s  = []

for i in range(50):
    beta = 0.1*(i+1)
    n1,n2=  calculate_probabilities(beta)
    p1=n1/(n1+n2)
    p2=n2/(n1+n2)
    fract_two_cycles = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    fract_one_cycle = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))   
    #print (beta, p1,p2,fract_one_cycle,fract_two_cycles)
    betas.append(beta)
    p1s.append(p1)
    p2s.append(p2)
    tp1s.append(fract_one_cycle)
    tp2s.append(fract_two_cycles)

pylab.plot(betas,p1s,color='r',label='Probability one cycle')
pylab.plot(betas,p2s,color='g',label='Probability two cycles')
pylab.plot(betas,tp1s,color='b',label='Fract one cycle (theoretical)')
pylab.plot(betas,tp2s,color='m',label='Fract two cycles (theoretical)')

pylab.xlabel(r'$\beta$')
pylab.ylabel('$Probability$')
pylab.legend()
pylab.title('$Probability\ of\ one\ and\ two\ cycles$')
pylab.savefig('A2A.png')