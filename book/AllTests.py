#!/usr/bin/env python

# Copyright (C) 2025 Greenweaves Software Limited
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

'''
	Test harness for all modules in this folder
    Import tests from other models and execute them
'''

from unittest import main

from ising import NbrTest, GrayGeneratorTest, GrayFlipTest, NeighboursTest, Nbr3dTest, EdgeTest, EM_Test
from enumerate_ising import TestIsing
from geometry import TestHistogram
from cluster_ising import ClusterIsingTests
from ising_db import DbTest
from thermo import TestThermo

main()
