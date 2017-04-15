import random, math, pylab

def gauss_cut(cut=1.0):
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= cut:
            return x
        
alpha = 0.5
nsamples = 1000000

def select(proposer=lambda: random.uniform(-1.0, 1.0),
       accepter=lambda u:math.exp(-0.5 * u ** 2 - alpha * u ** 4 )):
    samples_x = []
    samples_y = []
    for sample in range(nsamples):
        while True:
            x = gauss_cut()
            y = gauss_cut()
            p = math.exp( - alpha * (x ** 4 + y ** 4))
            if random.uniform(0.0, 1.0) < p:
                break
        samples_x.append(x)
        samples_y.append(y)
    return (samples_x, samples_y)

def plot(name,samples_x, samples_y):
    pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
    pylab.axis([-1.0, 1.0, -1.0, 1.0])
    cb = pylab.colorbar()
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.title(name)
    pylab.savefig('{0}.png'.format(name))

    
# Evolve and plot with uniform distribution

pylab.figure(1)    
(samples_x, samples_y)=select()
plot('A1_1',samples_x, samples_y)

# Evolve and plot with gauss_cut

pylab.figure(2) 
(samples_x, samples_y)=select(proposer=gauss_cut, 
                          accepter=lambda u:math.exp(- alpha * u ** 4 ))
plot('A1_2',samples_x, samples_y)

pylab.show()