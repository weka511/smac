/**
 * Copyright (C) 2019-2025 Greenweaves Software Limited
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
#include <vector> 
using namespace std;

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
			bool wrapped) ;
				
	
 /**
  * This class caches the neighbours of all specified cells, shifted by one, e.g.
  *                   6-7-8
  *                   | | |
  *                   3-4-5
  *                   | | |
  *                   0-1-2
  */
 class Neighbours{
	private:
		int d;
		int N;
		vector<vector<int>> neighbours;
	public:
	
		void prepare(const int m,
					const int n,
					bool wrapped);
					
		int get_neighbour(int i,int j) {return neighbours[i][j];}
		
		int get_d() {return d;}
 };
 
 #endif //_NBR_HPP_
 