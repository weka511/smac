import random, math, pylab

alpha = 0.5
nsteps = 1000000
samples_x = []
samples_y = []
x, y = 0.0, 0.0
for step in range(nsteps):
    xnew = random.uniform(-1.0, 1.0)
    ynew = random.uniform(-1.0, 1.0)
    exp_new = - 0.5 * (xnew ** 2 + ynew ** 2) - alpha * (xnew ** 4 + ynew ** 4)
    exp_old = - 0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4)
    if random.uniform(0.0, 1.0) < math.exp(exp_new - exp_old):
        x = xnew
        y = ynew
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A3_1')
pylab.savefig('plot_A3_1.png')
pylab.show()