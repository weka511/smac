import random

gamma = -0.8
n_steps = 10000000
tot = 0.0
running = []
for step in range(n_steps):
    tot += random.uniform(0.0, 1.0) ** gamma
    av = tot / float(step + 1)
    running.append(av)
