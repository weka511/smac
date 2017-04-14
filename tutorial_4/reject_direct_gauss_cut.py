import random, math

y_max = 1.0 / math.sqrt(2.0 * math.pi)
x_cut = 5.0
n_data = 1000
n_accept = 0
while n_accept < n_data:
    y = random.uniform(0.0, y_max)
    x = random.uniform(-x_cut, x_cut)
    if y < math.exp( - x **2 / 2.0)/math.sqrt(2.0 * math.pi): 
        n_accept += 1
        print x
