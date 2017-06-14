import random, math


def unit_sphere():
    'Return the coordintes of a random point on a unit sphere'
    x = [random.gauss(0.0, 1.0) for i in range(3)]
    norm =  math.sqrt(sum(xk ** 2 for xk in x))
    return [xk / norm for xk in x]

def minimum_distance(positions, N):
    dists = [math.sqrt(sum((positions[k][j] - positions[l][j]) ** 2 \
             for j in range(3))) for l in range(N) for k in range(l)]
    return min(dists)


def resize_disks(positions, r, N, gamma):
    '''
    The annealing schedule consists in increasing the disk radius
    (which corresponds to decreasing the temperature). The parameter gamma
    constitutes an annealing rate (gamma=1 gives a fast annealing,
    while a small gamma makes the annealing slower).'''
    Upsilon = minimum_distance(positions, N) / 2.0
    r = r + gamma * (Upsilon - r)
    return r

N = 19
gamma  = 0.375 #0.5 0.25
min_density = 0.78
#     Several independent runs are performed, and each time one solution is found.

for run in range(250):
    sigma  = 0.25
    r = 0.0
    positions = [unit_sphere() for j in range(N)]
    n_acc = 0
    step = 0
    while sigma > 1.e-8:
        step += 1
        if step % 500000 == 0:
            eta = N / 2.0 * (1.0 - math.sqrt(1.0 - r ** 2)) #surface area of the spherical caps formed by the disks.
            print ('{0} {1} {2} {3}'.format( r, eta, sigma, acc_rate))
        k = random.randint(0, N - 1)
        newpos = [positions[k][j] + random.gauss(0, sigma) for j in range(3)]
        norm = math.sqrt(sum(xk ** 2 for xk in newpos))
        newpos = [xk / norm for xk in newpos]
        new_min_dist = min([math.sqrt(sum((positions[l][j] - newpos[j]) ** 2 \
                       for j in range(3))) for l in list(range(k)) + list(range(k + 1, N))])
        if new_min_dist > 2.0 * r:
            positions = positions[:k] + [newpos] + positions[k + 1:]
            n_acc += 1
        if step % 100 == 0:
            acc_rate = n_acc / float(100)
            n_acc = 0
            #  Automatic step-size control is used (by changing sigma
            #  to keep the acceptance ratio in a reasonable interval.
            if acc_rate < 0.2:
                sigma *= 0.5
            elif acc_rate > 0.8 and sigma < 0.5:
                sigma *= 2.0
            r = resize_disks(positions, r, N, gamma)
            # The relation between outer-sphere radius R and disk
            # radius r reads R = 1 / (1 / r -1).
            R = 1.0 / (1.0 / r - 1.0)
            eta = 1.0 * N / 2.0 * (1.0 - math.sqrt(1.0 - r ** 2))
    print ('Run {0}. final density: {1} (gamma = {2})'.format(run+1,eta, gamma))
    
    # For each run, the final configuration is written on a file. 
    # This is done only for configurations that are above a given density
    # min_density (to avoid storing configurations which are clearly not optimal).
    if eta > min_density:
        f = open('N_{0}_eta_{1}_gamma_{2}.dat'.format(N,eta,gamma), 'w')
        for a in positions:
            f.write(str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[2]) + '\n')
        f.close()