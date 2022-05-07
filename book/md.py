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

'''Algorithm 2.3 Pair collision'''

from argparse          import ArgumentParser
from matplotlib.pyplot import figure, hist, plot, savefig, show, title
from numpy             import dot, multiply, sqrt
from numpy.linalg      import norm
from numpy.random      import default_rng
from os.path           import basename, splitext
from matplotlib        import rc
from sys               import maxsize

def get_pair_time(x1, x2, v1, v2, sigma=0.01):
    '''Algorithm 2.2 Pair Time. Pair collision time for two particles'''
    Delta_x = x1 - x2
    Delta_v = v1 - v2
    Upsilon = dot(Delta_x,Delta_v)**2 - dot(Delta_v,Delta_v)*(dot(Delta_x,Delta_x)-4*sigma**2)
    return - (dot(Delta_x,Delta_v)+sqrt(Upsilon))/dot(Delta_v,Delta_v) if Upsilon>0 and dot(Delta_x,Delta_v) <0 else float('inf')

def get_wall_time(x1, x2, v1, v2, sigma=0.01, d=2, L=[1,1,1]):
    t = float('inf')
    for i in range(d):
        pass

def collide_pair(x1, x2, v1, v2):
    '''Algorithm 2.3 Pair collision'''
    Delta_x      = x1 - x2
    e_hat_perp   = Delta_x/norm(Delta_x)
    Delta_v      = v1 - v2
    Delta_v_perp = dot(Delta_v,e_hat_perp)
    return (v1 - Delta_v_perp*e_hat_perp, v2 + Delta_v_perp*e_hat_perp)



def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def create_rng(seed0):
    '''
    Make sure run is reproducible by displaying seed

    Parameters:
         seed0 is seed supplied by user

    Returns: Default random number generator, seedes with seed0 or newly generated seed
    If seed0 is not Mone, use it

    If seed0 is None (no seed supplied),
    generate a new seed using random number generator and print it so user can reuse.

    '''
    rng    = default_rng(seed = seed0)
    if seed0==None:
        seed = rng.integers(0,maxsize)
        print (f'Setting seed to {seed}')
        return default_rng(seed = seed)
    else:
        return rng

def sample(rng,
           L      = 1,
           V      = 1,
           sigma  = 0.1,
           d      = 2):
    '''Find one sample where points admissable'''
    while True:
        x1 =  2 * multiply(L, rng.random((d,))) - L
        x2 =  2 * multiply(L, rng.random((d,))) - L
        v1 = -V + 2 * V * rng.random((d,))
        v2 = -V + 2 * V * rng.random((d,))
        if dot(x1-x2,x1-x2) > 4 * sigma**2 and dot(x1 - x2,v1 - v2)<0:
            return x1,x2, v1, v2

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--action',
                        default = 'run',
                        choices = ['test',
                                   'run'])
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    parser.add_argument('--seed',
                        type    = int,
                        default = None,
                        help    = 'Seed for random number generator')
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.1,
                        help    = 'Radius of spheres')
    parser.add_argument('--N',
                        type = int,
                        default = 10000000,
                        help = 'Number of iterations')
    parser.add_argument('--d',
                        type    = int,
                        default = 2,
                        choices = [2,3],
                        help    = 'Dimension of space')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()
    rng    = create_rng(args.seed)
    L      = [1] * args.d
    n      = 0
    Diffs  = []
    while True:
        x1, x2, v1, v2 = sample(rng,
                                sigma = args.sigma,
                                L     = L,
                                d     = args.d)
        DeltaT         = get_pair_time(x1,x2,v1,v2,sigma = args.sigma)
        if DeltaT<float('inf'):
            n += 1
            x1_prime = x1 + DeltaT *v1
            x2_prime = x2 + DeltaT *v2
            v1_prime, v2_prime = collide_pair(x1_prime, x2_prime, v1, v2)
            E = dot(v1,v1) + dot(v2,v2)
            E_prime = dot(v1_prime,v1_prime) + dot(v2_prime,v2_prime)
            Diffs.append((E-E_prime)/(E+E_prime))
        if n>args.N: break

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize=(12,12))
    hist(Diffs,
         bins=250 if args.N>9999 else 25)
    title (f'Discrepancy in energies for {args.N:,} trials')
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
