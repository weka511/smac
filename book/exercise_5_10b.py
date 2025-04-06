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
    Exercise 5.10  Plot M against T
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
    parser.add_argument('-m', type = int, default = 4, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = 4, help = 'Number of columns')
    parser.add_argument('--Nsteps', type = int, default = 10000, help = 'Number of steps')
    parser.add_argument('--Nburn', type = int, default = 0, help = 'Number of steps for burn in')
    parser.add_argument('--Niterations', type = int, default = 5, help = 'Number of iterations of Markov chain')
    parser.add_argument('-f', '--frequency',type = int, default = 0, help = 'How often to report progress')
    parser.add_argument('-T', '--T', default=[1000], nargs='+', type=float, help = 'Range for temperature: [start, ]stop, [step, ]')
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', default=False, action = 'store_true', help = 'Show plot')
    return parser.parse_args()

def get_range(T,deltaT=0.1):
    '''
    Used to convert temperature (specified in args) to a range

    Parameters:
        T       [start, ]stop, [step, ]
    '''
    match (len(T)):
        case 1:
            return T
        case 2:
            return np.arange(T[0],T[1],deltaT)
        case 3:
            return np.arange(T[0],T[1]+T[2],T[2])

    raise ValueError(f'Parameter T must have length of 1,2, or 3')

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

def get_boundary_conditions(periodic):
    '''
    Used to format suptitle
    '''
    return 'Periodic boundary conditions' if periodic else 'Bounded'

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    rng = np.random.default_rng(args.seed)
    T_range = get_range(args.T)
    fig = figure(figsize=(12,12))
    fig.suptitle(fr'{get_boundary_conditions(args.periodic)} , ' +
                 fr'{args.m}$\times${args.n} sites, {args.Niterations} iterations $\times$ {args.Nsteps} steps')

    ax = fig.add_subplot(1,1,1)
    for j,T in enumerate(T_range):
        markov = MarkovIsing(rng=rng,
                             shape=(args.m,args.n),
                             periodic=args.periodic,
                             Niterations=args.Niterations,
                             beta=1/T)
        accepted = 0
        for i in range(args.Niterations):
            markov.run(Nsteps=args.Nsteps,Nburn=args.Nburn,frequency=args.frequency,iteration=i)
            accepted += markov.accepted_moves

        Es,means, stds,M,magnetization = markov.get_stats()
        ax.bar(M,magnetization,width=0.8,label=fr'T={T}, accepted={100*accepted/(args.Niterations*args.Nsteps):.1f}\%')
        ax.set_xlabel('$M$')
        ax.set_ylabel('Magnetization')
        ax.set_title('Magnetization')
        ax.legend(loc='upper left')

        fig.tight_layout(h_pad=4,pad=2)
        fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()

