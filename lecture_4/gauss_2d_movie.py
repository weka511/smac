import random, pylab

nsamples = 100000
x_list, y_list = [], []
for sample in range(nsamples):
    x_list.append(random.gauss(0.0, 1.0))
    y_list.append(random.gauss(0.0, 1.0))
# begin graphics output
pylab.plot(x_list, y_list, marker='.', linestyle='')
pylab.title('Samples from the 2D Gaussian distribution')
pylab.xlabel('$x$', fontsize=14)
pylab.ylabel('$y$', fontsize=14)
pylab.xlim(-4.0, 4.0)
pylab.ylim(-4.0, 4.0)
pylab.axes().set_aspect('equal') # set the aspect ratio of the plot
pylab.savefig('plot-gauss_2d.png')
