# direct-plot.py

# Copyright (C) 2015 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; with out even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

import random,math,pylab

n_trials=10
n = 1

errors=[]
iterations=[]
while n<8:
    print n_trials
    error=0
    for i in range(20):
        n_hits=0
        for iter in range(n_trials):
            x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
            if x*x + y*y < 1.0: 
                n_hits += 1
        
        pi_approx=4.0 * n_hits / float(n_trials)
        error+=(math.pi-pi_approx)*(math.pi-pi_approx)
        print n_trials,n_hits,pi_approx
    n_trials *= 10
    n+=1
    errors.append(math.log(error))
    iterations.append(n)    
    
pylab.plot(iterations, errors, 'o')
pylab.xlabel('iteration')
pylab.ylabel('apparent error')
pylab.title('Bunching:  error vs iteration number')
pylab.savefig('apparent_error_bunching.png')
pylab.show()