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

#ifndef _ENUMERATE_ISING_HPP_
#define _ENUMERATE_ISING_HPP_

#include <vector>
#include <map>


/**
 *   This class is reposnsible for enumerating states and calculating Energy and Magnetization.
 */
class IsingEnumerator {
		
	public:
		/**
		 *  Compute molecular field at location k,, i.e.
		 *  the total contribution of all neighbours
		 */					
		int get_field(	vector<int> sigma,
						int k,
						int n,
						bool wrapped = false);
						
		/**
		 *  Enumerate energy levels
		 */
		void enumerate_ising(	int n,
						// ofstream &out,
						bool wrapped = false,
						bool progress = false);
						
		void output(ofstream &out);
		
		map<pair<int,int>, long long int> Ns;

	
};
#endif //_ENUMERATE_ISING_HPP_
