#!/usr/bin/env python

# Copyright (C) 2015-2022 Greenweaves Software Limited

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

from math              import pi
from matplotlib.pyplot import plot, savefig, show
from os                import name
from os.path           import basename, splitext

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def binomial_convolution(theta,estimates):
    '''Algorithm 1.25 from Krauth'''
    def calculate_row(estimates):
        return [theta*x + (1-theta)*y for (x,y) in zip(estimates[:-1],estimates[1:])]
    return calculate_row([0] + estimates + [0])


if __name__=="__main__":
    pi_estimates = [1]
    for i in range(8):
        pi_estimates = binomial_convolution(pi/4,pi_estimates)
        plot(pi_estimates)

    if name == 'posix':
        savefig(get_plot_file_name())
    if name == 'nt':
        show()
