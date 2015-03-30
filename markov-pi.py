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

import random, smacfiletoken as ftk

registry=ftk.Registry()
registry.register_all("markov-pi%d.txt")

x, y = 1.0, 1.0
[total_trials,n_hits,x,y]= registry.read([0,0,1.0,1.0])

delta = 0.1
n_trials = 4000000

for i in range(n_trials):
    if registry.is_kill_token_present(): break    
    del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
    if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
        x, y = x + del_x, y + del_y
    if x*x + y*y < 1.0: n_hits += 1
    total_trials+=1
    
registry.write([total_trials,n_hits,x, y])

print 4.0 * n_hits / float(total_trials)
