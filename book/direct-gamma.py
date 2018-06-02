import random,pylab,math,numpy as np
from scipy.stats import gaussian_kde

def direct_gamma(gamma,generator=False,K=10000,N=1000000):
    sigma = 0
    for i in range(N): 
        sigma += random.random()**gamma
    return sigma/N


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Evaluate integral from Krauth Section 1.4.')
    parser.add_argument('steps', metavar='M', type=int, nargs=1,help='Number of steps for integral')
    
    args = parser.parse_args()
    M = args.steps[0]
    gamma = -0.8
    
    for N in [1,10,100,1000,10000]:
        def scaled(n):
            return (direct_gamma(gamma,N=n)-5)/(N**(-1-gamma))
        data = [direct_gamma(gamma,N=N) for m in range(M)]
        density = gaussian_kde(data)
        y,binEdges=np.histogram(data,normed=True,bins=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,100000000000])
        bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        pylab.plot(bincenters,density(bincenters),label='N={0}'.format(N))        
    pylab.xlim(1,10)
    pylab.xlabel(r'$\Sigma/N$')
    pylab.ylabel(r'$\pi(\Sigma/N$)')
    pylab.title(r'$Average\ {0}\ iterations$'.format(M))
    pylab.legend()
    pylab.savefig('histogram.png')
    pylab.show()
    

