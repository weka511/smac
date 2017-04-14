import math, random, pylab

def V(x,cubic, quartic):
    return x*x* (0.5 + x*(cubic+x*quartic))

def rho_free(x, y, beta):    # free off-diagonal density matrix
    return math.exp(-(x - y) ** 2 / (2.0 * beta)) 

# Read data from matrix squaring
def read_file(filename):
    def extract_floats(z):
        x,y=z
        return (float(x),float(y))
    def split_list(ll):
        return ([a for (a,_) in ll],[b for (_,b) in ll])    
    with open(filename) as f:
        return split_list([extract_floats(line.split()) for line in f])

# Plot results for slice k (so we can answer the questions:
# Does the histogram of x[1] give a significantly different result from the histogram of x[0]? 
# Is it correct to produce a histogram of the entire path (x[0] and x[1] and x[2], etc)?
# Notice that I am generating an array delta, whose 1st axis is the slice number,
# 2nd the particular value of x[slice], and I discard the first value when I generate
# the histogram. On my first attempt I tried to initilaize data=[[]]*N, which resulted
# in an array of N pointer to the same list, which prevented me from keeping the slices separate
# Notice also the technique for initializing data (See comments labelled "hack" below) to make
# sure thast each row was separate list.

def plot_results(k,data,xs,rhos):
    pylab.figure(k+1)
    pylab.hist(data[k][1:], 100,normed = 'True',label='Histogram')
    pylab.plot(xs,rhos, c='r',label='Matrix squaring')
    pylab.xlim(-2.0, 2.0)
    pylab.title('Anharmonic oscillator for slice {0}; cubic={1}, quartic={2}'.format(k,cubic,quartic), fontsize = 12)
    pylab.xlabel('$x$', fontsize = 30)
    pylab.ylabel('$Probability$', fontsize = 20)
    pylab.legend(loc='upper left',framealpha=0.5)
    pylab.savefig('c2_{0}.png'.format(k).format(beta)) 
    
if __name__=='__main__':
    quartic=1
    cubic= - quartic    
    (xs,rhos)=read_file('data_anharmonic_matrixsquaring_beta_4.0.dat')

    beta = 4.0
    N = 16                                            # number of slices
    dtau = beta / N
    delta = 1.0                                       # maximum displacement on one slice
    n_steps = 1000000                                 # number of Monte Carlo steps
    x = [0.0] * N                                     # initial path
    data=[]                                           # hack - see plot_result()
    for i in range(N):                                # hack - see plot_result()
        data.append([i+10])                           # hack - see plot_result()
    n_sample = 10
    for step in range(n_steps):
        k = random.randint(0, N - 1)                  # random slice
        knext, kprev = (k + 1) % N, (k - 1) % N       # next/previous slices
        x_new = x[k] + random.uniform(-delta, delta)  # new position at slice k
        old_weight  = (rho_free(x[knext], x[k], dtau) *
                       rho_free(x[k], x[kprev], dtau) *
                       math.exp(-0.5 * dtau * V(x[k],cubic, quartic)))
        new_weight  = (rho_free(x[knext], x_new, dtau) *
                       rho_free(x_new, x[kprev], dtau) *
                       math.exp(-0.5 * dtau * V(x_new,cubic, quartic)))
        if random.uniform(0.0, 1.0) < new_weight / old_weight:
            x[k] = x_new

        if step%n_sample==0:
            for i in range(N):
                data[i].append(x[i])
    
    plot_results(0,data,xs,rhos)
