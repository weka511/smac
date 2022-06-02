'''Algorithm 6.1:  direct sampling for N pins'''
from random import uniform
from pylab import gca, Rectangle, axis, xlabel, title, savefig, show

N     = 15
L     = 10.0
sigma = 0.1
conf  = []

while len(conf) < N:
    conf.append(uniform(sigma, L - sigma))
    for k in range(len(conf) - 1):
        if abs(conf[-1] - conf[k]) < 2.0 * sigma:
            conf = []
            break

# begin of graphical output
bluesquare = Rectangle((sigma,0), L -2 * sigma, 0.33 * L, fc='b')
gca().add_patch(bluesquare)

for pin in conf:
    gca().add_patch(Rectangle((pin - 2 * sigma, 0), 4 * sigma, 0.33 * L, fc='w', ec='w'))
    gca().add_patch(Rectangle((pin - sigma, 0), 2 * sigma, 0.33 * L, fc='r'))


axis('scaled')
axis([0, L, 0, 0.33 * L])
xlabel('$x$', fontsize=14)
title('red: clothes pins; blue: remaining available space')
savefig('plot-direct_pins-configuration.png')
show()
