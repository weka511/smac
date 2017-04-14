import random, math

nsamples = 50
for sample in range(nsamples):
    x, y, z = (random.gauss(0.0, 1.0), 
               random.gauss(0.0, 1.0), 
               random.gauss(0.0, 1.0))
    radius = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    print (x / radius, y / radius, z / radius)
