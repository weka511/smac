import random, math, pylab

x = 0.2
delta = 0.5
data = []
y_max = 0
n_trials = 10000
for k in xrange(n_trials):
    x_new = x + random.uniform(-delta, delta)
    if x_new > 0.0 and x_new < 1.0:
        if random.uniform(0.0, 1.0) < math.sqrt(x) / math.sqrt(x_new): 
            x = x_new 
    if 1.0 / math.sqrt(x) > y_max: 
         y_max =  1.0 / math.sqrt(x)
         print y_max, x, k
    data.append(x)

pylab.hist(data, bins=100, normed='True')
pylab.xlabel('$x$', fontsize=16)
pylab.ylabel('$\pi(x)$', fontsize=16)
x = [a / 100.0 for a in xrange(1, 101)]
y = [0.5 / math.sqrt(a) for a in x]
pylab.plot(x, y, linewidth=1.5, color='r')
pylab.title('Theoretical distribution $\pi(x)={1}/{(2 \sqrt{x})}$ and normalized\
    \n histogram for '+str(len(data))+' samples',fontsize=16)
pylab.show()
