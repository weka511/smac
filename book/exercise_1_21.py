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

def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    parser.add_argument('--zeta', type=float, default=-0.25)
    parser.add_argument('--delta', type=float,
                        default=[
                            0.0000625, 0.000125, 0.00025, 0.0005,
                            0.000625, 0.00125, 0.0025, 0.005,
                            0.0125, 0.025, 0.05, 0.125,
                            0.25, 0.3125, 0.375, 0.4375,
                            0.5],
                        nargs='+')
    parser.add_argument('--length', type=float, default=1.0)
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

    Rejection_rate = np.zeros_like(args.delta)
    Means = np.zeros_like(args.delta)
    Stds = np.zeros_like(args.delta)

    for i in range(len(args.delta)):
        N = int(args.length/args.delta[i])+1
        X = np.zeros((N))
        X[0] = 1
        number_accepted = 0
        for j in range(1,N):
            X[j], accepted = markov_zeta(X[j-1],delta=args.delta[i],zeta=args.zeta,rng=rng)
            if accepted:
                number_accepted += 1
        Rejection_rate[i] = 1 - number_accepted/(N-1)
        Means[i] = X.mean()
        Stds[i] = X.std()

    fig = figure(figsize=(12,12))
    fig.suptitle(r'$\zeta=$'f'{args.zeta}')

    ax1 = fig.add_subplot(2,1,1)
    plot1a = ax1.plot(args.delta,Rejection_rate,color='red',label='Rejection')
    ax1.set_xlabel(r'$\delta$')
    ax1.set_ylabel(r'$Rejection\ rate$')
    ax1a = ax1.twinx()
    plot1b = ax1a.plot(args.delta,Means,label=r'$\mu$',color='blue')
    plot1c =  ax1a.plot(args.delta,Stds,label=r'$\sigma$',color='green')
    plots = plot1a + plot1b + plot1c
    labels = [p.get_label() for p in plots]
    ax1.legend(plots,labels,loc='center left')

    ax2 = fig.add_subplot(2,1,2)
    ax2.scatter(Rejection_rate,Stds,label='Std',color='green')
    ax2.set_ylabel(r'$\sigma$')
    ax2.set_xlabel(r'$Rejection\ rate$')
    ax2.set_title('Variance vs. rejection rate.')
    fig.tight_layout(h_pad=3)
    fig.savefig(get_file_name(args.out))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
