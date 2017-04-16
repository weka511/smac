'''
Path sampling: A firework of algorithms

This program is tor step B1. I have restructured into spearate functions
for the main steps.
'''

import math, random, pylab

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

beta = 20.0
N = 80
dtau = beta / N
delta = 1.0
n_steps = 4000000

def create_path():
    x = [5.0] * N
    data = []
    for step in range(n_steps):
        k = random.randint(0, N - 1)
        knext, kprev = (k + 1) % N, (k - 1) % N
        x_new = x[k] + random.uniform(-delta, delta)
        old_weight  = (rho_free(x[knext], x[k], dtau) *
                       rho_free(x[k], x[kprev], dtau) *
                       math.exp(-0.5 * dtau * x[k] ** 2))
        new_weight  = (rho_free(x[knext], x_new, dtau) *
                       rho_free(x_new, x[kprev], dtau) *
                       math.exp(-0.5 * dtau * x_new ** 2))
        if random.uniform(0.0, 1.0) < new_weight / old_weight:
            x[k] = x_new
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
    pylab.title('naive_harmonic_path (beta=%s, N=%i)' % (beta, N))
    pylab.xlim(-2, 2)
    pylab.savefig('plot_B1_beta%s.png' % beta)

def plot_path(x,figure=1):
    pylab.figure(figure)
    y=[i*beta/N for i in range(N)]
    pylab.plot(x,y)
    pylab.xlabel('$x$')
    pylab.ylabel('$Time=\\frac{i \\beta}{N}$')
    pylab.title('Naive harmonic path')
    pylab.savefig('plot_B1_path_beta%s.png' % beta)
    
x,data = create_path()
write_path(x)
plot_histogram(data)
plot_path(x,figure=2)

pylab.show()