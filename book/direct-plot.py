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

import random,math,matplotlib.pyplot as plt

n_trials=10
mult = 2

errors=[]
iterations=[]
for n in range(12):
    print ('n=%(n)d,n_trials=%(n_trials)d'%locals())
    error=0
    for i in range(20):
        n_hits=0
        for iter in range(n_trials):
            x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
            if x*x + y*y < 1.0:  n_hits += 1
        pi_approx=4.0 * n_hits / float(n_trials)
        error+=(math.pi-pi_approx)*(math.pi-pi_approx)
    n_trials *= mult
    errors.append(math.log(error))
    iterations.append(n)    
    
plt.plot(iterations, errors, 'o')
plt.xlabel('Log N trials')
plt.ylabel('Log Error')
plt.title('Error vs iteration number')
plt.savefig('direct-plot.png')
plt.show()