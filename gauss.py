# gauss.py

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

import random, math

def naive_gauss(k):
    return sum([random.random()-0.5 for kk in range(k)])/math.sqrt(k/12.0)

if __name__=="__main__":
    import pylab
    
m=10
n=100

def pl(k):
    frequencies=[]
    xs=[]
    for i in range(2*m+1):
        xs.append(i)
        frequencies.append(0)
    for i in range(n):
        r=naive_gauss(k)
        rindex=int(m*(r+1))
        if (rindex<0):
#            print rindex
            rindex=0
        if (rindex>2*m):
            print rindex
            rindex=2*m
        frequencies[rindex]+=1
    for i in range(2*m+1):
        frequencies[i]/=float(2*m+1)
 #   pylab.subplot(100+k)   
    pylab.plot(xs, frequencies, 'o')
    #pylab.xlabel('Log N trials')
    #pylab.ylabel('Log Error')
    #pylab.title('Error vs iteration number')
    #pylab.savefig('markov-discrete-pebble.png')
    pylab.show()    
    
pl(8)