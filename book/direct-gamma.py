import random,pylab,math,numpy as np

def direct_gamma(gamma,generator=False,K=10000,N=1000000):
    sigma = 0
    for i in range(N):
        x = random.random()
        sigma += x**gamma
    return sigma/N


if __name__ == '__main__':
    M = 100000
    gamma = -0.8
    
    for N in [1,10,100,1000,10000]:
        def scaled(n):
            return (direct_gamma(gamma,N=n)-5)/(N**(-1-gamma))
        data = [scaled(N) for m in range(M)]
        #data = [direct_gamma(gamma,N=N) for m in range(M)]
        y,binEdges=np.histogram(data,normed=True,bins=int(M/50))
        bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        pylab.plot(bincenters,y,'-',label='N={0}'.format(N))       
    #pylab.xlim(1,10)
    pylab.xlim(-10,2)
    pylab.xlabel(r'$\Sigma/N$')
    pylab.ylabel(r'$\pi(\Sigma/N$)')
    pylab.title(r'$Average\ {0}\ iterations$'.format(M))
    pylab.legend()
    pylab.savefig('histogram.png')
    pylab.show()
    

