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

'''Exercise 2-4. Sinai's system of two large sphere in a box. Show histogram of positions.'''

from argparse          import ArgumentParser
from math              import sqrt
from matplotlib        import rc
from matplotlib.pyplot import axis, colorbar, figure, grid, hist, hist2d, savefig, show, subplot, suptitle, title, xlabel, ylabel
from numpy             import allclose, argmin, linspace, pi
from os.path           import basename, splitext
from random            import random, seed

class HardDisk:
    '''Keeps track of position and velocity of disk'''
    def __init__(self,x,y,u,v,sigma):
        self.x     = x
        self.y     = y
        self.u     = u
        self.v     = v
        self.sigma = sigma

    def move(self,dt):
        '''Update position, assuming constant velocity for time dt'''
        self.x += self.u * dt
        self.y += self.v * dt

    def get_direction_cosines(self):
        '''Find direction of centre, ralative to origin'''
        radius = sqrt(self.x**2 + self.y**2)
        assert allclose(2*self.sigma, radius,
                        rtol = 1e-5,
                        atol = 0),f'{2*self.sigma} {radius}'
        return self.x/radius, self.y/radius

class Collision:
    '''Compute time to next collision of spheres and consequnces of collision'''
    def __init__(self,L,sigma,V):
        self.L     = L
        self.sigma = sigma
        self.a     = V**2

    def get_delta(self,disk):
        '''Compute time to next collision of spheres'''
        b     = disk.x * disk.u + disk.y * disk.v
        c     = disk.x**2 + disk.y**2 - 4*self.sigma**2
        delta = b**2 - self.a *c
        if delta>0 and b<0:
            return (-b - sqrt(delta))/self.a
        return float('inf')

    '''Collide spheres. We need to reverse the radial component of velocity, while preserving theta component.'''
    def exec(self,disk,dt,sample):
        disk.move(dt)
        x, y     = disk.get_direction_cosines()
        assert allclose(1,x**2 + y**2,
                        rtol = 1e-5,
                        atol = 0),f'{1} not = {x**2 + y**2}'
        v_r      =   x * disk.u + y * disk.v
        v_theta  = - y * disk.u + x * disk.v
        v_r     *= -1
        disk.v   = v_theta * x + v_r * y
        disk.u   = v_r * x     - v_theta * y
        assert allclose(self.a, disk.u**2+disk.v**2,
                        rtol = 1e-5,
                        atol = 0),f'{self.a} not = {disk.u**2+disk.v**2}'
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
    return HardDisk(x, y, u*V/norm, v*V/norm,sigma)

def get_next_event(collision, wrap, sample, disk):
    '''
       Generator that handles evolution in time. Repeatedly determine which type of event will happen next,
       and when it will occur (relative to current time).
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
                        default = 1.0,
                        help    = 'Half length of box')
    parser.add_argument('--sigma',
                        type    = float,
                        default = 0.365,
                        help    = 'Radius of sphere')
    parser.add_argument('--N',
                        type    = int,
                        default = 1000000,
                        help    = 'Number of steps to evolve configuration')
    parser.add_argument('--m',
                        type    = int,
                        default = 100,
                        help    = 'Number of bins for histogram')
    parser.add_argument('--seed',
                        type    = int,
                        default = None,
                        help    = 'Seed for random number generator')
    parser.add_argument('--dt',
                        type    = float,
                        default = 0.1,
                        help    = 'Time step for sampling')
    parser.add_argument('--V',
                        type    = float,
                        default = 1.0,
                        help    = 'Magnitude of velocity')
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    return parser.parse_args()

def flatten(Xss):
    '''Convert a list of lists into a single list'''
    return [x for Xs in Xss for x in Xs]

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
    figure(figsize=(12,6))
    suptitle('Sinai two-disk system')

    # Plot 2d histogram showing time spent at each position

    subplot(1,2,1)
    axis('scaled')
    h,_,_,_ = hist2d(sample.xs, sample.ys,
                     bins    = [bins,bins],
                     density = True)
    colorbar()
    title(fr'L={args.L}, $\sigma=${args.sigma}, N={args.N:,d}, dt={args.dt}, V={args.V}')
    xlabel('X')
    ylabel('Y')

    # Show distribution of frequencies

    subplot(1,2,2)
    hist (flatten(h),
          density = True,
          color = 'xkcd:blue')
    title(fr'Projected Densities $\eta=${pi*args.sigma**2/(4*args.L**2):.3f}')
    xlabel('Density')
    ylabel('Frequency')
    grid(True)

    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
