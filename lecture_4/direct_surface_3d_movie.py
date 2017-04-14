import random, math, pylab, mpl_toolkits.mplot3d

x_list, y_list, z_list = [],[],[]
nsamples = 1000
for sample in range(nsamples):
    x, y, z = random.gauss(0.0, 1.0), random.gauss(0.0, 1.0), random.gauss(0.0, 1.0)
    radius = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    x_list.append(x / radius)
    y_list.append(y / radius)
    z_list.append(z / radius)
# graphics output
fig = pylab.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
pylab.plot(x_list, y_list, z_list, '.')
pylab.title('Uniform sampling of the sphere surface')
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_zlabel('$z$', fontsize=14)
pylab.show()
