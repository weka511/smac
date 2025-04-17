/**
 * Copyright (C) 2025 Greenweaves Software Limited
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
#include <vector>

#include "nbr.hpp"
#include "field.hpp"

using namespace std;



/**
 * Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 * from Statistical Mechanics, Algorithms and Computations by Werner Karuth
 */
class MarkovIsing {
	private:
	     Neighbours neighbours;
		
		/**
		 * The spins
		 */
		vector<int> sigma;
		
		/**
		 * Total number od spins
		 */
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
		 *
		 * Upsilon[0] = exp(-2 beta)
		 * Upsilon[1] = exp(-4 beta)
		 ...
	  	 * Upsilon[2d-1] = exp(-4 d beta)
		 *
		 */
		vector<float> Upsilon; 
		
		/**
		 *  Stored values of magnetization and their counts
		 */
		Field Magnetization;
		
		/**
		 *  Stored values of energy and their counts
		 */
		Field Energies;
		
		std::mt19937_64 mt{ static_cast<std::mt19937::result_type>(
							std::chrono::steady_clock::now().time_since_epoch().count())
							};
							
		std::uniform_real_distribution<float> dt;
		
		std::uniform_int_distribution<int> d;
		
		/**
		 * This method is used to randomize the spins at the start of each run.
		 */
		void randomize_spins();
		
		/**
		 * This method is used to initialize E, M, and their counts at the start of each run.
		 */
		void resetEM(const int run=1);
		
		/**
		 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model.
		 * If burned in, store energy and momentu acceptem.
		 *
		 * Returns true iff we have burned in, and the proposed step has been accepted,
		 * so caller can calculate accpetance. 
		 */	
		bool step(const int run,const bool has_burned_in);
		
	public:
		/**
		 * Initialize neighbour table and the data storage for energy and magnetization.  
		 * Cache the exp(-beta*deltaE) and create a vector of spins (all zero). The spins
		 * will be set correctly at the start of each run.
		 */
		MarkovIsing(const int m,int const n,const bool wrapped, ofstream &out, const float beta, const int nruns);
		
	    /**
		 * Execute the entirety of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
		 */	
		void run(int max_steps, int frequency, const int run,const int burn_in);

		/**
		 * Calculate field at a particular site
		 */		
		int get_field(int i, vector<int> spins); 
		
		/**
		 * Output energy and magnetization
		 */
		int dump();
		
		/**
		 * Access cached values of exp(-beta*deltaE)
		 */
		float get_upsilon(int i) {return Upsilon[i];};
		
		int get_count(const int energy, const int run);
		
};

#endif //_MARKOV_ISING_HPP_

