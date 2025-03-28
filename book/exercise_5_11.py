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

'''Exercise 5-11/Algorithm 5-9-cluster ising'''

from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show


def parse_arguments():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
    parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
    parser.add_argument('--figs', default = './figs')
    parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
    return parser.parse_args()

class ClusterIsing:
    def __init__(self,Nbr=Nbr,rng=np.random.default_rng(),shape=(4,5),periodic=False,Niterations=5,beta=0.001):
        self.Nbr = lambda k:Nbr(k,shape=shape,periodic=periodic)
        self.rng = rng
        self.m = shape[0]
        self.n = shape[1]
        self.N = self.m*self.n
        self.periodic = periodic
        self.beta = beta
        self.p  = 1.0 - np.exp(-2.0*beta)
        # self.data = IsingData(Niterations=Niterations,N=self.N)
        # self.weights = Weights(beta,get_max_neigbbours(shape))

    def step(self,sigma):
        j = self.rng.integers(self.N)
        Pocket, Cluster = [j], [j]
        while Pocket != []:
            k = self.rng.choice(Pocket)
            for l in nbr[k]:
                if sigma[l] == sigma[k] and l not in Cluster and self.rng.uniform() < self.p:
                    Pocket.append(l)
                    Cluster.append(l)
            Pocket.remove(j)
        for k in Cluster:
            sigma[k] *= -1

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
    rng = np.random.default_rng(args.seed)
    fig = figure(figsize=(12,12))

    fig.savefig(get_file_name(args))
    elapsed = time() - start
    minutes = int(elapsed/60)
    seconds = elapsed - 60*minutes
    print (f'Elapsed Time {minutes} m {seconds:.2f} s')

    if args.show:
        show()
