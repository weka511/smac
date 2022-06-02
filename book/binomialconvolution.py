# binomialconvolution.py

# Copyright (C) 2015,2018 Greenweaves Software Pty Ltd

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

import math,matplotlib.pyplot as plt

# Algorithm 1.25 from Krauth
def binomial_convolution(theta,pi):
    def calculate_row(pi):
        return [theta*x + (1-theta)*y for (x,y) in zip(pi[:-1],pi[1:])]
    return calculate_row([0]+pi+[0])
    

if __name__=="__main__":
    pi=[1]
    theta=math.pi/4
    for i in range(8):
        pi=binomial_convolution(theta,pi)
        plt.plot(pi)
    plt.show()
    