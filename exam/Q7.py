import random,matplotlib.pyplot as plt

L = 4
b = -0.5
x = 0
nsteps = 10000
xs = []
for step in range(nsteps):
    if random.uniform(0.0, 1.0) < 0.5 + b:
        dx = 1
    else:
        dx = -1
    if x + dx >= 0 and x + dx < L:
        x += dx
    xs.append(x)
   
plt.hist(xs)