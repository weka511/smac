#!/usr/bin/env python

#   Copyright (C) 2024-2025 Simon Crase

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
    Exercise 5.10 Implement Local Metropolis algorithm and test it against the specific heat capacity.
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from markov_ising import MarkovIsing

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--periodic', default=False, action = 'store_true', help = 'Use periodic boundary conditions')
    parser.add_argument('--lowest', default=False, action = 'store_true', help = 'Initialize to all spins down at the start of each run')
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('--Nburn', type = int, default = 0, help = 'Number of steps for burn in')
    parser.add_argument('--Niterations', type = int, default = 5, help = 'Number of iterations of Markov chain')
    parser.add_argument('-f', '--frequency',type = int, default = 100, help = 'How often to report progress')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('-T', '--T', type=float, default=2.0,help='Temperature')
    return parser.parse_args()


def get_file_name(args,default_ext='.png',seq=None):
    '''
    Used to create file names

    Parameters:
        args
        default_ext
        seq
    '''
    base,ext = splitext(args.out)
    if len(ext) == 0:
        ext = default_ext
    if seq != None:
        base = f'{base}{seq}'
    return join(args.figs,f'{base}{ext}')

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    NObservations = args.m*args.n
    beta = 1/args.T

    markov = MarkovIsing(rng = np.random.default_rng(args.seed),
                         shape=(args.m,args.n),periodic=args.periodic,
                         Niterations=args.Niterations,beta=beta)
    e = np.zeros((args.Niterations))
    cV = np.zeros((args.Niterations))
    for i in range(args.Niterations):
        markov.run(Nsteps=args.Nsteps,Nburn=args.Nburn,frequency=args.frequency,iteration=i,lowest=args.lowest)
        E, N = markov.data.get_data(iteration=i)
        Emean = np.average(E,weights=N)
        e[i] = Emean/NObservations
        cV[i] = beta**2 * np.average((E-Emean)**2,weights=N)/NObservations
        print (f'e={e[i]:.03f},cV={cV[i]:.05f}')
    print (f'e: {e.mean():.03f} {e.std():.03g}')
    print (f'cV: {cV.mean():.05f} {cV.std():.03g}')
    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(2,1,1)
    ax.bar(E,N)
    ax.set_title(fr'$\beta=${beta}')

    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(e,label='e',color='blue')
    ax2.legend(loc='upper left')
    ax2t = ax2.twinx()
    ax2t.plot(cV,label='$c_V$',color='red')
    ax2t.legend(loc='upper right')

    fig.savefig(get_file_name(args))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
