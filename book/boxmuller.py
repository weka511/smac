# boxMuller.py

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

if __name__=="__main__":
    import matplotlib.pyplot as plt, smac
    gauss=smac.BoxMuller()
    gaussian_numbers=[]
    for i in range(1000000):
        gaussian_numbers.append(gauss.gauss())
    plt.hist(gaussian_numbers,bins=200,normed=True)
    plt.title("Gaussian Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()    

 