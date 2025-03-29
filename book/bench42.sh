#!sh
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

echo "Benchmark effect of Issue #42"
echo $1

echo "not cached"
for i in $(seq 1 5);
do
    ./exercise_5_11.py --Nsteps $1 --periodic 
done
echo "cached"
for i in $(seq 1 5);
do
    ./exercise_5_11.py --Nsteps $1 --periodic --cache
done
