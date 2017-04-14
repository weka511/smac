import random, math, pylab, mpl_toolkits.mplot3d

x_list, y_list, z_list = [],[],[]
nsamples = 200000
for sample in range(nsamples):
    x, y, z = random.gauss(0.0, 1.0), random.gauss(0.0, 1.0), random.gauss(0.0, 1.0)
    length = random.uniform(0.0, 1.0) ** (1.0 / 3.0) / math.sqrt(x ** 2 + y ** 2 + z ** 2)
    x, y, z = x * length, y * length, z * length
    if z < 0.075 and z > -0.075 or z > 0.85 or z < -0.85:
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
# graphics output
fig = pylab.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
pylab.title('Uniform sampling inside the sphere\n(only shown three intervals for z)')
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_zlabel('$z$', fontsize=14)
pylab.plot(x_list, y_list, z_list, '.')
pylab.show()
