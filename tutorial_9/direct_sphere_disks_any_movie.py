import random, math, mayavi.mlab

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

x, y, z = [[(1.0 + R) * pos[j] for pos in positions] + [0.0] for j in range(3)]
rad = [2.0 * R for pos in positions] + [2.0]
mayavi.mlab.figure(bgcolor=(0.9, 0.9, 1), size=(1000, 700))
mayavi.mlab.points3d(x, y, z, rad, scale_factor=1, resolution=100)
mayavi.mlab.show()

