# levy-convolution.py

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

def levy(pi,A_Plus=1.25,alpha=1.25):
    x0,_  = pi[0]
    xK,_  = pi[-1]
    K     = len(pi)
    Delta = (xK-x0)/(K-1)
    for k in range(K):
        x = x0 + (K + k) * Delta
        pik = A_Plus/x**(1+alpha)
        pi.append((x,pik))
    pi_dash=[]
    for k in range(0,2*K):
        x = (pi[0][0]+pi[k][0])/(2**(1/alpha))
        pi_x = Delta * sum([pi[i][1]*pi[k-i][1] for i in range(k)])/2**(1/alpha)
        pi_dash.append((x,pi_x))
    norm = sum([p for (_,p) in pi_dash])
    return [(x,p/norm) for (x,p) in pi_dash if x>= x0 and x0 <= xK]

if __name__=='__main__':
    pi=[(x/10,0.1) for x in range(11)]
    for i in range(10):
        pi=levy(pi)
        plt.plot(pi)
    plt.show()