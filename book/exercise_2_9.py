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
   parser.add_argument('-M','--M', type=int, default=1000000,help='Number of iterations')
   parser.add_argument('-N','--N', type=int, default=16,help='Number of spheres')
   parser.add_argument('--bins', default='sqrt', type=get_bins, help = 'Binning strategy or number of bins')
   parser.add_argument('--L', type = float, nargs   = '+', default = [1,1], help='Lengths of walls')
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


def direct_disks_any(N,L=np.array([1,1]), rng = np.random.default_rng()):
   '''
   Algorithm 2-8: compute the acceptance rate of Algorithm 2-7,
   direct-disks, in a rectangular box.

   Parameters:
      N         Number of disks
      L         Array of lenghts of sides for box
      rng       Random number generator
   '''
   def get_sigma2(pts):
      '''
      Get minimum distance between points

      Parameters:
          pts    The array of points
      '''
      sigma2 = float('inf')
      for i in range(N):
         for j in range(i+1,N):
            sigma2 = min(sigma2,np.linalg.norm(pts[i,:]-pts[j,:]))
      return sigma2

   sigma = 0.5 * get_sigma2(L * rng.random((N,2)))
   return np.pi * sigma**2 * N / (L[0]*L[1])

def get_bins(bins):
   '''
   Used to parse args.bins: either a number of bins, or the name of a binning strategy.
   '''
   try:
      return int(bins)
   except ValueError:
      if bins in ['auto', 'fd', 'doane', 'scott', 'sturges', 'sqrt', 'stone', 'rice']:
         return bins
      raise ArgumentTypeError(f'Invalid binning strategy "{bins}"')

if __name__=='__main__':
   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   start  = time()
   args = parse_arguments()
   rng = np.random.default_rng(args.seed)

   etas = np.fromfunction(np.vectorize(lambda x:direct_disks_any(args.N,np.array(args.L),rng=rng)),(args.M,))
   n,bins = np.histogram(etas,bins=args.bins,density=True)
   centres = 0.5 *(bins[1:] + bins[:-1])

   fig = figure(figsize=(12,12))
   ax1 = fig.add_subplot(1,1,1)
   ax1.plot(centres,1-np.cumsum(n/n.sum()),label=r'$\pi(\eta_{max})$')
   ax1.plot(centres,np.exp(-2*(args.N-1)*centres),label=r'$\exp(-2(N-1)\eta)$')
   ax1.set_yscale('log')
   ax1.legend()
   ax1.set_xlabel(r'$\eta$')
   ax1.set_ylabel(r'$P_{accept}(\eta)$')
   ax1.set_title(f'Acceptance rate for {args.N} disks, after {args.M} iterations')
   fig.savefig(get_file_name(args.out))
   elapsed = time() - start
   minutes = int(elapsed/60)
   seconds = elapsed - 60*minutes
   print (f'Elapsed Time {minutes} m {seconds:.2f} s')

   if args.show:
      show()
