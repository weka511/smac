#!/usr/bin/env python

# Copyright (C) 2022 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''
Monte Carlo simulation of Exercise 2.11 of Chaosbook
In higher dimensions, any two vectors are nearly orthogonal
'''
from matplotlib.pyplot import figure, savefig, hist, show
from numpy             import arccos, dot, linspace, mean, pi, sqrt, std, zeros
from numpy.linalg      import norm
from numpy.random      import normal
from scipy.stats       import norm as gaussian

d     = 10000
N     = 1000000
bins  = 100

x0    = zeros(d)
x0[0] = 1
sigma = 1/ sqrt(d)
X0    = []
Theta = []

# Use Krauth, algorihm 1.23. Only the x1 is needed for our result, but we'll canculate all the sx

for i in range(N):
    x          = normal(scale = sigma,
                        size  = d)
    x          = x/norm(x)
    projection = dot(x,x0)
    X0.append(projection)
    Theta.append(arccos(projection))

m0        = mean(X0)
std0      = std(X0)
xs        = linspace(min(X0), max(X0))
rv        = gaussian(scale = sigma)

m_theta   = mean(Theta)
std_theta = std(Theta)
xs_theta  = linspace(min(Theta), max(Theta))
rv_theta  = gaussian(loc   = pi/2,
                     scale = sigma)

fig = figure(figsize=(12,12))
axs = fig.subplots(nrows=2)

fig.suptitle(f'd={d}, N= {N}')
sqrt_d = r'$\frac{1}{\sqrt{d}}=$'
axs[0].hist(X0,
            bins    = bins,
            density = True,
            label   = f'Observed: mean={m0:0.4f}, std={std0:0.4f}')
axs[0].plot(xs,rv.pdf(xs),
            label = f'Gaussian: std={sqrt_d}{sigma}')
axs[0].set_title(r'Inner Product: $\mathbf{x}_1^\intercal \mathbf{x}_2$')
axs[0].legend()

axs[1].hist(Theta,
            bins    = bins,
            density = True,
            label   = f'Observed: mean={m_theta:0.4f}, std={std_theta:0.4f}')
axs[1].plot(xs_theta,rv_theta.pdf(xs_theta),
            label = f'Gaussian: mean={pi/2:0.4f}, std={sqrt_d}{sigma}')
axs[1].set_title(r'$\theta$')
axs[1].legend()

savefig('direct-surface')
show()
