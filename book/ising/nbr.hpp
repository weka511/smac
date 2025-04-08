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
 
using namespace std;
#include <iostream>
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
			bool wrapped=false) ;
				
	
 
 class Neighbours{
	private:
		const int _d;
		const int N;
		int ** _neighbours;
	public:
		Neighbours(const int m,
					const int n,
					bool wrapped=false) : _d(2), N(m*n){
			_neighbours = new int*[N];
			for(int i = 0; i < N; ++i){
				_neighbours[i] = new int[2*_d+1];
				for (int j=0;j<2*_d+1;j++)
					_neighbours[i][j] = nbr(i+1,j+1, n, wrapped);
			}
		}
		
		int get_neighbour(int i,int j) {return _neighbours[i][j];}
		
		int get_d() {return _d;}
		virtual ~Neighbours() {
			 for(int i = 0; i < N; ++i)
				 delete [] _neighbours[i];
			 delete [] _neighbours;
			 std::cout << "Cleaned up" << std::endl;
		 }
	 

 };
 #endif
 