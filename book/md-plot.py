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

'''Visualize output from md.cpp'''

from argparse          import ArgumentParser
from matplotlib.pyplot import arrow, colorbar, figure, hist, hist2d, legend, plot, savefig, scatter,  show, subplot, \
                                suptitle, tight_layout, title, xlabel, ylabel
from numpy             import array, exp, log
from os.path           import basename, splitext
from matplotlib        import rc
from scipy.stats       import linregress

def read_input(file_name='md.csv'):
    Xs = []
    Ys = []
    Us = []
    Vs = []
    N  = None
    with open(file_name) as input_file:
        for line in input_file:
            if '=' in line:
                a,b = line.strip().split('=')
                if a=='N':
                    N = int(b)
                continue
            if 'X1' in line: continue
            x,y,u,v = line.strip().split(",")
            Xs.append(float(x))
            Ys.append(float(y))
            Us.append(float(u))
            Vs.append(float(v))
    return N,Xs,Ys,Us,Vs

def get_curve(n,bins):
    xs     = array([0.5*(bins[i] + bins[i+1]) for i in range(n.shape[0])])
    fitted = linregress(xs,log(n))
    beta   = -fitted.slope
    return beta,xs,exp(fitted.intercept+fitted.slope*xs)

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
    parser.add_argument('--input',
                        default = 'md/check.csv',
                        help    = 'Name of file produced by md.cpp')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()
    N,Xs,Ys,Us,Vs = read_input(file_name=args.input)
    Es          = [0.5*(u**2 + v**2) for u,v in zip(Us,Vs)]
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize=(12,12))
    subplot(2,2,1)
    scatter(Xs,Ys,
            color = 'xkcd:blue')
    xlabel('X')
    ylabel('Y')
    title('Positions')

    subplot(2,2,2)
    scale = 0.01
    for x,y,u,v in zip(Xs,Ys,Us,Vs):
        arrow(x,y,scale*u,scale*v,
              color      = 'xkcd:blue',
              head_width = 0.05)
    xlabel('X')
    ylabel('Y')
    title('Velocities')

    subplot(2,2,3)
    hist2d(Xs,Ys,
           bins  = 25,
           range = [[-1,1],[-1,1]])
    colorbar()
    xlabel('X')
    ylabel('Y')
    title('Density')

    subplot(2,2,4)
    n,bins,_    = hist(Es,
                       bins    = 25,
                       density = True,
                       color   = 'xkcd:blue',
                       label   = 'Observed')
    beta,xs,ys  = get_curve(n,bins)
    plot(xs,ys,
         color = 'xkcd:red',
         label = f'Bolzmann $\\beta T=${beta:.4f}')
    legend()
    title('Energies')
    xlabel('E')

    suptitle(f'Configuration after {N:,} collisions')
    tight_layout()

    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
