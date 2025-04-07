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

#ifndef _MARKOV_ISING_HPP_
#define _MARKOV_ISING_HPP_
#include <random>
#include <chrono>
using namespace std;

class MarkovIsing {
	private:
	     Neighbours * neighbours;
		 std::mt19937_64 mt{ static_cast<std::mt19937::result_type>(
								std::chrono::steady_clock::now().time_since_epoch().count())
							};
		
		int * sigma;
		int N;
		int E;
		int M;
		float beta = 4.0;
		
	public:
		MarkovIsing(int m=6,int n=6,bool wrapped=true);
		
		void prepare();
		
		void step(int k, float rr);

		void run();
		
		int get_field(int i); 
		
		virtual ~MarkovIsing();
};
#endif
