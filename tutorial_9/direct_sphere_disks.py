import random, math

def unit_sphere():
    x = [random.gauss(0.0, 1.0) for i in range(3)]
    norm =  math.sqrt(sum(xk ** 2 for xk in x))
    return [xk / norm for xk in x]

N = 13
r = 0.25
attempts = 0
while True:
    attempts += 1
    positions = [unit_sphere() for j in range(N)]
    dists = [math.sqrt(sum((positions[k][j] - positions[l][j]) ** 2 \
             for j in range(3))) for l in range(N) for k in range(l)]
    if min(dists) > 2.0 * r: break
print attempts, 'trials required'
