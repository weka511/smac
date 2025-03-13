#!/usr/bin/env python

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

'''
   Visualize output from md.cpp. Plot distribution of distances from wall,
   and compare energy histogram with Bolzmann distribution.
'''

from argparse          import ArgumentParser
from matplotlib.pyplot import colorbar, figure, show, subplot
from numpy             import array, exp, log, pi
from os.path           import basename, splitext
from matplotlib        import rc
from scipy.stats       import linregress
from seaborn           import kdeplot

def read_input(file_name='md.csv'):
    '''Extract positions and velocities of each particle from input file'''
    Xs                = []
    Ys                = []
    Zs                = []
    Us                = []
    Vs                = []
    Ws                = []
    N                 = None
    n                 = None
    d                 = None
    M                 = None
    L                 = None
    V                 = None
    sigma             = None
    n_wall_collisions = 0
    n_pair_collisions = 0
    with open(file_name) as input_file:
        for line in input_file:
            if '=' in line:
                key,value = line.strip().split('=')
                if key=='N':
                    N = int(value)
                if key=='n':
                    n = int(value)
                if key=='d':
                    d = int(value)
                if key=='M':
                    M = int(value)
                if key=='wall_collisions':
                    n_wall_collisions = int(value)
                if key=='pair_collisions':
                    n_pair_collisions = int(value)
                if key=='sigma':
                    sigma = float(value)
                if key=='L':
                    L = float(value)
                if key=='V':
                    V = float(value)
            elif 'X1' in line:
                continue
            else:
                value_iterator = iter(line.strip().split(","))
                Xs.append(float(next(value_iterator)))
                Ys.append(float(next(value_iterator)))
                Zs.append(float(next(value_iterator)) if d==3 else 0.0)
                Us.append(float(next(value_iterator)))
                Vs.append(float(next(value_iterator)))
                Ws.append(float(next(value_iterator)) if d==3 else 0.0)

    return (N,n,d,M,L,V,sigma,n_wall_collisions,n_pair_collisions),Xs,Ys,Zs,Us,Vs,Ws

def fit_boltzmann(n,bins):
    '''Fit an exponential to the counts in the non-empty bins'''
    xs           = array([0.5*(bins[i] + bins[i+1]) for i in range(n.shape[0])])
    non_empty    = [(x,count) for x,count in zip(xs,n) if count>0 ]
    xs_non_empty = [x for x,_ in non_empty]
    n_non_empty  = [n for _,n in non_empty]
    fitted       = linregress(xs_non_empty,log(n_non_empty))
    return -fitted.slope,fitted.rvalue,fitted.stderr,xs_non_empty,[exp(fitted.intercept+fitted.slope*x) for x in xs_non_empty]

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--bw_adjust',
                        type    = float,
                        default = 1.0,
                        help    = 'Bandwidth adjustment for kdeplot')
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    parser.add_argument('--input',
                        default = 'md/check.csv',
                        help    = 'Name of file produced by md.cpp')
    parser.add_argument('--bins',
                        choices = ['auto', 'fd', 'doane', 'scott', 'stone', 'rice', 'sturges', 'sqrt'],
                        default = 'auto',
                        help    = 'Strategy for assigning bin edges')
    return parser.parse_args()

def get_density(L     = 1,
                d     = 2,
                sigma = 0.01,
                n     = 1):
    '''Calculate density of particles in box'''
    volume_box    = (2*L)**d
    volume_sphere = pi*sigma**2 if d==2 else (4/3)*pi*sigma**3
    return n*volume_sphere/volume_box

if __name__=='__main__':
    args                                                  = parse_arguments()
    Params,Xs,Ys,Zs,Us,Vs,Ws                              = read_input(file_name=args.input)
    N,n,d,M,L,V,sigma,n_wall_collisions,n_pair_collisions = Params
    Es                                                    = [0.5*(u**2 + v**2* + w**2) for u,v,w in zip(Us,Vs,Ws)]
    eta                                                   = get_density(  L     = L,
                                                                          d     = d,
                                                                          sigma = sigma,
                                                                          n     =n)
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    fig = figure(figsize=(12,6))

    ax3         = subplot(1,2,1)
    kdeplot(Xs,
            ax        = ax3,
            bw_adjust = args.bw_adjust,
            color     = 'xkcd:blue',
            label     = 'X')
    kdeplot(Ys,
            ax        = ax3,
            bw_adjust = args.bw_adjust,
            color     = 'xkcd:red',
            label     = 'Y')
    if d==3:
        kdeplot(Zs,
                ax        = ax3,
                bw_adjust = args.bw_adjust,
                color     = 'xkcd:green',
                label     = 'Z')

    ax3.legend(loc='lower center')
    ax3.set_title(f'Positions: n={n}, $\\sigma=${sigma}, $\\eta=$ {eta:.3e}, bandwidth adjust={args.bw_adjust}.')

    ax5              = subplot(1,2,2)
    n,bins,_         = ax5.hist(Es,
                                bins    = args.bins,
                                density = True,
                                color   = 'xkcd:blue',
                                label   = f'Observed: {n_pair_collisions:,} pair collisions, {n_wall_collisions:,} wall collisions')
    beta,r,sd,xs,ys  = fit_boltzmann(n,bins)
    Boltzmann = r'P(E)=$e^{-\beta E}$'
    ax5.plot(xs,ys,
         color = 'xkcd:red',
         label = f'Bolzmann {Boltzmann}, where $\\beta=${beta:.2f}; $r^2$={r**2:.2f}, std err={sd:.2f}')
    ax5.legend()
    ax5.set_title(f'Energies: dimension = {d}')
    ax5.set_xlabel('E')

    fig.tight_layout()

    fig.savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
