'''
Path sampling: A firework of algorithms

This program is tor step C2.
'''

import math, random, pylab, time

cubic   = -1
quartic = 1
beta    = 20.0
N       = 100
dtau    = beta / N
delta   = 1.0
n_steps = 4000000

def V_harmonic(x, cubic, quartic):
    return x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

def V_anharm(x, cubic, quartic):
    return cubic * x ** 3 + quartic * x ** 4

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

def calculate_trotter_weight(x,V=lambda x: V_harmonic(x, cubic, quartic)):
    return math.exp(sum(-V(a) * dtau for a in x))



def levy_free_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        x_mean = (dtau_prime * x[k - 1] + dtau * xend) / \
                 (dtau + dtau_prime)
        sigma = math.sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
        x.append(random.gauss(x_mean, sigma))
    return x

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

def create_path(levy_path=lambda xstart, xend, dtau, N:levy_harmonic_path(xstart, xend, dtau, N)):
    x = [5.0] * N
    data = []
    Ncut = N//5  # for N=80 this gives an acceptance of 52%, close enough to 50%
    old_trotter_weight = calculate_trotter_weight(x)
    n_trials=0
    for step in range(n_steps):
        accepted=False
        while not accepted:
            x_new = levy_path(x[0], x[Ncut], dtau, Ncut) + x[Ncut:]
            new_trotter_weight = calculate_trotter_weight(x_new)
            accepted=old_trotter_weight==0 or random.random()<new_trotter_weight/old_trotter_weight
            n_trials+=1
        old_trotter_weight=new_trotter_weight
        x=x_new[:]
        x = x[1:] + x[:1] 
        if step % N == 0:
            k = random.randint(0, N - 1)
            data.append(x[k])
        if step%100==0:
            print ('Step={0},Acceptance Rate {1}%'.format(step,100*step/n_trials))
            
    print ('Acceptance Rate {0}%'.format(100*n_steps/n_trials))
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
    pylab.savefig('plot_C2_beta%s.png' % beta)

def plot_path(x,figure=1):
    pylab.figure(figure)
    y=[i*beta/N for i in range(N)]
    pylab.plot(x,y)
    pylab.xlabel('$x$')
    pylab.ylabel('$Time=\\frac{i \\beta}{N}$')
    pylab.title('Levy harmonic path')
    pylab.savefig('plot_C1_path_beta%s.png' % beta)

start_time = time.time()    
x,data = create_path(levy_path=lambda xstart, xend, dtau, N:levy_harmonic_path(xstart, xend, dtau, N))
write_path(x)
plot_histogram(data)
plot_path(x,figure=2)

print('--- {0:.1f} minutes ---'.format((time.time() - start_time)/60))

pylab.show()