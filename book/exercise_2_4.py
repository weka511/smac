#!/usr/bin/env python

#   Copyright (C) 2025 Simon Crase

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
    Exercise 2-4. Sinai's system of two large sphere in a box. Show histogram of positions.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from numpy.testing import assert_allclose
from matplotlib import rc
from matplotlib.pyplot import figure, show

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--L', type = float, default = 1.0, help = 'Length of box')
    parser.add_argument('--sigma', type = float, default = 0.365, help = 'Radius of sphere')
    parser.add_argument('--N', type = int, default = 1000, help = 'Number of steps to evolve configuration')
    parser.add_argument('--DeltaT', type = float, default = 1.0, help = 'For sampling')
    parser.add_argument('--freq', type = int, default = 250, help = 'For reporting')
    parser.add_argument('--m', type = int, default = 100, help = 'Number of bins for histogram')
    parser.add_argument('--V', type = float, default = 1.0, help = 'Velocity')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
    args = parser.parse_args()
    if 0.25*args.L < args.sigma and args.sigma < 0.5 * args.L:
        return args
    else:
        parser.error('sigma should be between 0.25L and 0.5L')

def get_bins(bins):
    '''
    Used to parse args.bins: either a number of bins, or the name of a binning strategy.
    '''
    try:
        return int(bins)
    except ValueError:
        if bins in ['auto', 'fd', 'doane', 'scott', 'sturges', 'sqrt', 'stone', 'rice']:
            return bins
        raise ArgumentTypeError(f'Invalid binning strategy "{bins}"')

def get_file_name(name,default_ext='png',seq=None):
    '''
    Used to create file names

    Parameters:
        name          Basis for file name
        default_ext   Extension if non specified
        seq           Used if there are multiple files
    '''
    base,ext = splitext(name)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    qualified_name = f'{base}.{ext}'
    if ext == 'png':
        return join(args.figs,qualified_name)
    else:
        return qualified_name

def create_config(sigma=0.375,L=1,V=1,corners=np.array([[0,0],[0,1],[1,1],[1,0]]),rng=np.random.default_rng(),n=100):
    '''
    Establish a starting point for iterations.

    Parameters:
        sigma    Radius of sphere
        L        Length of one size of box
        V        Used to normalize velocities
        corners  Centres of the 4 quarter spheres (fixed sphere)
        rng      Random number generator
        n        Number of attempts to generate acceptable starting point

    Returns:
        x      An acceptable starting position
        v      A random velocity in the range (-V,V)
    '''
    def acceptable(x):
        for i in range(m):
            if np.dot(x - corners[i,:],x - corners[i,:]) < 4*sigma**2:
                return False
        return True

    m,d = corners.shape
    for i in range(n):
        x = L*rng.random((d))
        if acceptable(x):
            return x,V*(2*rng.random((d)) - 1)

    raise ValueError(f'create_config(...) Could not find a starting configuration with sigma={sigma} after {n} attempts')



def get_pair_time(x, x_center, v, sigma = 0.01,cutoff=1e-8):
    '''
    Algorithm 2.2 Pair Time. Pair collision time for two spheres

    Parameters:
        x         Centre of moving sphere
        x_center  Centre of the other sphere
        v         Velocity of moving sphere
        sigma     Radius of sphere

    Returns:
        The time at which two spheres will collide: may be np.inf
    '''
    Delta = x - x_center
    Upsilon = np.dot(Delta,v)**2 + np.dot(v,v)*( 4*sigma**2 - np.dot(Delta,Delta) )
    if Upsilon > 0:
        if abs(np.dot(Delta,v)**2 - Upsilon) > cutoff:
            dt1 = - (np.dot(Delta,v) + np.sqrt(Upsilon)) / np.dot(v,v)
            dt2 = - (np.dot(Delta,v) - np.sqrt(Upsilon)) / np.dot(v,v)
            if dt1 > cutoff and dt2 > cutoff: return min(dt1,dt2)
            if dt1 > cutoff and dt2 < 0: return dt1
            if dt1 < 0 and dt2 > cutoff: return dt2
        else:
            dt = -2 * np.dot(Delta,v)/ np.dot(v,v)
            if dt > 0:
                return dt
    return float('inf')

