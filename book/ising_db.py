#!/usr/bin/env python

#   Copyright (C) 2025 Simon Crase

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

'''Store parameters and results in a database'''

from os.path import  splitext
import sqlite3
from io import BytesIO
from os import remove
from unittest import main, TestCase
import numpy as np
from  numpy.testing import assert_array_equal

class ContextManager:
    '''
    This class looks after the database connection,
    so we don't need to bother about closing it.
    '''
    def __init__(self,file_name):
        self.file_name = file_name

    def __enter__(self):
        self.con = sqlite3.connect(self.file_name,detect_types=sqlite3.PARSE_DECLTYPES)
        return self.con

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.con.close()

class IsingDatabase:

    '''
    This class stores parameters and results in a database
    '''
    def adapt_array(arr):
        '''
        Used to store a numpy array in database

        https://pythonforthelab.com/blog/storing-data-with-sqlite/
        https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database/18622264#18622264
        '''
        out = BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        '''
        Used to retrieve a numpy array from the database
        https://pythonforthelab.com/blog/storing-data-with-sqlite/
        https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database/18622264#18622264
        '''
        out = BytesIO(text)
        out.seek(0)
        return np.load(out)

    def __init__(self,file='test.db',run_table='run',verbose=False):
        sqlite3.register_adapter(np.ndarray, IsingDatabase.adapt_array)
        sqlite3.register_converter('array', IsingDatabase.convert_array)
        base,_ = splitext(file)
        self.file_name = f'{base}.db'
        self.run_table = run_table
        self.verbose = verbose
        with ContextManager(self.file_name) as con:
            try:
                con.execute(f'CREATE TABLE {self.run_table}(Temperature FLOAT, m INTEGER, n INTEGER, iterations INTEGER, sigma array, Energy array, Magnetization array)')
                if self.verbose:
                    print (f'Created table {self.run_table}')
            except sqlite3.OperationalError as e:
                if self.verbose:
                    print (e)
            for row in  con.execute('SELECT name FROM sqlite_master'):
                if self.verbose:
                    print (row)

    def generate_keys(self):
        '''
        Iterate through all keys in database
        '''
        with ContextManager(self.file_name) as con:
            for T,m,n in con.execute(f'SELECT Temperature,m,n FROM {self.run_table} ORDER BY Temperature'):
                yield T,m,n

    def __getitem__(self,key):
        '''
        Retrieve a set of parameters from datebase

        Parameters:
            key     T,m,n
        '''
        count = 0
        T,m,n = key
        with ContextManager(self.file_name) as con:
            for NIterations,s,E,M in con.execute(f'SELECT iterations, sigma, Energy, Magnetization FROM {self.run_table} '
                                                 f'WHERE Temperature={T} AND m={m} AND n={n}'):
                count += 1
            if count == 1:
                return NIterations,s,E,M
            elif count == 0:
                raise KeyError(f'{key} not found')
            else:
                raise ValueError(f'Multiple records found for {key}')


    def __setitem__(self,key,value):
        '''
        Store a set of parameters in datebase

        Parameters:
            key     T,m,n
            value   NIterations, s, E, M
        '''
        count = 0
        T,m,n = key
        with ContextManager(self.file_name) as con:
            for _,_,_ in con.execute(f'SELECT Temperature, m,n FROM {self.run_table} WHERE Temperature={T} AND m={m} AND n={n}'):
                count += 1
            if count > 0:
                con.execute(f'DELETE FROM {self.run_table} WHERE Temperature={T}')
            NIterations,s,E,M = value
            con.executemany(f'INSERT INTO {self.run_table} VALUES(?, ?, ?, ? ,?, ?, ?)',  [(T, m,n, NIterations, s, E, M)])
            con.commit()

class DbTest(TestCase):
    def setUp(self):
        self.db = IsingDatabase(__file__)

    def test1(self):

        self.db[(1.0,2,2)] = 1066,np.array([1,1,-1,-1]),np.array([[-72,1],[-68,4]]),np.array([[-36,1],[+36,4]])
        NIterations,s,E,M = self.db[(1.0,2,2)]
        self.assertEqual(1066,NIterations)
        assert_array_equal(np.array([1,1,-1,-1]),s)
        try:
            _ = self.db[(1.0,3,2)]
            self.fail('Exception not thrown')
        except KeyError:
            pass

    def tearDown(self):
        remove(self.db.file_name)

if __name__=='__main__':
    main()
