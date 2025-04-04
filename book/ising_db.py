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
from send2trash import send2trash
import numpy as np
from numpy.testing import assert_array_equal

class ContextManager:
    '''
    This class looks after the database connection,
    so we don't need to bother about closing it.
    '''
    def __init__(self,file_name):
        self.file_name = file_name

    def __enter__(self):
        '''
        Connect to database when we enter context
        '''
        self.con = sqlite3.connect(self.file_name,detect_types=sqlite3.PARSE_DECLTYPES)
        return self.con

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''
        Automagically disconnect when we leave
        '''
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

    def __init__(self,file='test.db',run_table='run',
                 spins_table='Spins',energies_table='energies',magnetization_table='magnetization',verbose=False,fresh=False):
        sqlite3.register_adapter(np.ndarray, IsingDatabase.adapt_array)
        sqlite3.register_converter('array', IsingDatabase.convert_array)
        base,_ = splitext(file)
        self.file_name = f'{base}.db'
        self.run_table = run_table
        self.spins_table = spins_table
        self.energies_table = energies_table
        self.magnetization_table = magnetization_table
        self.verbose = verbose
        if fresh: self.__ensure_fresh()

        self.__ensure_table_exists(self.run_table,
                                 '(Temperature FLOAT NOT NULL, m INTEGER NOT NULL, n INTEGER NOT NULL, iterations INTEGER,'
                                 'CONSTRAINT PK_run PRIMARY KEY (Temperature,m,n))')
        self.__ensure_table_exists(self.spins_table,
                                 '(Temperature FLOAT NOT NULL, m INTEGER NOT NULL, n INTEGER NOT NULL, site INTEGER NOT NULL,'
                                 ' spin INTEGER NOT NULL,'
                                 'CONSTRAINT PK_run PRIMARY KEY (Temperature,m,n,site))')
        self.__ensure_table_exists(self.energies_table,
                                 '(Temperature FLOAT NOT NULL, m INTEGER NOT NULL, n INTEGER NOT NULL, Value INTEGER NOT NULL,'
                                 ' Count INTEGER NOT NULL,'
                                 'CONSTRAINT PK_run PRIMARY KEY (Temperature,m,n,Value))')
        self.__ensure_table_exists(self.magnetization_table,
                                 '(Temperature FLOAT NOT NULL, m INTEGER NOT NULL, n INTEGER NOT NULL, Value INTEGER NOT NULL,'
                                 ' Count INTEGER NOT NULL,'
                                 'CONSTRAINT PK_run PRIMARY KEY (Temperature,m,n,Value))')

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
        def create_spins(table):
            spins = [spin for _,spin in con.execute(f'SELECT site,spin FROM {table} '
                                                 f'WHERE Temperature={T} AND m={m} AND n={n} ORDER BY site')]
            return np.array(spins,dtype=int)
        def create_EM(table):
            energies = [pair for pair in con.execute(f'SELECT value,count FROM {table} '
                                                 f'WHERE Temperature={T} AND m={m} AND n={n} ORDER BY value')]
            return np.array(energies,dtype=int)
        count = 0
        T,m,n = key
        with ContextManager(self.file_name) as con:
            for NIterations, in con.execute(f'SELECT iterations FROM {self.run_table} '
                                                 f'WHERE Temperature={T} AND m={m} AND n={n}'):
                count += 1
            if count == 1:
                return NIterations,create_spins(self.spins_table),create_EM(self.energies_table),create_EM(self.magnetization_table)
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
        def insert_2d(EM,table):
            nrows,_ = EM.shape
            for i in range(nrows):
                value,count = EM[i,:]
                con.executemany(f'INSERT INTO {table} VALUES(?, ?, ?, ? ,?)',  [(T, m,n, int(value), int(count))])

        T,m,n = key
        with ContextManager(self.file_name) as con:
            for table in [self.run_table, self.spins_table, self.energies_table, self.magnetization_table]:
                self.__remove_old_entries(table,con,T,m,n)

            NIterations,spins,E,M = value
            con.executemany(f'INSERT INTO {self.run_table} VALUES(?, ?, ?, ? )',  [(T, m,n, NIterations)])
            for i in range(len(spins)):
                con.executemany(f'INSERT INTO {self.spins_table} VALUES(?, ?, ?, ? ,?)',  [(T, m,n, i, int(spins[i]))])
            insert_2d(E,self.energies_table)
            insert_2d(M,self.magnetization_table)

            con.commit()

    def __ensure_fresh(self):
        '''
        Used to ensure a fresh database (usually for testing)
        Recycle the old database to be safe!
        '''
        try:
            send2trash(self.file_name)
            if self.verbose:
                print (f'Recycled {self.file_name}')
        except FileNotFoundError:
            if self.verbose:
                print (f'Could not find {self.file_name}')

    def __ensure_table_exists(self,table,columns):
        '''
        When we create dataase, this is used to create the necessary tables.
        '''
        with ContextManager(self.file_name) as con:
            try:
                con.execute(f'CREATE TABLE {table} {columns}')
                if self.verbose:
                    print (f'Created table {table}')
            except sqlite3.OperationalError as e:
                if self.verbose:
                    print (e)
            for row in  con.execute('SELECT name FROM sqlite_master'):
                if self.verbose:
                    print ('name:', row)

    def __remove_old_entries(self,table,con,T,m,n):
        '''
        Used to remove old data that is to be replaced
        '''
        con.execute(f'DELETE FROM {table} WHERE Temperature={T} AND m={m} AND n={n}')


class DbTest(TestCase):
    def setUp(self):
        self.db = IsingDatabase(__file__)

    def test1(self):
        spins = np.array([1,1,-1,-1],dtype=int)
        E = np.array([[-72,2],[-70,4],[-68,6]],dtype=int)
        M = np.array([[12,4],[-12,5]],dtype=int)
        self.db[(1.0,2,2)] = 1066,spins,E,M
        NIterations,s,E1,M1 = self.db[(1.0,2,2)]
        self.assertEqual(1066,NIterations)
        assert_array_equal(np.array([1,1,-1,-1]),s)
        try:
            _ = self.db[(1.0,3,2)]
            self.fail('Exception not thrown')
        except KeyError:
            pass
        self.db[(1.0,2,2)] = 1067,spins,E,M

    def tearDown(self):
        remove(self.db.file_name)

if __name__=='__main__':
    main()
