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
#include <utility>
#include <vector>
#include "nbr.hpp"

using namespace std;

/**
 * Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 * from Statistical Mechanics, Algorithms and Computations by Werner Karuth
 */
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
		ofstream & out;
		float beta;
		float * Upsilon; 
		vector<pair<int,int>> Magnetization;
		vector<pair<int,int>> Energies;
		
		void increment(vector<pair<int,int>> & Field,const int k){
			int i = Field[k].first;
			int j = Field[k].second;
			j++;
			Field[k] = make_pair(i,j);
		}
	public:
		MarkovIsing(int m,int n,bool wrapped,ofstream &out, float beta=2.0);
		
		/**
		 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
		 */
		void prepare();
		
		/**
		 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		bool step(int k, float rr);

	    /**
		 * Execute the entirity of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		void run(int max_steps=100000, int frequency=0);

		/**
		 * Calculate field at a particular site
		 */		
		int get_field(int i, int * spins); 
		
		void dump(ofstream & out);
		
		virtual ~MarkovIsing();
};

#endif //_MARKOV_ISING_HPP_

