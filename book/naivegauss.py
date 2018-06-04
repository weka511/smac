# gauss.py

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
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

import random, math, smacfiletoken as ft

def gauss(k):
    return sum([random.random()-0.5 for kk in range(k)])/math.sqrt(k/12.0)


m=25
n=1000

def get_frequencies(k):
    frequencies=[]
    xs=[]
    for i in range(2*m+1):
        xs.append(i)
        frequencies.append(0)
        
    for i in range(n):
        r=gauss(k)
        rindex=int(m*r/math.sqrt(12*k))+m
        frequencies[rindex]+=1
        
    for i in range(2*m+1):
        frequencies[i]/=float(2*m+1)
 
    return (xs,frequencies)

if __name__=="__main__":
    import matplotlib.pyplot as plt
    
    for k in range(1,12):
        (xs,frequencies)=get_frequencies(k)
        plt.plot(xs,frequencies,label='k={0}'.format(k))
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Gauss')
        plt.legend(loc='upper left')
        plt.savefig(ft.make_temp_file('gauss.png'))
        
    plt.show()    
