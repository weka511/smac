# Copyright (C) 2022 Simon Crase

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

'''Template for programs--replace with description'''

from argparse          import ArgumentParser
from matplotlib.pyplot import figure, plot, savefig,show
from os.path           import basename, splitext
from matplotlib        import rc

# Determine plot file name

def get_plot_file_name(plot):
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

if __name__=='__main__':
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    args   = parser.parse_args()
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    plt.figure(figsize=(20,20))
    plt.plot([1,2,3])
    plt.savefig(get_plot_file_name(args.plot))
    if args.show:
        plt.show()
