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

'''Exercose 2-4. Sinai's system of two large sphere in a box. Show histogram of positions'''

from argparse          import ArgumentParser
from math              import sqrt
from matplotlib        import rc
from matplotlib.pyplot import colorbar, figure, hist2d, savefig, show, title
from numpy             import argmin, linspace
from os.path           import basename, splitext
from random            import random, seed

class HardDisk:
    '''Keeps track of position and velocity of disk'''
    def __init__(self,x,y,u,v):
        self.x = x
        self.y = y
        self.u = u
        self.v = v

    def move(self,dt):
        self.x += self.u * dt
        self.y += self.v * dt

    def get_norm(self):
        return sqrt(self.x**2 + self.y**2)

class Collision:
    '''Compute time to next collision of spheres and consequnces of collision'''
    def __init__(self,L,sigma,V):
        self.L     = L
        self.sigma = sigma
        self.a     = V**2

    def get_delta(self,disk):
        '''Compute time to next collision of spheres'''
        b     = disk.x * disk.v + disk.y * disk.u
        c     = disk.x**2 + disk.y**2 - self.sigma**2
        delta = b**2 - self.a *c
        if delta>0 and b<0:
            return (-b - sqrt(delta))/self.a
        return float('inf')

    '''Collide spheres. We need to reverse the radial component of velocity, while preserving theta component.'''
    def exec(self,disk,dt,sample):
        disk.move(dt)
        norm     = disk.get_norm()
        x        = disk.x/norm
        y        = disk.y/norm
        v_r      =   x * disk.u + y * disk.v
        v_theta  = - y * disk.u + x * disk.v
        v_theta -= 1
        disk.v   = v_theta * x + v_r * y
        disk.u   = v_r * x     - v_theta * y
        sample.synchronize(dt)

class Wrap:
    '''Compute time to next collision with Wall and consequnces of collision'''
    def __init__(self,L):
        self.L = L

    def get_delta(self,disk):
        '''
           Compute time to next collision with Wall.
           Store the number of the wall that gives next collision
        '''
        Deltas    = [self.get_one_delta(disk.x,disk.u),
                    self.get_one_delta(disk.y,disk.v)]
        self.axis = argmin(Deltas)
        return Deltas[self.axis]

    def exec(self,disk,dt,sample):
        '''Move disk to wall, and wrap position around.'''
        disk.move(dt)
        if self.axis==0:
            disk.x *= -1
        else:
            disk.y *= -1
        sample.synchronize(dt)

    def get_one_delta(self,x,u):
        '''Compute time to next collision with specified Wall'''
        if x*u > 0:
            return (self.L-abs(x))/abs(u)
        else:
            return (self.L+abs(x))/abs(u)

class Sample:
    '''Keep track of Time, and sample state at regular intervals. '''
    def __init__(self,N,dt):
        self.N      = N
        self.n      = -1
        self.dt     = dt
        self.t_acc  = 0
        self.xs     = []
        self.ys     = []

    def get_delta(self,disk):
        '''Calculate time to next sample'''
        return self.dt - self.t_acc

    def exec(self,disk,dt,sample):
        '''Sample position'''
        disk.move(dt)
        self.xs.append(disk.x)
        self.ys.append(disk.y)
        self.t_acc  = 0

    def should_continue(self):
        '''Are we there yet?'''
        self.n += 1
        return self.n<self.N

    def synchronize(self,dt):
        '''Accumulate time from Collisions and Wraps'''
        self.t_acc += dt

def create_disk(L,V,sigma):
    '''
       Set up one disk that is in a valid position, i.e. outside reference disk,
       but otherwise has a random position and direction.

       Parameters:
         L     Half length of box
         V     Magnitude of velocity
         sigma Radius of sphere
    '''
    x,y = 0,0
    while x**2 + y**2 < sigma**2:
        x = L * (2 * random()-1)
        y = L * (2 * random()-1)

    u    = 2*random()-1
    v    = 2*random()-1
    norm = sqrt(u**2 + v**2)
    return HardDisk(x, y, u*V/norm, v*V/norm)

def get_next_event(collision, wrap, sample, disk):
    '''
       Generator that handles evolution in time. Repeatedly determine which type of event will happen next,
       then perform event.
    '''
    events = [collision, wrap, sample]
    while sample.should_continue():
        next_event_times = [event.get_delta(disk) for event in events]
        first_index      = argmin(next_event_times)
        yield events[first_index],next_event_times[first_index]

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
    parser.add_argument('--m',
                        type    = int,
                        default = 10)
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
    seed(args.seed)
    disk   = create_disk(args.L, args.V, args.sigma)
    sample = Sample(args.N,args.dt)
    for event,dt in get_next_event(collision = Collision(args.L,args.sigma,args.V),
                                   wrap      = Wrap(args.L),
                                   sample    = sample,
                                   disk      = disk):
        event.exec(disk,dt,sample)

    bins = linspace(-args.L, args.L,
                    num = args.m)
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize=(12,12))
    hist2d(sample.xs, sample.ys,bins=[bins,bins])
    colorbar()
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
