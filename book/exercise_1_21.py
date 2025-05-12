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
    Exercise 1.21 Determine the mean value of x**(gamma-zeta) in
    a simple implementation of Algorithm 1.31 (markov-zeta)
'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def markov_zeta(x,delta = 0.005,zeta = -0.25,rng=np.random.default_rng()):
    '''
    Algorithm 1.31 Markov-chain Monto Carlo algorithm for a point x on the interval [0,1]
    with probability proportional to x**zeta

    Returns:
        x_bar, True    If next step accepted
        x, False       If rejected
    '''
    x_bar = x + 2*delta*rng.random() - delta
    if 0 < x_bar and x_bar < 1:
        p_accept = (x_bar/x)**zeta
        if rng.random() < p_accept:
            return x_bar,True
    return x,False

def direct_gamma_zeta(gamma,zeta,n, delta = 0.005,rng=np.random.default_rng()):
    def get_positive_sample():
        while True:
            x = rng.random()
            if x > 0: return x

    x = get_positive_sample()
    sigma = 0
    sigma2 = 0
    n_accepted = 0
    for i in range(n):
        x,accepted = markov_zeta(x,delta = delta,zeta = zeta,rng=rng)
        x2 = x**(gamma - zeta)
        sigma += x2
        sigma2 += x2**2
        if accepted:
            n_accepted += 1

    mean = sigma/n
    return (mean,np.sqrt(sigma2/n-mean*mean)/np.sqrt(n),n_accepted/n)


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--zeta', type=float, default=-0.25)
    parser.add_argument('--gamma', type=float, default=-0.8)
    parser.add_argument('--N',type=int,default=1000)
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

if __name__=='__main__':
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    start  = time()
    args = parse_arguments()
    rng = np.random.default_rng(args.seed)
    Results = np.zeros((3,args.N))
    for n in range(2,args.N):
        Results[0,n], Results[1,n],Results[2,n] = direct_gamma_zeta(args.gamma,args.zeta,n, delta = 1/n,rng=rng)

    fig = figure(figsize=(12,12))
    fig.suptitle(r'$\zeta=$'f'{args.zeta}'r'$,\gamma=$'f'{args.gamma}'r',$N=$'f'{args.N}')
    ax1 = fig.add_subplot(2,1,1)
    plot1 = ax1.plot(Results[0,5:],label='Mean',color='blue')
    plot2 = ax1.plot(Results[1,5:],label='Var',color='green')
    plot3 = ax1.axhline(1/(args.gamma+1),label='Ground Truth',color='magenta')
    plot1a = ax1.twinx().plot(Results[2,5:],label='Acceptance',color='red')
    plots = plot1 + plot2 + plot1a
    ax1.legend(plots,[p.get_label() for p in plots])

    ax2 = fig.add_subplot(2,1,2)
    ax2.scatter(Results[2,2:],Results[0,2:]-1/(args.gamma+1),color='magenta')
    ax2.set_xlabel('Acceptance')
    ax2.set_ylabel('Error')
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
