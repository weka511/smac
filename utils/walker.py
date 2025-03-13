#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

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
Used to create README.MD from file tree
'''

from os import walk
from re import match

def get_python(files):
    return [file for file in files if file.endswith('.py')]

n = 0
name = ''
header = 'https://github.com/weka511/smac/tree/master/'
nbsp = '&nbsp;'
Lines  = {}

for i in range(9):
    Lines[i+1]=[]

for root,d,files in walk('.'):
    if root.startswith(r'.\.git'): continue
    m = match(r'\.\\((homework)|(lecture)|(tutorial))_(\d+)$',root)
    if m:
        name = m.group(1)
        n    = int(m.group(5))

    if n>0:
        for i,file in enumerate(get_python(files)):
            if i==0:
                Lines[n].append(f'{n}|[{name.title()}]({header}{name}_{n})|{file}|')
            else:
                Lines[n].append (f'{nbsp}|{nbsp}|{file}|')

for key,value in Lines.items():
    for v in value:
        print (v)
