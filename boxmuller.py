# boxMuller.py

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
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

import random, math, smacfiletoken as ft, naivegauss

def gauss0(sigma):
    phi=random.random()*2*math.pi
    while phi==2*math.pi:phi=random.random()*2*math.pi
    rr=random.random()
    while rr==0: rr=random.random()
    upsilon=-math.log(rr)
    r=sigma*math.sqrt(2*upsilon)
    x=r*math.cos(phi)
    y=r*math.sin(phi)
    return (x,y)

def gauss1(sigma):
    upsilon1=2 # force loop to be executed at least once
    while upsilon1==0 or upsilon1>1:
        x=2*random.random()-1
        y=2*random.random()-1
        upsilon1=x*x+y*y
    upsilon=-math.log(upsilon1)
    upsilon2=sigma*math.sqrt(2*upsilon/upsilon1)
    x*=upsilon2
    y*=upsilon2
    return (x,y)



def get_freq(sigma,gauss):
    m=25
    n=10000    
    frequencies=[]
    xs=[]
    for i in range(2*m+1):
        xs.append(i)
        frequencies.append(0)
        
    for i in range(n):
        r,s=gauss(sigma)
        rindex=int(m*r)+m
        frequencies[rindex]+=1
        rindex=int(m*s)+m
        frequencies[rindex]+=1
        
    for i in range(2*m+1):
        frequencies[i]/=float(2*m+1)
    return (xs, frequencies)
    
if __name__=="__main__":
    import matplotlib.pyplot as plt
    (xs, frequencies)=get_freq(0.25,gauss0)
    plt.figure(1)
    plt.plot(xs, frequencies)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Gauss')
    plt.savefig(ft.make_temp_file('gauss1.png'))
    
    (xs, frequencies)=get_freq(0.25,gauss1)
    plt.figure(2)
    plt.plot(xs, frequencies)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Gauss')
    plt.savefig(ft.make_temp_file('gauss1.png'))
    
    plt.figure(3)
    
    (xss,frs)=naivegauss.get_frequencies(12)
    plt.plot(xss,frs)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Gauss')
    plt.savefig(ft.make_temp_file('gauss2.png'))
        
    plt.show()    