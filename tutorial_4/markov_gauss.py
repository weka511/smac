import random, math

x = 0.0
delta = 0.5
for k in range(100000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  \
         math.exp (- x_new ** 2 / 2.0) / math.exp (- x ** 2 / 2.0): 
        x = x_new 
    print x
