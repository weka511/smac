#!/usr/bin/env python

# Copyright (C) 2015 Greenweaves Software Pty Ltd

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

'''
   Exercise 2.9: implement Algorithm 2.8, direct-disks-any,
   in order to determine the acceptance rate of algorithm 2.7, direct-disks.
'''
from argparse import ArgumentParser
from os.path import basename, join, splitext
from time import time
import numpy as np
from matplotlib import rc
from matplotlib.pyplot import figure, show

def parse_arguments():
   '''Parse command line arguments'''
   parser = ArgumentParser(__doc__)
   parser.add_argument('--seed',type=int,default=None,help='Seed for random number generator')
   parser.add_argument('-o', '--out', default = basename(splitext(__file__)[0]),help='Name of output file')
   parser.add_argument('--figs', default = './figs', help = 'Name of folder where plots are to be stored')
   parser.add_argument('--show', action = 'store_true', help   = 'Show plot')
   parser.add_argument('-N','--N', type=int, default=1000,help='Number of iterations')
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



def distance(z1,z2):
   return (z1[0]-z2[0])*(z1[0]-z2[0])+(z1[1]-z2[1])*(z1[1]-z2[1])

def direct_disks_any(n,l_x,l_y, rng = np.random.default_rng()):
   '''Algoritm 2-8'''
   def get_sigma2():
      sigma2 = float('inf')
      for i in range(n):
         for j in range(i+1,n):
            sigma2 = min(sigma2,np.linalg.norm(pts[i,:]-pts[j,:]))
      return sigma2
   pts = np.array([l_x,l_y]) * rng.random((n,2))
   sigma = 0.5 * get_sigma2()
   return np.pi*(sigma**2)*n/(l_x*l_y)

if __name__=='__main__':
   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   start  = time()
   args = parse_arguments()
   rng = np.random.default_rng(args.seed)

   etas = np.empty((args.N))

   for i in range(args.N):
      etas[i] = direct_disks_any(16,1,1,rng=rng)

   fig = figure(figsize=(12,12))
   ax = fig.add_subplot(1,1,1)
   ax.hist(etas,'sqrt')

   fig.savefig(get_file_name(args.out))
   elapsed = time() - start
   minutes = int(elapsed/60)
   seconds = elapsed - 60*minutes
   print (f'Elapsed Time {minutes} m {seconds:.2f} s')

   if args.show:
      show()
