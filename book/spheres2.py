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

'''Sinai's system of two large sphere in a box'''

from argparse          import ArgumentParser
from math              import sqrt
from matplotlib        import rc
from matplotlib.pyplot import figure, plot, savefig,show
from numpy             import argmin
from os.path           import basename, splitext
from random            import random, seed

class HardDisk:
    '''Keeps track of position and velocity of disk'''
    def __init__(self,x,y,u,v):
        self.x = x
        self.y = y
        self.u = u
        self.v = v

class Collision:
    '''Compute time to next collision of spheres and consequnces of collision'''
    def __init__(self,L,sigma,V):
        self.L     = L
        self.sigma = sigma
        self.a     = V**2

    def get_delta(self,disk):
        b     = disk.x * disk.v + disk.y * disk.u
        c     = disk.x**2 + disk.y**2 - self.sigma**2
        delta = b**2 - self.a *c
        if delta>0 and b<0:
            return (-b - sqrt(delta))/self.a
        return float('inf')

    def exec(self,disk,dt,sample):
        # TODO
        sample.synchronize(dt)

class Wrap:
    '''Compute time to next collision with and consequnces of collision'''
    def __init__(self,L):
        self.L = L

    def get_delta(self,disk):
        Deltas = [self.get_one_delta(disk.x,disk.u),
                  self.get_one_delta(disk.y,disk.v)]
        self.axis = argmin(Deltas)
        return Deltas[self.axis]

    def exec(self,disk,dt,sample):
        if self.axis==0:
            disk.x += dt * disk.u
            disk.x *= -1
        else:
            disk.y += dt * disk.v
            disk.y *= -1
        sample.synchronize(dt)

    def get_one_delta(self,x,u):
        if x*u > 0:
            return (self.L-abs(x))/abs(u)
        else:
            return (self.L+abs(x))/abs(u)

class Sample:
    '''Keep track of Time, and sample state at regular intervals. '''
    def __init__(self,N,dt):
        self.N      = N
        self.n      = 0
        self.dt     = dt
        self.t_acc  = 0
        self.xs     = []
        self.ys     = []

    def get_delta(self,disk):
        '''Calculate time to next sample'''
        return self.dt - self.t_acc

    def exec(self,disk,dt,sample):
        print (self.n)
        self.xs.append(disk.x)
        self.ys.append(disk.y)
        self.t_acc  = 0

    def should_continue(self):
        self.n += 1
        return self.n<self.N

    def synchronize(self,dt):
        '''Accumulkate time from Collisions and Wraps'''
        self.t_acc += dt

def create_disk(L,V):
    x,y = 0,0
    while x**2+y**2 < args.sigma**2:
        x= L * ( 2*random()-1)
        y =L * ( 2*random()-1)

    u = 2*random()-1
    v = 2*random()-1
    norm = sqrt(u**2 + v**2)
    return HardDisk(x, y, u*V/norm, v*V/norm)

def get_next_event(collision, wrap, sample,disk):
    events = [collision, wrap, sample]
    while True:
        dts    = [event.get_delta(disk) for event in events]
        index  = argmin(dts)
        yield events[index],dts[index]
        if not sample.should_continue(): break

def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('--L',
                        type    = float,
                        default = 1.0)
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.365)
    parser.add_argument('--N',
                        type    = int,
                        default = 100)
    parser.add_argument('--seed',
                        type    = int,
                        default = None)
    parser.add_argument('--dt',
                        type    = float,
                        default = 0.1)
    parser.add_argument('--V',
                        type    = float,
                        default = 1.0)
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    return parser.parse_args()

if __name__=='__main__':
    args = parse_arguments()

    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)

    seed(args.seed)

    disk   = create_disk(args.L, args.V)
    sample = Sample(args.N,args.dt)
    for event,dt in get_next_event(collision = Collision(args.L,args.sigma,args.V),
                                   wrap      = Wrap(args.L),
                                   sample    = sample,
                                   disk      = disk):
        event.exec(disk,dt,sample)

    # figure(figsize=(12,12))
    # plot([1,2,3])
    # savefig(get_plot_file_name(args.plot))
    # if args.show:
        # show()
