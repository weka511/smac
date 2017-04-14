import random, math, pylab

alpha = 0.5
nsteps = 1000000
samples_x = []
samples_y = []
x, y = 0.0, 0.0
for step in range(nsteps):
    if step % 2 == 0:
        while True:
            x = random.uniform(-1.0, 1.0)
            p = math.exp(-0.5 * x ** 2 - alpha * x ** 4 )
            if random.uniform(0.0, 1.0) < p:
                break
    else:
        while True:
            y = random.uniform(-1.0, 1.0)
            p = math.exp(-0.5 * y ** 2 - alpha * y ** 4 )
            if random.uniform(0.0, 1.0) < p:
                break
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A2_1')
pylab.savefig('plot_A2_1.png')
pylab.show()