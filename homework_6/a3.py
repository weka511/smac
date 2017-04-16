'''
Peer-graded Assignment: Path sampling: A firework of algorithms
'''

import random, math, pylab

def gauss_cut(cut=1.0):
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= cut:
            return x
        
alpha = 0.5
nsteps = 1000000

def evolve(proposer=lambda: random.uniform(-1.0, 1.0),
          accepter=lambda x,y: math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4))):
    samples_x = []
    samples_y = []
    x, y = 0.0, 0.0
    for step in range(nsteps):
        xnew = proposer()
        ynew = proposer()
        exp_new = accepter(xnew,ynew)
        exp_old = accepter(x,y)
        if random.uniform(0.0, 1.0) < math.exp(exp_new - exp_old):
            x = xnew
            y = ynew
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
(samples_x, samples_y)=evolve()
plot('A3_1',samples_x, samples_y)

# Evolve and plot with gauss_cut

pylab.figure(2) 
(samples_x, samples_y)=evolve(proposer=gauss_cut, 
                              accepter=lambda x,y: math.exp(- alpha * (x ** 4 + y ** 4)))
plot('A3_2',samples_x, samples_y)
    
pylab.show()