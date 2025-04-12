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
 * This type represents a collection of counts from different runs
 */
typedef vector<int> row;

/**
 * This type represents a value (Energy or Magnetism), plus its collection of counts from different runs
 */
typedef pair<int,row> CountedData;
/**
 *  This class is used to record counts of energy and magnetization
 */
class Field: public vector<pair<int,int>>{
	private:
		vector<CountedData> container;
		int min;
		int max;
		int step;
		int width;
		
	public:	
		void prepare(const int min, const int max, const int step, const int width);
	
		/**
		 * Used to increment Energies or Magnetization
		 */
		void increment(const int k,const int run=0);  // FIXME k?
		
		void dump(ofstream & out,std::string header);
		
		bool all_zero(row counts) {
			for (vector<int>::const_iterator j = counts.begin(); j < counts.end(); j++)
				if (*j > 0) return false;
			return true;
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
		void initialize_counts(const int width=1);
		/**
		 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
		 */
		void prepare(const int run=1);
		
		/**
		 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		bool step(const int run);

	    /**
		 * Execute the entirety of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		void run(int max_steps=100000, int frequency=0, const int run=1);

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

