import random, math

K = 10  # for each sample, we sum up K independent random variables
sigma = math.sqrt(K / 12.0)
nsamples = 100
for sample in range(nsamples):
    print (sum(random.uniform(-0.5, 0.5) for i in range(K)) / sigma)
