import random, pylab

N = 15 
L = 10.0
sigma = 0.1
conf = []
while len(conf) < N:
    conf.append(random.uniform(sigma, L - sigma))
    for k in range(len(conf) - 1):
        if abs(conf[-1] - conf[k]) < 2.0 * sigma:
            conf = []
            break

# begin of graphical output
bluesquare = pylab.Rectangle((sigma,0), L -2 * sigma, 0.33 * L, fc='b')
pylab.gca().add_patch(bluesquare)
for pin in conf:
    whiterec = pylab.Rectangle((pin - 2 * sigma, 0), 4 * sigma, 0.33 * L, fc='w', ec='w')
    pylab.gca().add_patch(whiterec)
for pin in conf:
    redrec = pylab.Rectangle((pin - sigma, 0), 2 * sigma, 0.33 * L, fc='r')
    pylab.gca().add_patch(redrec)
pylab.axis('scaled')
pylab.axis('scaled')
pylab.axis([0, L, 0, 0.33 * L])
pylab.xlabel('$x$', fontsize=14)
pylab.title('red: clothes pins; blue: remaining available space')
pylab.savefig('plot-direct_pins-configuration.png')
pylab.show()
