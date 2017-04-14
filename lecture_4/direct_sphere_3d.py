import random, math

nsamples = 100
for sample in range(nsamples):
    x, y, z = (random.gauss(0.0, 1.0), 
               random.gauss(0.0, 1.0), 
               random.gauss(0.0, 1.0))
    length = random.uniform(0.0, 1.0) ** (1.0 / 3.0) \
                    / math.sqrt(x ** 2 + y ** 2 + z ** 2) 
    print ( x *length, y * length, z * length)
