# markov-pi.py

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

import random, math, matplotlib.pyplot as plt

def distance(z1,z2):
   return (z1[0]-z2[0])*(z1[0]-z2[0])+(z1[1]-z2[1])*(z1[1]-z2[1])
   
def direct_disks_any(n,l_x,l_y):
   pts=[]
   for k in range(n):
      pts.append((random.random()*l_x,random.random()*l_y))
   
   sigma_squared=min([distance(pts[k],pts[l]) for k in range(len(pts)) for l in range(k)])
   
   return math.pi*0.5*sigma_squared*n/(l_x*l_y)
   

#print direct_disks_any(10,1,1)

etas=[]

for i in range(100000):
   etas.append(direct_disks_any(16,1,1))
   
n, bins, patches = plt.hist(etas,50)

plt.show()
