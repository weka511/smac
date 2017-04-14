import random, math, pylab

# exact distrubution:
list_x = [i * 0.1 for i in range(-40, 40)]
list_y = [math.exp(- x ** 2 / 2.0) / (math.sqrt(2.0 * math.pi)) for x in list_x]
pylab.plot(list_x, list_y, color='k', label='exact')
# sampled distributions:
nsamples = 2000000
for K in [1, 2, 6]: 
    print ('K = %i' % K)
    sigma = math.sqrt(K / 12.0)
    data = []
    for sample in xrange(nsamples):
        data += [sum(random.uniform(-0.5, 0.5) for k in xrange(K)) / sigma]
    pylab.hist(data, bins=200, normed=True, histtype='step', label='sampled (K=%i)' % K)
pylab.legend()
pylab.title('Sampling of the gaussian distribution\n(naive_gauss_movie.py)')
pylab.xlabel('$x$', fontsize=14)
pylab.ylabel('$\pi(x)$', fontsize=14)
pylab.savefig('plot-naive_gauss.png')
