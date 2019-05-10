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
 

 
 int nbr(const int cell, const int seq, const int n) {
	 int column = cell%n; if (column==0) column = n;
	 int row = cell/n; if (column<n) row+=1;
	 
	 switch (seq) {
		 case 1:
			column++;
			break;
		 case 2:
			row++;
			break;
		 case 3:
			column--;
			break;
		 case 4:
			row--;
			break;
	 }
	 if (row<1 || row>n || column<1 ||column>n)
		 return -1;
	 else
		 return (row-1)*n+column;
 }