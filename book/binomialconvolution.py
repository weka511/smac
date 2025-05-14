#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Limited

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

'''Algorithm 1.25 from Krauth'''

from os.path import basename, splitext
import numpy as np
from matplotlib.pyplot import figure, show

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def binomial_convolution(theta = np.pi/4,N=9):
    '''Algorithm 1.25 from Krauth'''
    P = np.full((N,N),np.nan)   # P[N,k] - k hits in N trials
    P[0,0] = 1
    for n in range(1,N):
        P[n,0] = (1-theta) * P[n-1,0]
        for k in range(1,n):
            P[n,k] = (1-theta) * P[n-1,k] +  theta* P[n-1,k-1]
        P[n,n] = theta * P[n-1,n-1]

    return P


if __name__=='__main__':
    theta = np.pi/4              # p hit
    fig = figure()
    ax = fig.add_subplot(1,1,1)

    P = binomial_convolution(theta = np.pi/4,N=1000)
    ax.plot(P[-1,:])
    # for n in range(1,9):
        # ax.plot(P[n,:],label=f'n={n}')
    # ax.legend()

    fig.savefig(get_plot_file_name())
    show()
