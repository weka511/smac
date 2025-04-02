#!/usr/bin/env python

#   Copyright (C) 2024-2025 Simon Crase

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''Store paramters in a database'''

from os.path import  splitext
import numpy as np
import sqlite3
from io import BytesIO

class IsingDatabase:
    def adapt_array(arr):
        '''
        https://pythonforthelab.com/blog/storing-data-with-sqlite/
        https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database/18622264#18622264
        '''
        out = BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        '''
        https://pythonforthelab.com/blog/storing-data-with-sqlite/
        https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database/18622264#18622264
        '''
        out = BytesIO(text)
        out.seek(0)
        return np.load(out)

    def __init__(self,file='test.db',run_table='run',verbose=True):
        base,_ = splitext(file)
        sqlite3.register_adapter(np.ndarray, IsingDatabase.adapt_array)
        sqlite3.register_converter('array', IsingDatabase.convert_array)
        self.con = sqlite3.connect(f'{base}.db',detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()
        self.run_table = run_table
        self.verbose = verbose
        try:
            self.execute(f'CREATE TABLE {self.run_table}(Temperature FLOAT PRIMARY KEY, iterations INTEGER, sigma array)')
            if self.verbose:
                print (f'Created table {self.run_table}')
        except sqlite3.OperationalError as e:
            print (f'Table {self.run_table} exists already')
        for row in  self.execute('SELECT name FROM sqlite_master'):
            print (row)

    def execute(self,sql_string):
        return self.cur.execute(sql_string)

    def executemany(self,sql_string,data):
        return self.cur.executemany(sql_string,data)

    def commit(self):
        self.con.commit()

    def __getitem__(self,key):
        count = 0
        T = None
        M = None
        s = None
        for T,M,s in self.execute(f'SELECT Temperature, iterations, sigma FROM {self.run_table} WHERE Temperature={key}'):
            count += 1
        return count,T,M,s

    def __setitem__(self,T,value):
        count = 0
        for T,M,s in self.execute(f'SELECT Temperature, iterations, sigma FROM {self.run_table} WHERE Temperature={T}'):
            count += 1
        M,s = value
        if count == 0:
            data = [(T, M, s)]
            self.executemany(f'INSERT INTO {self.run_table} VALUES(?, ?, ?)', data)
            self.commit()
        else:
            self.execute(f'UPDATE {self.run_table} SET M = {M} WHERE Temperature={T}')

if __name__=='__main__':
    db = IsingDatabase('baz')
    db[1.0] = 666,np.array([1,1,-1,-1])
    # count,T,M,s = db[1.0]

    z=0

