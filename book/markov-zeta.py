# Copyright (C) 2015,2018 Greenweaves Software Limited

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

import random, matplotlib.pyplot as plt

def markov_zeta(delta,zeta,x):
    x_bar=x+2*delta*random.random()-delta
    if 0<x_bar and x_bar<1:
        p_accept=(x_bar/x)**zeta
        if random.random()<p_accept: x=x_bar
    return x

if __name__=="__main__":
    from matplotlib import rc
    rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    rc('text', usetex=True)    
    delta=0.005
    n=1000000
    x=1
    zeta=-0.8
    xs=[]
    
    for i in range(0,n):
        x=markov_zeta(delta,zeta,x)
        xs.append(x)
    plt.figure(1)   
    plt.plot(xs)
    plt.title('$\zeta=-0.8$')
    plt.savefig('markov-zeta-0-8.png')
    
    x=1
    zeta=-1.6
    xs=[]
    
    for i in range(0,n):
        x=markov_zeta(delta,zeta,x)
        xs.append(x)
    plt.figure(2)    
    plt.plot(xs)
    plt.title('$\zeta=-1.6$')
    plt.savefig('markov-zeta-1-6.png')
    plt.show()