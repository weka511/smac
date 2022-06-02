# Copyright (C) 2015-2012 Greenweaves Software Limited

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

''' Test for Box Muller algorithm'''

from matplotlib.pyplot import hist, show, title, xlabel, ylabel
from smac              import BoxMuller

if __name__=="__main__":

    gauss = BoxMuller()

    hist([gauss.gauss() for _ in range(1000000)],
         bins    = 200,
         density = True)
    title("Gaussian Histogram")
    xlabel("Value")
    ylabel("Frequency")
    show()
