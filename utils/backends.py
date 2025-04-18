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

from matplotlib import use,get_backend

gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg']

for gui in gui_env:
    try:
        print("testing", gui)
        use(gui, force=True)
        break
    except (ModuleNotFoundError,ValueError) as e:
        print (e)
        continue

print("Using:",get_backend())
