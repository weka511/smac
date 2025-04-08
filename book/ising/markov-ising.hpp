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
#include "nbr.hpp"
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
		ofstream &out;
	public:
		MarkovIsing(int ,int n,bool wrapped,ofstream &out);
		
		void prepare();
		
		void step(int k, float rr,float * Upsilon);

		void run(int max_steps=100000, int frequency=1000);
		
		int get_field(int i); 
		
		virtual ~MarkovIsing();
};
#endif
