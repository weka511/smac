import random, math

for delta in [0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0]:
    x, y = 0.0, 0.0
    n_trials = 2**30
    n_hits = 0
    n_accepted = 0
    for i in range(n_trials):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if (x + del_x)*(x + del_x) + (y + del_y)*(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
            n_accepted+=1
        z = random.uniform(-1.0, 1.0)

        if x**2 + y**2 +z**2< 1.0:
            n_hits += 1
      
    print ('Delta={0:.3f}, acceptance={1:.2f}, <Q_3>={2:.6f}, diff={3:.2g}'.\
           format(delta, n_accepted/n_trials, 2*n_hits/n_trials ,abs(2*n_hits/n_trials- 4/3)))