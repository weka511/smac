#!/usr/bin/env python

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

'''Template for programs--replace with description'''

from argparse          import ArgumentParser
from matplotlib.pyplot import figure, hist, savefig, show, title
from numpy             import load
from os.path           import basename, splitext
from matplotlib        import rc


def get_plot_file_name(plot=None):
    '''Determine plot file name from source file name or command line arguments'''
    if plot==None:
        return f'{splitext(basename(__file__))[0]}.png'
    base,ext = splitext(plot)
    return f'{plot}.png' if len(ext)==0 else plot

def parse_arguments():
    parser = ArgumentParser(description = __doc__)
    parser.add_argument('file',
                        help    = 'Name of saved file')
    parser.add_argument('--show',
                        action = 'store_true',
                        help   = 'Show plot')
    parser.add_argument('--plot',
                        default = None,
                        help    = 'Name of plot file')
    return parser.parse_args()

def reload(file):
    restored = load(file, allow_pickle=True)
    return restored['Xs'], restored['Vs'], restored['args'], restored['seed'], restored['epoch']

if __name__=='__main__':
    args                       = parse_arguments()
    Xs, Vs, args0, seed, epoch = reload(args.file)
    Es       = [u**2 + v**2 for u,v in Vs]
    rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    figure(figsize = (12,12))
    hist(Es)
    title(f'Epoch={epoch}')
    savefig(get_plot_file_name(args.plot))
    if args.show:
        show()
