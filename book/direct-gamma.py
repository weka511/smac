import random,pylab,math

def direct_gamma(gamma,generator=False,K=10000,N=1000000):
    sigma = 0
    sigma_sq = 0
    for i in range(N):
        x = random.uniform(0,1)
        sigma += x**gamma
        sigma_sq += x**(2*gamma)
        if generator and i%K==0:
            yield(i,sigma/(i+1))        
    diff = sigma_sq-sigma*sigma
    Obs = sigma/N
    return (Obs,math.sqrt(sigma_sq/N-Obs*Obs)/N)


if __name__ == '__main__':
    pylab.style.use('ggplot')
    xs = []
    ys = []
    
    for i,Obs in direct_gamma(-0.8,generator=True):
        xs.append(i)
        ys.append(Obs)
    pylab.plot(xs,ys)
    pylab.xlabel(r'$Number\ of\ samples\ i$')
    pylab.ylabel(r'$Running\ average\ \frac{\Sigma}{N}$')
    pylab.title(r'$Value\ of\ \gamma\ integral$')
    pylab.savefig('direct-gamma.png')
    pylab.show()
