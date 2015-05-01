# sphere-test.py

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

import boxmuller, math, random,numpy, smac



def accept(d):
    xs = direct_sphere(d)
    xs.append(2.0*random.random()-1)
#    print xs
    sumsq=sum ([x*x for x in xs])
#    print sumsq
    return sumsq<=1

def acceptance_ratio(d,n):
    count=0
    for i in range(n):
        if accept(d): count+=1
    return float(count)/n

if __name__=="__main__":
#    print direct_sphere(10)
#    print acceptance_ratio(250,1000)
#    print acceptance_ratio(250,1000)*acceptance_ratio(251,1000), math.pi/(252/2)
    import matplotlib.pyplot as plt
    N=1000000
    sg=smac.SphereGenerator(3*N)
    energies=[x*x+y*y+z*z for (x,y,z) in sg.direct_sphere()]
    plt.hist(energies,bins=500)
    plt.title("Gaussian Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()          
        