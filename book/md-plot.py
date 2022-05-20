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
from matplotlib.pyplot import colorbar, figure, show, subplot
from numpy             import array, exp, log
from os.path           import basename, splitext
from matplotlib        import rc
from scipy.stats       import linregress

def read_input(file_name='md.csv'):
    '''Extract positions and velocities of each particle from input file'''
    Xs    = []
    Ys    = []
    Zs    = []
    Us    = []
    Vs    = []
    Ws    = []
    N     = None
    n     = None
    d     = None
    M     = None
    L     = None
    V     = None
    sigma = None
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

def get_density_by_shells(h):
    n               = len(h)
    cell_counts     = [4*(n-2*i-1) for i in range(n//2)]
    assert sum(cell_counts)==n**2
    particle_counts = []
    n0              = 0
    n1              = n
    while n0<n1:
        total = 0
        total += sum([h[n0][j] for j in range(n0,n1-1)])
        total += sum([h[n1-1][j] for j in range(n0,n1-1)])
        total += sum([h[i][n0] for i in range(n0,n1-1)])
        total += sum([h[i][n1-1] for i in range(n0,n1-1)])
        particle_counts.append(total)
        check_total = 0
        check_total += sum([1 for j in range(n0,n1-1)])
        check_total += sum([1 for j in range(n0,n1-1)])
        check_total += sum([1 for i in range(n0,n1-1)])
        check_total += sum([1 for i in range(n0,n1-1)])
        assert cell_counts[n0]==check_total
        n0 += 1
        n1 -= 1

    density = [p/c for c,p in zip(cell_counts,particle_counts)]
    return range(len(density)),density

if __name__=='__main__':
    args                                                  = parse_arguments()
    Params,Xs,Ys,Zs,Us,Vs,Ws                              = read_input(file_name=args.input)
    N,n,d,M,L,V,sigma,n_wall_collisions,n_pair_collisions = Params
    Es                                                    = [0.5*(u**2 + v**2* + w**2) for u,v,w in zip(Us,Vs,Ws)]
    pair_collision_ratio                                  = n_pair_collisions/(n_wall_collisions+n_pair_collisions)
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    fig = figure(figsize=(12,12))

    ax1 = fig.add_subplot(2,2,1, projection='3d' if d==3 else None)
    ax1.scatter(Xs,Ys,Zs,
            color = 'xkcd:blue')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Positions')
    ax1.set_xlim(-1,1)
    ax1.set_ylim(-1,1)
    if d==3:
        ax1.set_zlabel('Z')
        ax1.set_zlim(-1,1)

    if d==2:
        ax3         = subplot(2,2,2)
        h,_,_,image = ax3.hist2d(x       = Xs,
                                 y       = Ys,
                                 bins    = 50,
                                 density = False)
        colorbar(image)
        ax3.set_xlabel('X')
        ax3.set_ylabel('Y')
        ax3.set_title('Density')

    if d==2:
        shells,density = get_density_by_shells(h)
        ax4            = subplot(2,2,3)
        ax4.plot(shells,density)
        ax4.set_xlabel('Depth')
        ax4.set_ylabel('Density')
        ax4.set_title('Density by shells')
        ax4.set_ylim((0,max(density)))

    ax5              = subplot(2,2,4)
    n,bins,_         = ax5.hist(Es,
                                bins    = 25,
                                density = True,
                                color   = 'xkcd:blue',
                                label   = f'Observed: {N:,} Epochs, with {100*pair_collision_ratio:.1f}\% pair collisions')
    beta,r,sd,xs,ys  = fit_boltzmann(n,bins)
    ax5.plot(xs,ys,
         color = 'xkcd:red',
         label = f'Bolzmann $\\beta T=${beta:.2f}, $r^2$={r**2:.2f}, std err={sd:.2f}')
    ax5.legend()
    ax5.set_title(f'Energies: dimension = {d}')
    ax5.set_xlabel('E')

    fig.tight_layout()

    fig.savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
