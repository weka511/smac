import random, math, mayavi.mlab

def unit_sphere():
    x = [random.gauss(0.0, 1.0) for i in range(3)]
    norm =  math.sqrt(sum(xk ** 2 for xk in x))
    return [xk / norm for xk in x]

def minimum_distance(positions, N):
    dists = [math.sqrt(sum((positions[k][j] - positions[l][j]) ** 2 \
            for j in range(3))) for l in range(N) for k in range(l)]
    return min(dists)

def resize_disks(positions, r, N, gamma):
    Upsilon = minimum_distance(positions, N) / 2.0
    r = r + gamma * (Upsilon - r)
    return r

N = 13
r = 0.2
nsteps = 1000000
sigma  = 0.25
gamma  = 0.05
while True: 
    positions = [unit_sphere() for j in range(N)] 
    if minimum_distance(positions, N) > 2.0 * r: break
n_acc = 0
for step in range(nsteps):
    k = random.randint(0, N - 1)
    newpos = [positions[k][j] + random.gauss(0, sigma) for j in range(3)]
    norm = math.sqrt(sum(xk ** 2 for xk in newpos))
    newpos = [xk / norm for xk in newpos]
    new_min_dist = min([math.sqrt(sum((positions[l][j] - newpos[j]) ** 2 \
                   for j in range(3))) for l in range(k) + range(k + 1, N)])
    if new_min_dist > 2.0 * r:
        positions = positions[:k] + [newpos] + positions[k+1:]
        n_acc += 1
    if step % 100 == 0:
        acc_rate = n_acc / float(100)
        n_acc = 0
        if acc_rate < 0.5:
            sigma *= 0.5
        r = resize_disks(positions, r, N, gamma)
        R = 1.0 / (1.0 / r - 1.0)
        density = 1.0 * N / 2.0 * (1.0 - math.sqrt(1.0 - r ** 2))
print
print 'Final r = %0.5f'%r + '  Final R = %0.5f'%R + '  Final density = %0.5f'%density

R = 1.0 / (1.0 / r - 1.0)
x, y, z = [[(1.0 + R) * pos[j] for pos in positions] + [0.0] for j in range(3)]
rad = [2.0 * R for pos in positions] + [2.0]
mayavi.mlab.figure(bgcolor=(0.9, 0.9, 1), size=(1000, 700))
mayavi.mlab.points3d(x, y, z, rad, scale_factor=1, resolution=100)
mayavi.mlab.show()
