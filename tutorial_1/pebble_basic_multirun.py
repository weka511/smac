import random

neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]
t_max = 4
N_runs = 25600
for run in range(N_runs):
    site = 8
    t = 0
    while t < t_max: 
        t += 1
        site = neighbor[site][random.randint(0, 3)]
    print site
