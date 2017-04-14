import random, math

def unit_sphere():
    x = [random.gauss(0.0, 1.0) for i in range(3)]
    norm =  math.sqrt(sum(xk ** 2 for xk in x))
    return [xk / norm for xk in x]

N = 13
r = 0.3
nsteps = 10000
sigma  = 0.4
while True: 
    positions = [unit_sphere() for j in range(N)] 
    dists = [math.sqrt(sum((positions[k][j] - positions[l][j]) ** 2 \
             for j in range(3))) for l in range(N) for k in range(l)]
    if min(dists) > 2.0 * r: break
n_acc = 0
for step in range(nsteps):
    k = random.randint(0, N - 1)
    newpos = [positions[k][j] + random.gauss(0.0, sigma) for j in range(3)]
    norm = math.sqrt(sum(xk ** 2 for xk in newpos))
    newpos = [xk / norm for xk in newpos]
    new_min_dist = min([math.sqrt(sum((positions[l][j] - newpos[j]) ** 2 \
                 for j in range(3))) for l in range(k) + range(k + 1, N)])
    if new_min_dist > 2.0 * r:
        positions = positions[:k] + [newpos] + positions[k + 1:]
        n_acc += 1
print 'acceptance rate:', n_acc / float(nsteps)
