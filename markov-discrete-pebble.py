# markov-discrete-pebble.py

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

neighbour_table =[
    [2,4,0,0],
    [3,5,1,0],
    [0,6,2,0],
    [5,7,0,1],
    [6,8,4,2],
    [0,9,5,3],
    [8,0,0,4],
    [9,0,7,5],
    [0,0,8,6]
]

def markov_discrete_pebble(k,table):
    neighbours=table[k]
    while True:
        n=random.randint(0,3)
        if neighbours[n]!=0: return neighbours[n]
    
visits=[0,0,0,0,0,0,0,0,0]