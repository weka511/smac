import random, math, pylab, mpl_toolkits.mplot3d

x_list, y_list, z_list = [], [], []
nsamples = 1000
for sample in range(nsamples):
    x_list.append(random.gauss(0.0, 1.0))
    y_list.append(random.gauss(0.0, 1.0))
    z_list.append(random.gauss(0.0, 1.0))
# begin graphics output
fig = pylab.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal') # set the aspect ratio of the plot
pylab.plot(x_list, y_list, z_list, '.')
pylab.title('Samples from the 3D gaussian distribution')
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_zlabel('$z$', fontsize=14)
pylab.show()