def get_wall_time(x,v,L=1,d=2):
    '''
    Establish the time to the next collision with a wall

    Parameters:
        x
        v
        L
        d

    Returns:
        t
        index
        direction
    '''
    t = float('inf')
    direction = 0
    index = -1
    for i in range(d):
        if v[i] < 0:
            t0 = - x[i]/v[i]
        if v[i] > 0:
            t0 = (L - x[i])/v[i]

        if t0 < t:
            t = t0
            index = i
            direction = np.sign(v[i])

    return t,index,direction

def collide_pair(x, x_center, v):
    '''
        Algorithm 2.3 Pair collision

        Parameters:
            x          Centre of moving sphere
            x_center   Centre of stationary sphere
            v          Velocity of moving sphere

        Returns:
           Velocities after collision
        '''
    Delta_x = x - x_center
    e_hat_perp = Delta_x/np.linalg.norm(Delta_x)
    Delta_v_perp = np.dot(v,e_hat_perp)
    return v - 2* Delta_v_perp*e_hat_perp

def box_it(x,L=1,d=2):
    '''
    Restrict x to be within box defined by L
    '''
    for k in range(d):
        while x[k] > args.L:
            x[k] -= args.L
        while x[k] < 0:
            x[k] += args.L
    return x

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)

    corners = np.array([[0,0],[0,args.L],[args.L,args.L],[args.L,0]])
    T = np.zeros((len(corners)+1))
    X = np.zeros((args.N,2))
    V = np.zeros((args.N,2))
    x,v = create_config(args.sigma,args.L,corners=corners,rng=rng,V=args.V)

    X[0,:],V[0,:] =x,v
    for i in range(1,args.N):
        T[len(corners)] = args.DeltaT          # Time until next sample due
        if i%args.freq == 0:
            print (f'Epoch={i:,}')
        sampled = False
        # Iterate through a sequence of collisions until
        # we reach a time step so we can sample
        while not sampled:
            t_wall,index,direction = get_wall_time(x,v,L=args.L)
            for j in range(len(corners)):
                T[j] = get_pair_time(x, corners[j,:], v, sigma = args.sigma)

            j = np.argmin(T)    # Index of next event: either collision or sample
            if t_wall < T[j]:
                x += t_wall * v
                x[index] -= args.L * direction
                T[len(corners)] -= t_wall
            else:
                x += T[j] * v       # Position of next event

                if j < len(corners):   # Collision
                    assert_allclose(2*args.sigma, np.sqrt(np.dot(x- corners[j,:],x- corners[j,:])))
                    v = collide_pair(x, corners[j,:], v)
                    T[len(corners)] -= T[j]               # Update time until next sample
                else:                                     # Event is a sample
                    x = box_it(x,L=args.L)
                    X[i,:],V[i,:] =x,v
                    sampled = True

    bins = np.linspace(0, args.L, num = args.m)
    fig = figure(figsize=(8,12))
    fig.suptitle(fr'L={args.L}, $\sigma=${args.sigma}, N={args.N:,d}, $\Delta T=${args.DeltaT}, V={args.V}')

    ax1 = fig.add_subplot(2,2,1)
    ax1.scatter(X[:,0],X[:,1],s=1)

    ax2 = fig.add_subplot(2,2,2)
    ax2.axis('scaled')
    h,_,_,mappable = ax2.hist2d(X[:,0],X[:,1], bins = [bins,bins], density = True)
    fig.colorbar(mappable)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    # Show distribution of frequencies

    ax3 = fig.add_subplot(2,2,3)
    r = h.ravel()
    ax3.hist (r[r>0], density = True, color = 'xkcd:blue',bins=args.bins)
    ax3.set_title(fr'Projected Densities $\eta=${np.pi*args.sigma**2/(4*args.L**2):.3f}, ignoring empty regions')
    ax3.set_xlabel('Density')
    ax3.set_ylabel('Frequency')
    ax3.grid(True)

    Distances= np.zeros((args.N,4))
    for i in range(4):
        Distances[:,i] = np.sqrt(((X-corners[i])**2).sum(axis=1))

    ax4 = fig.add_subplot(2,2,4)
    ax4.hist(Distances.min(axis=1),density=True,color = 'xkcd:blue',bins=args.bins,label='Distribution')
    ax4.axvline(x=2*args.sigma,label=r'$2\sigma$',color='xkcd:red')
    ax4.set_xlabel(r'$\Delta$')
    ax4.set_title('Distribution of distances between centres')
    ax4.legend()

    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
