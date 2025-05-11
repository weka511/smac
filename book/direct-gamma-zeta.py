#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''
    Exercise 1.21, Algorithm 1.31.
'''

import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib import rc

def direct_gamma_zeta(gamma,zeta,n, rng=np.random.default_rng()):
    def get_positive_sample():
        while True:
            x = rng.random()
            if x > 0: return x

    sigma = 0
    sigma2 = 0
    for i in range(n):
        x = get_positive_sample()
        x1 = x**(1/(1+zeta))
        x2 = x1**(gamma - zeta)
        sigma += x2
        sigma2 += x2**2

    mean = sigma/n
    return (mean,np.sqrt(sigma2/n-mean*mean)/np.sqrt(n))


if __name__=="__main__":
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    rng = np.random.default_rng()
    n = 1000
    gammas = [2.0,1.0,0.0,-0.1,-0.4,-0.8]
    fig = figure(figsize=(12,12))
    for i,zeta in enumerate([0.0, -0.1, -0.7]):
        ax=fig.add_subplot(2,2,i+1)
        y = np.zeros((len(gammas),3))
        for j in range(len(gammas)):
            (s,t) = direct_gamma_zeta(gammas[j],zeta,n,rng=rng)
            y[j,0] = s - t
            y[j,1] = s + t
            y[j,2] = (zeta+1)/(gammas[j]+1)
        ax.plot(gammas,y[:,0],label='Lower bound')
        ax.plot(gammas,y[:,1],label='Upper bound')
        ax.plot(gammas,y[:,2],label='Estimate')
        ax.set_xlabel(r'$\gamma$')
        ax.legend(title=r'$\zeta=$'f'{zeta}')

    fig.tight_layout(h_pad=3)
    show()
