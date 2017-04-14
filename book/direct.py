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

# Problem 1.1 from Werner Krauth, Statistical Mechanics, Algorithms & Computations
# plus Problem 1.3

import random, smacfiletoken as ftk

if __name__=='__main__':
    n_trials = 400000
    
    registry=ftk.Registry()
    registry.register_all("direct%d.txt")
    
    [total_trials,n_hits]= registry.read([0,0])
    
    for iter in range(n_trials):
        if registry.is_kill_token_present(): break
        x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
        if x*x + y*y < 1.0: 
            n_hits += 1
        total_trials+=1
        
    print ('Total Trials=%(total_trials)d, hits=%(n_hits)d, estimate%(estimate)f'%{
        'total_trials':total_trials,
        'n_hits':n_hits,
        'estimate': 4.0 * n_hits / float(total_trials)})
    
    registry.write([total_trials,n_hits])
