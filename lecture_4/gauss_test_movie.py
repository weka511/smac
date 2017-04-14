import random, math, pylab

def gauss_test(sigma):
    phi = random.uniform(0.0, 2.0 * math.pi)
    Upsilon = random.uniform(0.0, 1.0)
    Psi = - math.log(Upsilon)
    r = sigma * math.sqrt(2.0 * Psi)
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return [x, y]

# exact distrubution:
list_x = [i * 0.1 for i in range(-40, 40)]
list_y = [math.exp(- x ** 2 / 2.0) / (math.sqrt(2.0 * math.pi)) for x in list_x]
# sampled distribution:
n_sampled_pairs = 5000000
data = []
for sample in range(n_sampled_pairs):
        data += gauss_test(1.0)
# graphics output
pylab.plot(list_x, list_y, color='k', label='exact')
pylab.hist(data, bins=150, normed=True, color='r', histtype='step', label='sampled')
pylab.legend()
pylab.title('Sampling of the gaussian distribution\n(gauss_test_movie.py)')
pylab.xlabel('$x$', fontsize=14)
pylab.ylabel('$\pi(x)$', fontsize=14)
pylab.savefig('plot-gauss_test.png')
