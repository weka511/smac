# smacfiletoken.py

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

# Problem 1.3 from Werner Krauth, Statistical Mechanics, Algorithms & Computations
# Tested using direct.py (Problem 1.1)

import os, time, tempfile

def make_temp_file(name):
    return os.path.join(tempfile.gettempdir(),name)
    
class Token:
    def __init__(self,name):
        self.name=make_temp_file(name)
        self.timeformat="%a, %d %b %Y %H:%M:%S +0000"
    
    def exists(self):
        return os.path.isfile(self.name)
       
    def read(self,initial):
        if self.exists():
            with open(self.name,"r") as f:
                date_line=f.readline().strip(' \t\n\r')
                self.time=time.strptime(date_line, self.timeformat)
                return self.line2floats(f.readline().strip(' \t\n\r'))
        else:
            return initial
        
    def line2floats(self,line):
        return [float(s) for s in line.split(",")]
    
    def write(self,values):
        with open(self.name,"w") as f:
           ts=time.strftime(self.timeformat) 
           f.write(ts+"\n")
           f.write(self.list2str(values)+"\n")
           
    def list2str(self,values):
        result=""
        sep=""
        for el in values:
            result+=sep
            result+=str(el)
            sep=","
        return result    
    
    def precedes(self,other):
        return self.time<other.time

# This class allows Tokens to be stored in a Regisrty file
# Or retrieved, and it also manages kill Tokens

class Registry:
    def __init__(self,kill_token="kill.txt"):
        self.tokens=[]
        self.kill_token=kill_token
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
        if os.path.isfile(self.kill_token):
            print ("killing")
            os.remove(self.kill_token)
            return True
        else:
            return False
   