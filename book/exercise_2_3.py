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
    Exercise 2.3. Implement algorithm 2.1 (event disks) for disks in a square
    box without periodic boundary conditions. Start from a legal configuration,
    allowing restart as discussed in exercise 1.3. Sample at regular intervals,
    and generate histograms of position and velocity.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext, exists
from os import replace
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from md import create_config, get_next_pair, get_next_wall, collide_pair, get_L, Collision
from smacfiletoken import Registry

def parse_arguments():
    '''Parse command line arguments'''
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--sigma', type    = float, default = 0.125, help = 'Radius of spheres')
    parser.add_argument('-N','--N', type = int, default = 1000, help = 'Number of iterations')
    parser.add_argument('-n','--n', type = int, default = 4, help = 'Number of spheres')
    parser.add_argument('-M','--M', type = int, default = 1000, help = 'Number of attempts to create configuration')
    parser.add_argument('-L','--L', type = float, nargs = '+', default = [1,1], help = 'Lengths of box walls')
    parser.add_argument('-d','--d', type = int, default = 2, choices = [2,3], help = 'Dimension of space')
    parser.add_argument('--freq', type = int, default = 250, help = 'For reporting')
    parser.add_argument('--DeltaT', type = float, default = 1.0, help = 'For sampling')
    parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
    parser.add_argument('--restart', default = None, help  = 'Restart from checkpoint')
    return parser.parse_args()

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

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    registry = Registry()
    registry.register_all("md%d.txt")

    if args.restart == None:
        n = args.n
        d = args.d
        L = np.array(args.L)
        sigma = args.sigma
        M = args.M
        DeltaT = args.DeltaT
        Xs,Vs = create_config(n = n, d = d, L = L, sigma = sigma, rng = rng, M = M)
        bins = get_bins(args.bins)
        binsv = get_bins(args.bins)
        binsvx = get_bins(args.bins)
    else:
        with np.load(args.restart) as  npzfile:
            Xs = npzfile['Xs']
            Vs = npzfile['Vs']
            counts = npzfile['counts']
            bins =  npzfile['bins']
            countsv = npzfile['countsv']
            binsv =  npzfile['binsv']
            countsvx = npzfile['countsvx']
            binsvx =  npzfile['binsvx']
            L = npzfile['L']
            sigma = float(npzfile['sigma'])
            DeltaT = float(npzfile['DeltaT'])
            _,d = Xs.shape

    T = np.zeros((3)) # times to next wall collision, next pair colliion, and next sample time
    X_all_disks = np.zeros((args.N,args.n))
    Vx_all_disks = np.zeros((args.N,args.n))
    V_all_disks = np.zeros((args.N,args.n))
    for i in range(args.N):
        if registry.is_kill_token_present():
            X_all_disks = X_all_disks[0:i,:]
            V_all_disks = V_all_disks[0:i,:]
            Vx_all_disks = Vx_all_disks[0:i,:]
            break

        t = args.DeltaT * i
        if i%args.freq == 0:
            print (f'Epoch={i:,},t={t}')
        T[Collision.SAMPLE] = args.DeltaT + t
        sampled = False
        # Iterate through a sequence of collisions until
        # we reach a time step so we can sample
        while not sampled:
            dt_wall,wall,j = get_next_wall(Xs, Vs, sigma = args.sigma, d = args.d, L = L)
            dt_pair, k, l = get_next_pair(Xs,Vs,sigma=args.sigma)
            T[Collision.WALL] = t + dt_wall
            T[Collision.PAIR] = t + dt_pair
            match np.argmin(T):
                case Collision.WALL:
                    Xs += dt_wall * Vs
                    Vs[j][wall] = - Vs[j][wall]
                    t += dt_wall
                case Collision.PAIR:
                    Xs += dt_pair * Vs
                    Vs[k], Vs[l] = collide_pair(Xs[k], Xs[l], Vs[k], Vs[l])
                    t += dt_pair
                case Collision.SAMPLE:
                    dt = (T[2] - t)
                    Xs += dt * Vs
                    X_all_disks[i,:] = Xs[:,0]
                    _,m_disks = V_all_disks.shape
                    for j in range(m_disks):
                        Vx_all_disks[i,j] = Vs[j,0]
                        V_all_disks[i,j] = np.sqrt(sum([Vs[j,k]**2 for k in range(d)]))
                    sampled = True

    n,bins = np.histogram(X_all_disks,bins=bins)
    if args.restart == None:
        counts = n
    else:
        counts += n

    nvx,binsvx = np.histogram(Vx_all_disks,bins=binsvx)

    if args.restart == None:
        countsvx = nvx
    else:
        countsvx += nvx

    nv,binsv = np.histogram(V_all_disks,bins=binsv)
    if args.restart == None:
        countsv = nv
    else:
        countsv += nv

    save_file = get_file_name(args.out,default_ext='npz')
    if exists(save_file):
        backup_file = save_file + '~'
        replace(save_file,backup_file)

    np.savez(save_file,
             Xs=Xs,Vs=Vs,counts=counts,bins=bins,countsvx=countsvx,binsvx=binsvx,countsv=countsv,binsv=binsv,L=L,sigma=sigma,DeltaT=DeltaT)

    Disks,_ = Xs.shape

    fig1 = figure(figsize=(12,12))
    fig1.suptitle(fr'{args.n} Disks, '
                  fr'{counts.sum()//Disks:,} Epochs, '
                  fr'$\sigma=${args.sigma:.3g}, ')

    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot(0.5*(bins[0:-1]+bins[1:]),counts/counts.sum())
    ax1.axvline(x=args.sigma,color='red',linestyle='dashed')
    ax1.axvline(x=L[0]-args.sigma,color='red',linestyle='dashed')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Positions')

    fig1.savefig(get_file_name(args.out,seq='X'))

    fig2 = figure(figsize=(12,12))
    fig2.suptitle(fr'{args.n} Disks, '
                  fr'{counts.sum()//Disks:,} Epochs, '
                  fr'$\sigma=${args.sigma:.3g}, ')
    ax2 = fig2.add_subplot(1,1,1)
    ax2.plot(0.5*(binsvx[0:-1]+binsvx[1:]),countsvx/countsvx.sum(),label='$V_x$')
    ax2.plot(0.5*(binsv[0:-1]+binsv[1:]),countsv/countsv.sum(),label='V')
    ax2.set_xlabel('V')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Velocities')
    ax2.legend()

    fig2.savefig(get_file_name(args.out,seq='V'))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
