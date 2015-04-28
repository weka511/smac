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

def gauss(sigma=1.0):
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

    
if __name__=="__main__":
    import matplotlib.pyplot as plt
    gaussian_numbers=[]
    for i in range(1000000):
        (x,y)=gauss()
        gaussian_numbers.append(x)
        gaussian_numbers.append(y)   
    plt.hist(gaussian_numbers,bins=200)
    plt.title("Gaussian Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()    

 