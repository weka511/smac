/**
 * Copyright (C) 2019 Greenweaves Software Limited
 *
 * This is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>
 */
 
 int force_into_range(int i,int n) {
	 return i>0 and i<=n ? i : -1;
 }
 
 int nbr(int i, int j, int n) {
	 switch (j) {
		 case 0:
			return force_into_range(i+1,n*n);
		 case 1:
			return force_into_range(i+n,n*n);
		 case 2:
			return force_into_range(i-1,n*n);
		 case 3:
			return force_into_range(i-n,n*n);
	 }
 }