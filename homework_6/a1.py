'''
This program encompasses both version of the program from step A2.
Function mcmc carries out the Markov Chain Monte Carlo evolution,
and plot produces the graphs.
'''

import random, math, pylab

def gauss_cut(cut=1.0):
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= cut:
            return x
        
alpha = 0.5
nsamples = 1000000

def select(proposer=lambda: random.uniform(-1.0, 1.0),
           accepter=lambda x,y: math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4))):
    '''
    Perform direct sampling Monte Carlo evolution
    
    Arguments:
        proposer   Propose data to be used for the next step
        accepter   Decide whether to accept propsed value
    '''    
    samples_x = []
    samples_y = []
    for sample in range(nsamples):
        while True:
            x = proposer()
            y = proposer()
            p = accepter(x,y)
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
                              accepter=lambda x,y: math.exp(- alpha * (x ** 4 + y ** 4)))
plot('A1_2',samples_x, samples_y)

pylab.show()