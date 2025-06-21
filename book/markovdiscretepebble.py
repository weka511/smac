#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Pty Ltd

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
   Algorithm 1.6: discrete Markov Chain Monte Carlo for the pebble game
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
   parser.add_argument('--m', default=51,type=int)
   parser.add_argument('--n', default=91,type=int)
   parser.add_argument('--M', default=7,type=int)
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

# Table 1.3 (0-8 instead of 1-9)

neighbour_table =np.array([
    [ 1,  3, -1, -1],
    [ 2,  4,  0, -1],
    [-1,  5,  1, -1],
    [ 4,  6, -1,  0],
    [ 5,  7,  3,  1],
    [-1,  8,  4,  2],
    [ 7, -1, -1,  3],
    [ 8, -1,  6,  4],
    [-1, -1,  7,  5]
])




def markov_discrete_pebble(k,table,rng=np.random.default_rng()):
   '''
   Algorithm 1.6: discrete Markov Chain Monte Carlo for the pebble game

   Parameters:
       k       State
       table   Transition table
       rng     Random number generator

      Returns:
         Next state
   '''
   k_next = rng.choice(table[k,:])
   return k if k_next == -1 else k_next

def markov_visits(m,n,i,j,N,neighbour_table=neighbour_table):
   def row(cell):
      return cell//3

   def column(cell):
      return cell%3

   def step(from_cell,to_cell):
      return (row(to_cell)-row(from_cell),column(to_cell)-column(from_cell))

   def index(i,j):
      def index(ii,mm):
         if ii == 0:
            return 0
         elif ii == mm-1:
            return 2
         else:
            return 1
      row_index = index(i,m)
      col_index = index(j,n)
      return row_index*3 + col_index

   visits = np.zeros((m,n),dtype=int)
   k = index(i,j)
   for trial in range(N):
      k_next = markov_discrete_pebble(k,neighbour_table)
      r = row(k)
      col = column(k)
      di,dj = step(k,k_next)
      i += di
      j += dj
      visits[i,j] += 1
      k = index(i,j)

   return visits/N


if __name__=='__main__':
   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   start  = time()
   args = parse_arguments()
   rng = np.random.default_rng(args.seed)

   N = 1
   ns = np.zeros((args.M))
   sds = np.zeros((args.M))
   for i in range(args.M):
      N *= 10
      ns[i] = np.log(N)
      frequencies = markov_visits(args.m,args.n,0,0,N)
      sds[i] = np.log(np.std(frequencies)/np.mean(frequencies))

   fig = figure(figsize=(12,12))
   ax1 = fig.add_subplot(1,1,1)

   ax1.plot(ns, sds, 'o')
   ax1.set_xlabel('Log N trials')
   ax1.set_ylabel('Log Error')
   ax1.set_title('Error vs iteration number')

   fig.savefig(get_file_name(args.out))
   elapsed = time() - start
   minutes = int(elapsed/60)
   seconds = elapsed - 60*minutes
   print (f'Elapsed Time {minutes} m {seconds:.2f} s')

   if args.show:
      show()
