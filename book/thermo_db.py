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

''' Exercise 5-11: calculate thermodynamic quantities'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from sys import exit
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show
from matplotlib.patches import Patch
from ising_db import IsingDatabase
from cluster_ising import IsingData

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-i', '--input', default = basename(splitext(__file__)[0]),help='Name of input file')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('-m', type = int, default = None, help = 'Number of rows')
    parser.add_argument('-n', type = int, default = None, help = 'Number of columns')
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

def thermo(E,N,beta=1,NObservations=36):
    Emean = np.average(E,weights=N)
    e = Emean/NObservations
    cV = beta**2 * np.average((E-Emean)**2,weights=N)/NObservations
    return e, cV

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    Ts = []
    es = []
    cVs = []
    database = IsingDatabase(args.input)
    lines = ['T,e,\t$c_V$']
    for T,m,n in database.generate_keys():
        if args.m != None and m != args.m: continue
        if args.n != None and n != args.m: continue
        NIterations,s,N,_ = database[T,m,n]
        e,cV = thermo(N[:,0],N[:,1],beta=1/T,NObservations=m*n)
        Ts.append(T)
        es.append(e)
        cVs.append(cV)
        lines.append(f'{T:.1f},\t{e:.3f},\t{cV:.5f}')

    if len(Ts) == 0:
        print ('No data')
        exit(0)

    fig = figure(figsize=(12,12))
    ax = fig.add_subplot(1,1,1)
    plt1 = ax.plot(Ts,es,color='blue',label='e')
    ax.set_xlabel('T')
    ax.set_ylabel('e')
    axt = ax.twinx()
    plt2 = axt.plot(Ts,cVs,color='red',label=r'$c_V$')
    axt.set_ylabel(r'$c_V$')
    lns = plt1 + plt2
    ax.legend(lns, [l.get_label() for l in lns], loc='upper left')
    axt.legend([Patch(color='white')]*len(lines),  lines,loc='center left')
    ax.set_title(fr'{m}$\times${n} Grid, after {NIterations} Iterations')
    fig.savefig(get_file_name(args.out))

    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
