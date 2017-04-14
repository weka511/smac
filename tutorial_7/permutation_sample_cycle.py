import random

N = 20
stats = [0] * (N + 1)
L = range(N)
nsteps = 1000000
for step in range(nsteps):
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)
    L[i], L[j] = L[j], L[i]
    if step % 100 == 0: 
        cycle_dict = {}
        for k in range(N):
            cycle_dict[k] = L[k]
        while cycle_dict != {}:
            starting_element = cycle_dict.keys()[0]
            cycle_length = 0
            old_element = starting_element
            while True:
                cycle_length += 1
                new_element = cycle_dict.pop(old_element)
                if new_element == starting_element: break
                else: old_element = new_element
            stats[cycle_length] += 1
for k in range(1, N + 1):
    print k, stats[k] 
