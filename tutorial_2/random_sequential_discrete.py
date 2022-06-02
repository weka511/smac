'''Create configuration of rods without tabula rasa: does not give equiprobable distribution'''
from random import randint

configurations = {(0, 3): 'a',
                  (0, 4): 'b',
                  (1, 4): 'c',
                  (3, 0): 'd',
                  (4, 0): 'e',
                  (4, 1): 'f'}

counts         = {'a': 0,
                  'b': 0,
                  'c': 0,
                  'd': 0,
                  'e': 0,
                  'f': 0}

n_runs         = 100000

for i in range(n_runs):
    red_rod = randint(0, 3)
    if red_rod >= 2: red_rod += 1
    while True:
        blue_rod = randint(0, 4)
        if abs(red_rod - blue_rod) > 2: break
    conf = configurations[(red_rod, blue_rod)]
    counts[conf] += 1

for conf in counts:
    print (conf, counts[conf] / float(n_runs))
