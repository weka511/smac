import random, math

def unit_sphere():
    x = [random.gauss(0.0, 1.0) for i in range(3)]
    norm =  math.sqrt(sum(xk ** 2 for xk in x))
    return [xk / norm for xk in x]

N = 13
positions = [unit_sphere() for j in range(N)]
dists = [math.sqrt(sum((positions[k][j] - positions[l][j]) ** 2 \
         for j in range(3))) for l in range(N) for k in range(l)]
rmax = min(dists) / 2.0
R = 1.0 / (1.0 / rmax - 1.0)
print 'r = %f, R = %f' % (rmax, R)


import pylab, numpy, mpl_toolkits.mplot3d

def draw_sphere(center, rad, col, ax, resolution):
    delta = numpy.pi / float(resolution)
    u, v = numpy.mgrid[0:2 * numpy.pi + delta:delta, 0:numpy.pi + delta * 0.5:delta * 0.5]
    x = center[0] + rad * numpy.cos(u) * numpy.sin(v)
    y = center[1] + rad * numpy.sin(u) * numpy.sin(v)
    z = center[2] + rad * numpy.cos(v)
    ax.plot_wireframe(x, y, z, color=col)

fig = pylab.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
ax.set_axis_off()
draw_sphere([0.0, 0.0, 0.0], 1.0, 'r', ax, 40)
centers = [[(1.0 + R) * pos[j] for j in range(3)] for pos in positions]
for center in centers:
    draw_sphere(center, R, 'b', ax, 10)
ax.set_xlim(-1.0 - 2.0 * R, 1.0 + 2.0 * R)
ax.set_ylim(-1.0 - 2.0 * R, 1.0 + 2.0 * R)
ax.set_zlim(-1.0 - 2.0 * R, 1.0 + 2.0 * R)
pylab.show()
