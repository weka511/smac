# template.py

# Copyright (C) 2020 Greenweaves Software Limited

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

# Template for programs

import math,matplotlib.pyplot as plt,numpy as np,os
from matplotlib import rc

# Determine plot file name

def get_plot_file_name(plot):
    if len(plot)==0:
        return '{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0])
    base,ext = os.path.splitext(plot)
    if len(ext)==0:
        return '{0}.png'.format(plot)
    return plot

if __name__=='__main__':
    import argparse
    
    parser = argparse.ArgumentParser('Template')
    parser.add_argument('--show',                           action='store_true', help='Show plot')
    parser.add_argument('--plot', default='',                                   help='Name of plot file')
    args   = parser.parse_args()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    plt.figure(figsize=(20,20))
    plt.plot([1,2,3])
    plt.savefig(get_plot_file_name(args.plot))   
    if args.show:
        plt.show()    
