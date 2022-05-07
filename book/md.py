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
from numpy             import dot, sqrt
from numpy.linalg      import norm
from os.path           import basename, splitext
from matplotlib        import rc

def get_pair_time(x1, x2, v1, v2, sigma=0.01):
    '''Algorithm 2.2 Pair Time. Pair collision time for two particles'''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    Upsilon = dot(Delta_x,Delta_v)**2 - dot(Delta_v,Delta_v)*(dot(Delta_x,Delta_x)-4*sigma**2)
    return - (dot(Delta_x,Delta_v)+sqrt(Upsilon))/dot(Delta_v,Delta_v) if Upsilon>0 and dot(Delta_x,Delta_v) <0 else float('inf')

def collide_pair(x1, x2, v1, v2, sigma=0.01):
    '''Algorithm 2.3 Pair collision'''
    Delta_x      = x1 - x2
    e_hat_perp   = Delta_x/norm(Delta_x)
    Delta_v      = v1 - v2
    Delta_v_perp = dot(Delta_v,e_hat_perp)
    return (v1 - Delta_v_perp*e_hat_perp, v2 - Delta_v_perp*e_hat_perp)

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize=(12,12))
    plot([1,2,3])
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
