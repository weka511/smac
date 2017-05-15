import random,pylab,math

def direct_gamma(N,gamma):
    sigma = 0
    sigma_sq = 0
    for i in range(N):
        x = random.uniform(0,1)
        sigma += x**gamma
        sigma_sq += x**(2*gamma)
    diff = sigma_sq-sigma*sigma
    Obs = sigma/N
    #print (diff)
    return (Obs,math.sqrt(sigma_sq/N-Obs*Obs)/N)

N=10000

if __name__ == '__main__':
    for gamma in [2,1,0,-0.2,-0.4,-0.8]:
        Obs,Error = direct_gamma(N,gamma)
        print (gamma, Obs,Error,1/(1+gamma))