import random, math

for delta in [0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0]:
    x, y = 1.0, 1.0
    n_trials = 2**12
    n_hits = 0
    n_accepted = 0
    for i in range(n_trials):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
            n_accepted+=1
        if x**2 + y**2 < 1.0: n_hits += 1
      
    estimate=4.0 * n_hits / float(n_trials)
    error=abs(estimate-math.pi)
    acceptance_rate=n_accepted/ float(n_trials)
    print ('Delta={0:5.3f}, acceptance rate={1:5.3f}, error={2:5.3f}'.format(delta,acceptance_rate,error))