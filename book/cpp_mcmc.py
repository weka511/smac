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

''' Script to plot output from C++ MCMC '''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from re import compile
from thermo_db import thermo

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('-i', '--input', default = 'markov-out.txt',help='Name of input file')
    parser.add_argument('-p', '--path', default = r'C:\cygwin64\home\Weka\smac\book\ising',help='path to input file')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()


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

def read_file(path,input):
    '''
    Parse the input file, which looks like this:
    m=6,n=6,periodic=1,beta=0.25,nruns=100
    beta=0.25, total_accepted=60505342, max_steps=100000000
    beta=0.25, total_accepted=60525654, max_steps=100000000
    beta=0.25, total_accepted=60537572, max_steps=100000000
    [i.e. one row for each run]
    ...
    E,N
    -132,0,0,0,0,0,0,0,0,0,0,16918,0,0,0,0,0,0,0,0,0,0,...
    -124,0,0,0,0,0,0,0,0,0,0,84486,0,0,0,0,0,0,0,0,0,...
    [i.e. one row for each value of E, one column for the count for each run]
    ...
    M,N
    -36,9640,9179,9289,9145,8726,9205,8737,8654,8256,8384,...
    -34,44917,43339,43676,42605,42257,44013,43288,42349,42239,...
    ...
    '''
    state = 0
    max_steps = 0
    pattern_parameters = compile(r'm=(\d+),n=(\d+),periodic=(\d),beta=([0-9.]+),nruns=(\d+)')
    pattern_accepted = compile(r'beta=([0-9.]*), total_accepted=(\d+), max_steps=(\d+)')

    with open(join(path,input)) as input_file:
        for line in input_file:
            line = line.strip()
            match (state):
                case 0:
                    match = pattern_parameters.match(line)
                    m = int(match.group(1))
                    n = int(match.group(2))
                    periodic = int(match.group(3)) == 1
                    beta = float(match.group(4))
                    nruns = int(match.group(5))
                    state = 1
                    accepted = []

                case 1:
                    match = pattern_accepted.match(line)
                    if match:
                        accepted.append(int(match.group(2)))
                        max_steps = int(match.group(3))
                    else:
                        state = 2
                    Es = []
                    Ms = []

                case 2:
                    try:
                        Es.append([int(x) for x in line.split(',')])
                    except ValueError:
                        state = 3

                case 3:
                    parts = line.split(',')
                    try:
                        Ms.append([int(x) for x in line.split(',')])
                    except ValueError:
                        pass

    return m,n,periodic,beta,np.array(Es),np.array(Ms),np.array(accepted),max_steps

def get_periodic(is_periodic):
    '''
    Used for suptitle
    '''
    return 'periodic' if is_periodic  else 'aperiodic'

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()

    m,n,is_periodic,beta,E,M,accept,max_steps = read_file(args.path,args.input)
    e,cV =thermo(E[:,0],np.sum(E[:,1:],axis=1),beta=beta,NObservations=m*n)
    acceptance_ratio = accept/max_steps
    Emean =np.average(E[:,1:],axis=1)
    Estd = np.std(E[:,1:],axis=1)
    Mmean =np.average(M[:,1:],axis=1)
    Mstd = np.std(M[:,1:],axis=1)

    fig = figure(figsize=(12,12))
    fig.suptitle(fr'{args.input}: {len(accept)}$\times${max_steps:,} steps, {m}$\times${n}, {get_periodic(is_periodic)}, $\beta=${beta},' )
    ax1 = fig.add_subplot(2,1,1)

    ax1.bar(E[:,0],Emean + Estd,label=r'$\mu+\sigma$')
    ax1.bar(E[:,0],Emean,label=r'$\mu$')
    ax1.bar(E[:,0],Emean - Estd,label=r'$\mu-\sigma$')
    ax1.legend()
    ax1.set_title(fr'Acceptance ratio={acceptance_ratio.mean():.3}$\pm${acceptance_ratio.std():.3}, e={e:.3f},$c_V=${cV:.5f}')
    ax1.set_xlabel('E')
    ax1.set_ylabel('Frequency')
    ax1.set_ylim(0)

    ax2 = fig.add_subplot(2,1,2)
    ax2.bar(M[:,0],Mmean + Mstd,label=r'$\mu+\sigma$')
    ax2.bar(M[:,0],Mmean,label=r'$\mu$')
    ax2.bar(M[:,0],Mmean - Mstd,label=r'$\mu-\sigma$')
    ax2.legend()
    ax2.set_xlabel('M')
    ax2.set_ylabel('Frequency')

    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
