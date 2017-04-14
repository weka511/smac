import random

t_max = 10000
for t in range(t_max):
    if random.randint(1, 6) == 1:
        print t, 'flip'
    else:
        print t