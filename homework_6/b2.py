'''
Path sampling: A firework of algorithms

This program is tor step B1. I have restructured into separate functions
for the main steps.
'''

import math, random, pylab, time

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

start_time = time.time()

beta = 20.0
N = 80
dtau = beta / N
delta = 1.0
n_steps = 4000000

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x

def create_path():
    x = [5.0] * N
    data = []
    Ncut = N//2
    for step in range(n_steps):
        x=levy_harmonic_path(x[0], x[0], dtau, N)
        x = x[Ncut:] + x[:Ncut] 
        if step % N == 0:
            k = random.randint(0, N - 1)
            data.append(x[k])
    return (x,data)

def write_path(x):
    with open('plot_B1_beta%s.txt' % beta,'w') as f:
        for xx in x:
            f.write('{0}\n'.format(xx))
    
def plot_histogram(data,figure=1):
    pylab.figure(figure)
    pylab.hist(data, normed=True, bins=100, label='QMC')
    list_x = [0.1 * a for a in range (-30, 31)]
    list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
              math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
    pylab.plot(list_x, list_y, label='analytic')
    pylab.legend()
    pylab.xlabel('$x$')
    pylab.ylabel('$\\pi(x)$ (normalized)')
    pylab.title('Levy harmonic path (beta=%s, N=%i)' % (beta, N))
    pylab.xlim(-2, 2)
    pylab.savefig('plot_B2_beta%s.png' % beta)

def plot_path(x,figure=1):
    pylab.figure(figure)
    y=[i*beta/N for i in range(N)]
    pylab.plot(x,y)
    pylab.xlabel('$x$')
    pylab.ylabel('$Time=\\frac{i \\beta}{N}$')
    pylab.title('Levy harmonic path')
    pylab.savefig('plot_B1_path_beta%s.png' % beta)
    
x,data = create_path()
write_path(x)
plot_histogram(data)
plot_path(x,figure=2)

print('--- {0:.1f} minutes ---'.format((time.time() - start_time)/60))

pylab.show()