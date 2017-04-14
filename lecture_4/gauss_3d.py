import random, math

nsamples = 100
for sample in range(nsamples):
    x, y, z = (random.gauss(0.0, 1.0),
               random.gauss(0.0, 1.0),
               random.gauss(0.0, 1.0))
    print (x, y, z)
