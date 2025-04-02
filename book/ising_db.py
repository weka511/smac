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

'''Store parameters in a database'''

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

    def __init__(self,file='test.db',run_table='run',verbose=False):
        base,_ = splitext(file)
        sqlite3.register_adapter(np.ndarray, IsingDatabase.adapt_array)
        sqlite3.register_converter('array', IsingDatabase.convert_array)
        self.con = sqlite3.connect(f'{base}.db',detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()
        self.run_table = run_table
        self.verbose = verbose
        try:
            self.execute(f'CREATE TABLE {self.run_table}(Temperature FLOAT, m INTEGER, n INTEGER, iterations INTEGER, sigma array, Energy array, Magnetization array)')
            if self.verbose:
                print (f'Created table {self.run_table}')
        except sqlite3.OperationalError as e:
            print (e)
        for row in  self.execute('SELECT name FROM sqlite_master'):
            if self.verbose:
                print (row)

    def execute(self,sql_string):
        return self.cur.execute(sql_string)

    def executemany(self,sql_string,data):
        return self.cur.executemany(sql_string,data)

    def commit(self):
        self.con.commit()

    def __getitem__(self,key):
        count = 0
        T,m,n = key
        for NIterations,s,E,M in self.execute(f'SELECT iterations, sigma, Energy, Magnetization FROM {self.run_table} WHERE Temperature={T} AND m={m} AND n={n}'):
            count += 1
        if count == 1:
            return NIterations,s,E,M
        elif count == 0:
            raise KeyError(f'{key} not found')


    def __setitem__(self,key,value):
        count = 0
        T,m,n = key
        for _,_,_ in self.execute(f'SELECT Temperature, m,n FROM {self.run_table} WHERE Temperature={T} AND m={m} AND n={n}'):
            count += 1
        if count > 0:
            self.execute(f'DELETE FROM {self.run_table} WHERE Temperature={T}')
        NIterations,s,E,M = value
        self.executemany(f'INSERT INTO {self.run_table} VALUES(?, ?, ?, ? ,?, ?, ?)',  [(T, m,n, NIterations, s, E, M)])
        self.commit()


if __name__=='__main__':
    db = IsingDatabase(__file__)
    db[(1.0,2,2)] = 1066,np.array([1,1,-1,-1]),np.array([[-72,1],[-68,4]]),np.array([[-36,1],[+36,4]])
    NIterations,s,E,M = db[(1.0,2,2)]
    z=0
    _ = db[(1.0,3,2)]
