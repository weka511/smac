# direct.py

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

import random
import token

n_trials = 4000000

registry=token.Registry()
registry.register_all("direct%d.txt")

[total_trials,n_hits]= registry.read([0,0])

try:
    for iter in range(n_trials):
        x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
        if x*x + y*y < 1.0: 
            n_hits += 1
        total_trials+=1
        
    print total_trials,n_hits,4.0 * n_hits / float(total_trials)
    
    registry.write([total_trials,n_hits])
except (KeyboardInterrupt, SystemExit):
    print "Interrupted"
    registry.write([total_trials,n_hits])
    print "Saved"