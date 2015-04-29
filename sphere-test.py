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

import boxmuller, math


def direct_surface(d):
    sigma=1.0/math.sqrt(d)    
    xs=[boxmuller.gauss(sigma) for k in range(d)] 
    Sigma=sum(x*x for x in xs)
    return [x/Sigma for x in xs]

print direct_surface(5)