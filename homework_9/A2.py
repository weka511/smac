import math, random

def V(x, y):
    pot  = -4.0 * x ** 2 - x ** 3 + 4.0 * x ** 4
    pot += -4.0 * y ** 2 - y ** 3 + 4.0 * y ** 4
    return pot

gamma = 0.6
while gamma > 0.00125:
    xmin, ymin = 0.807044513157, 0.807044513157
    
    n_runs = 10
    n_success = 0
    
    # n_runs independent minimization runs are performed, and for each one 
    # there is a check of whether the global minimum was found
    # (this is encoded in the n_success counter),
    for run in range(n_runs):
        T = 4.0
        x, y = 0.0, 0.0
        delta = 0.1
        step = 0
        acc = 0
        while T > 0.00001: # run is stopped when a certain final temperature is reached
            step += 1
            # the program includes an annealing schedule, in which the
            # temperature is reduced every 100 iterations        
            if step == 100:
                T *= (1.0 - gamma)
                # an automatic step-size control is implemented, to keep the 
                # acceptance ratio in the range [0.3,0.7]
                if acc < 30:
                    delta /= 1.2
                elif acc > 70:
                    delta *= 1.2
                step = 0
                acc = 0
            xnew = x + random.uniform(-delta, delta)
            ynew = y + random.uniform(-delta, delta)
            if abs(xnew) < 1.0 and abs(ynew) < 1.0 and \
               random.uniform(0.0, 1.0) < math.exp(- (V(xnew, ynew) - V(x, y)) / T):
                x = xnew
                y = ynew
                acc += 1
        if math.sqrt((x - xmin) ** 2 + (y - ymin) ** 2) < 0.1:
            n_success += 1
    print ('gamma={0}, success ratio={1}'.format(gamma, n_success / float(n_runs)))
    gamma/=2