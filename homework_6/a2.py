'''
Path sampling: A firework of algorithms

This program encompasses both version of the program from step A2.
Function mcmc carries out the Markov Chain Monte Carlo evolution,
and plot produces the graphs.
'''

import random, math, pylab

alpha = 0.5
nsteps = 1000000

def gauss_cut(cut=1.0):
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= cut:
            return x
        
def evolve(proposer=lambda: random.uniform(-1.0, 1.0),
       accepter=lambda u:math.exp(-0.5 * u ** 2 - alpha * u ** 4 )):
    '''
    Perform Markov Chain Monte Carlo evolution
    
    Arguments:
        proposer   Function which proposes data to be used for the next step
        accepter   Function which decides whether to accept proposed value
    '''
    samples_x = []
    samples_y = []
    x, y = 0.0, 0.0
    for step in range(nsteps):
        if step % 2 == 0:
            while True:
                x = proposer()
                p = accepter(x)
                if random.uniform(0.0, 1.0) < p:
                    break
        else:
            while True:
                y = proposer()
                p = accepter(y)
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
(samples_x, samples_y)=evolve()
plot('A2_1',samples_x, samples_y)

# Evolve and plot with gauss_cut

pylab.figure(2) 
(samples_x, samples_y)=evolve(proposer=gauss_cut, 
                          accepter=lambda u:math.exp(- alpha * u ** 4 ))
plot('A2_2',samples_x, samples_y)

pylab.show()