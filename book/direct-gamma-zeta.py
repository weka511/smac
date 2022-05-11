# Copyright (C) 2015 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

import random,math

def direct_gamma_zeta(gamma,zeta,n):
    sigma=0
    sigma2=0
    for i in range(n):
        x=0
        while x==0:
            x=random.random()
        x1=x**(1/(1+zeta))
        x2=x1**(gamma-zeta)
        sigma+=x2
        sigma2+=(x2*x2)
    mean=sigma/n
    return (mean,math.sqrt(sigma2/n-mean*mean)/math.sqrt(n))

def run(zeta,n):
    print(zeta)
    for gamma in [2.0,1.0,0.0,-0.1,-0.4,-0.8]:
        (s,t)=direct_gamma_zeta(gamma,zeta,n)
        print (gamma, s-t,s+t, (zeta+1)/(gamma+1))
            
if __name__=="__main__":
    for zeta in [0.0, -0.1, -0.7]:
        run(zeta,1000)