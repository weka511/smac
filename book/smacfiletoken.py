#!/usr/bin/env python

# Copyright (C) 2015-2025 Greenweaves Software Limited

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
    Problem 1.3 from Werner Krauth, Statistical Mechanics, Algorithms & Computations
    Allow program to be stopped by creating kill token. Tested using direct.py (Problem 1.1)
'''

from os import remove
from os.path import join, isfile
from time import strptime, strftime
from tempfile import gettempdir

def make_temp_file(name):
    '''
    Create a path to a named temporary file
    '''
    return join(gettempdir(),name)

class Token:
    def __init__(self,name):
        self.name       = make_temp_file(name)
        self.timeformat = "%a, %d %b %Y %H:%M:%S +0000"

    def exists(self):
        return isfile(self.name)

    def read(self,initial):
        if self.exists():
            with open(self.name,"r") as f:
                date_line = f.readline().strip(' \t\n\r')
                self.time = strptime(date_line, self.timeformat)
                return self.line2floats(f.readline().strip(' \t\n\r'))
        else:
            return initial

    def line2floats(self,line):
        return [float(s) for s in line.split(",")]

    def write(self,values):
        with open(self.name,"w") as f:
            ts = strftime(self.timeformat)
            f.write(ts+"\n")
            f.write(self.list2str(values)+"\n")

    def list2str(self,values):
        result = ""
        sep    = ""
        for el in values:
            result += sep
            result += str(el)
            sep     =","
        return result

    def precedes(self,other):
        return self.time<other.time

class Registry:
    '''
        This class allows Tokens to be stored in a Registry file
        or retrieved, and it also manages kill Tokens
    '''
    def __init__(self,kill_token="stop"):
        self.tokens = []
        self.kill_token = kill_token

    def register(self,token):
        self.tokens.append(token)

    def register_all(self,pattern):
        self.register_one(pattern,1)
        self.register_one(pattern,2)

    def register_one(self,pattern,n):
        self.register(Token(pattern%n))

    def write(self,values):
        for token in self.tokens:
            token.write(values)

    def read(self,initial):
        latestToken=None
        for token in self.tokens:
            if latestToken==None:
                latestToken=token
            elif token.exists() and latestToken.exists():
                latestToken.read(initial)
                token.read(initial)
                if latestToken.precedes(token):
                    latestToken=token
            elif token.exists():
                latestToken=token
        return latestToken.read(initial)

    def is_kill_token_present(self):
        if isfile(self.kill_token):
            print ("killing")
            try:
                remove(self.kill_token)
            except PermissionError as err:
                print ('Failed to delete killfile')
                print (err)
            return True
        else:
            return False
