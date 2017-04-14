import random, math, pylab

x = 0.0
delta = 0.5
data = []
for k in range(50000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  \
         math.exp (- x_new ** 2 / 2.0) / math.exp (- x ** 2 / 2.0): 
        x = x_new 
    data.append(x)

pylab.hist(data, 100, normed = 'True')
x = [a / 10.0 for a in range(-50, 51)]
y = [math.exp(- a ** 2 / 2.0) / math.sqrt(2.0 * math.pi) for a in x]
pylab.plot(x, y, c='red', linewidth=2.0)
pylab.title('Theoretical Gaussian distribution $\pi(x)$ and \
    \nnormalized histogram for '+str(len(data))+' samples', fontsize = 18)
pylab.xlabel('$x$', fontsize = 30)
pylab.ylabel('$\pi(x)$', fontsize = 30)
pylab.savefig('plot_markov_gauss.png')
pylab.show()
