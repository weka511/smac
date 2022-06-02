from random import uniform
from math   import pi, cos

a       = 0.6
b       = 1.0
n_hits  = 0
n_steps = 1000000

for n in range(n_steps):
    x_center = uniform(0.0, b * 0.5)
    phi = uniform(0.0, pi * 0.5)
    x_tip = x_center - a * 0.5 * cos(phi)
    if x_tip < 0.0: n_hits += 1

print (a * 2.0 * n_steps / float(n_hits) / b)
