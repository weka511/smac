import random, math, pylab

y_max = 100.0
x_cut = 1.0
n_data = 10000
data = []
n_accept = 0
while n_accept < n_data: 
    y = random.uniform(0.0, y_max)
    x = random.uniform(0.0, x_cut)
    if y < 1.0 / (2.0 * math.sqrt(x)):
        n_accept += 1
        data.append(x)

pylab.hist(data, bins=100, normed='True')
x = [a / 100.0 for a in xrange(1, 100)]
y = [1.0 / (2.0 * math.sqrt(a)) for a in x]
pylab.plot(x, y, 'red', linewidth = 2)
pylab.title('Theoretical distribution $\pi(x)={1}/{(2 \sqrt{x})}$ and normalized\
    \n histogram for '+str(n_accept)+' accepted samples',fontsize=16)
pylab.xlabel('$x$', fontsize=18)
pylab.ylabel('$\pi(x)$', fontsize=18)
pylab.show()
