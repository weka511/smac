import random

# Select one position in L, then take a single step.
# If new position invalid, stay put

def markov_step_box(sigma,delta):
    a = random.choice(L)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
    if not (box_cond or min_dist < 4.0 * sigma ** 2):
        a[:] = b

L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

def markov_run(n_steps):
    configurations = [conf_a, conf_b, conf_c]
    hits = {conf_a: 0, conf_b: 0, conf_c: 0}
    for steps in range(n_steps):
        markov_step_box(sigma,delta)
        for conf in configurations:
            condition_hit = True
            for b in conf:
                condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in L) < del_xy
                condition_hit *= condition_b
            if condition_hit:
                hits[conf] += 1
    return (configurations,hits)

sigma = 0.15
sigma_sq = sigma ** 2
delta = 0.1
del_xy = 0.05

conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))  

for n_steps in [10000,100000,1000000,10000000]:
    configurations,hits=markov_run(n_steps)   
    total_hits=sum(hits[conf] for conf in configurations)
    print (n_steps,\
           (max(hits[conf] for conf in configurations)-\
            min(hits[conf] for conf in configurations))/total_hits)
    for conf in configurations:
        print (conf, hits[conf],hits[conf]/total_hits)
