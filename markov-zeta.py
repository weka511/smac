# Copyright (C) 2015 Greenweaves Software Pty Ltd

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

import random, pylab

def markov_zeta(delta,zeta,x):
    x_bar=x+2*delta*random.random()-delta
    if 0<x_bar and x_bar<1:
        p_accept=(x_bar/x)**zeta
        if random.random()<p_accept: x=x_bar
    return x

if __name__=="__main__":
    delta=0.01
    n=500000
    x=1
    zeta=-0.8
    xs=[]
    
    for i in range(0,n):
        x=markov_zeta(delta,zeta,x)
        xs.append(x)
    pylab.figure(1)   
    pylab.plot(xs)
    
    x=1
    zeta=-1.6
    xs=[]
    
    for i in range(0,n):
        x=markov_zeta(delta,zeta,x)
        xs.append(x)
    pylab.figure(2)    
    pylab.plot(xs)