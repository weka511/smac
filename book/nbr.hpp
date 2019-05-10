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
 
#ifndef _NBR_HPP_
#define _NBR_HPP_
 
 /**
  * Find neighbours of specified cell. Layout is shown in Figure 5-2.
  * E.g. for 3x3 case:
  *                   7-8-9
  *                   | | |
  *                   4-5-6
  *                   | | |
  *                   1-2-3
  */
 int nbr(	const int cell,
			const int seq,
			const int n,
			bool wrapped=false) {
				
	 int column = cell%n; if (column==0) column = n;
	 int row = cell/n;    if (column<n) row+=1;
	 
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
	 
	 if (wrapped) {
		 if (row<1) row       = n;
		 if (row>n) row       = 1;
		 if (column<1) column = n;
		 if (column>n) column = 1;
	 } else
		if (row<1 || row>n || column<1 ||column>n)
			return -1;
	
	return (row-1)*n+column;
 }
 
 #endif
 