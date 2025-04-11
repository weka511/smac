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
#include <cassert>
#include "nbr.hpp"

using namespace std;

/**
 *  This class is used to record counts of energy and magnetization
 */
class Field: public vector<pair<int,int>>{
	private:
		vector<pair<int,int>> container;
		int min;
		int step;
		
	public:
		void prepare(int min,int max,int step);
	
		/**
		 * Used to increment Energies or Magnetization
		 */
		void increment(const int k);
		
		void dump(ofstream & out,std::string header){
			out << header << std::endl;
			for (vector<pair<int,int>>::const_iterator i = container.begin(); i < container.end(); i++) 
				out << i->first << ","<< i->second << std::endl;	
		}
};

/**
 * Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 * from Statistical Mechanics, Algorithms and Computations by Werner Karuth
 */
class MarkovIsing {
	private:
	     Neighbours neighbours;
		
		vector<int> sigma;
		const int N;
		
		/**
		 * Current energy
		 */
		int E;
		
		/**
		 * Current magnetization
		 */
		int M;
		
		/**
		 * Used to record data
		 */
		ofstream & out;
		
		/**
		 * Inverse temperature
		 */
		const float beta;
		
		/**
		 * Cache relevant values of exp(-beta*deltaE)
		 */
		vector<float> Upsilon; 
		
		Field Magnetization;
		
		Field Energies;
		
		std::mt19937_64 mt{ static_cast<std::mt19937::result_type>(
							std::chrono::steady_clock::now().time_since_epoch().count())
							};
							
		std::uniform_real_distribution<float> dt;
		std::uniform_int_distribution<int> d;
		
	public:
		MarkovIsing(int m,int n,bool wrapped,ofstream &out, float beta=2.0);
		
		/**
		 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
		 */
		void prepare();
		
		/**
		 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		bool step();

	    /**
		 * Execute the entirity of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		void run(int max_steps=100000, int frequency=0);

		/**
		 * Calculate field at a particular site
		 */		
		int get_field(int i, vector<int> spins); 
		
		/**
		 * Output energy and magnetization
		 */
		void dump(ofstream & out);
		
		float get_upsilon(int i) {return Upsilon[i];};
		
};

#endif //_MARKOV_ISING_HPP_

