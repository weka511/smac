# MIT License
# 
# Copyright (c) 2018 Simon Crase
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Implement Algorithm 1.29, subtract mean value for each sample, and generate
# histograms of the average of N samples and the rescaled averages.

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
    parser.add_argument('--N', metavar='N', type=int, nargs='+',default=[1,10,100,1000,10000],help='Number of steps for integral')
    parser.add_argument('--gamma',metavar='gamma',type=float,nargs=1,default=-0.8,help='exponent')
    args = parser.parse_args()
    M = args.steps[0]
    gamma = args.gamma
    bins=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,100000000000]
    
    for N in args.N:
        def scaled(n):
            return (direct_gamma(gamma,N=n)-5)/(N**(-1-gamma))
        data = [direct_gamma(gamma,N=N) for m in range(M)]
        density = gaussian_kde(data)
        y,binEdges=np.histogram(data,normed=True,bins=bins)
        bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        pylab.plot(bincenters,density(bincenters),label='N={0}'.format(N))        
    pylab.xlim(1,10)
    pylab.xlabel(r'$\Sigma/N$')
    pylab.ylabel(r'$\pi(\Sigma/N$)')
    pylab.title(r'$Average\ {0}\ iterations$'.format(M))
    pylab.legend()
    pylab.savefig('histogram.png')
    pylab.show()
    

