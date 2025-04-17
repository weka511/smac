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
 
#include <iostream>
#include <fstream>
#include <cassert>
#include <chrono>

#include "gray.hpp"
#include "nbr.hpp"
#include "markov-ising.hpp"

using namespace std;

/**
 * Initialize neighbour table and the data storage for energy and magnetization.  
 * Cache the exp(-beta*deltaE) and create a vector of spins (all zero). The spins
 * will be set correctly at the start of each run.
 */
MarkovIsing::MarkovIsing(const int m,const int n,const bool wrapped, ofstream &out, const float beta, const int nruns) :
			out(out), beta(beta), N(m*n), dt(0,1), d(0,m*n-1) {
	neighbours.prepare(m,n,wrapped);
	Energies.prepare(-4*N,4*N,2,nruns);	
	Magnetization.prepare(-N,N,1,nruns);		
	for (int i=1;i<=2*neighbours.get_d();i++){
		const int deltaE = 2*i;
		Upsilon.push_back(exp(-beta*deltaE));
	}
	for (int i=0;i<N;i++) 
		sigma.push_back(0);
	out << "m="<<m <<",n="<<n<<",periodic="<<wrapped<<",beta="<<beta <<",nruns=" << nruns<<std::endl;
}


/**
 * This method is used to randomize the spins at the start of each run.
 */
void MarkovIsing::randomize_spins() {
	std::uniform_int_distribution<int> bits(0,1);
	for (int i=0;i<N;i++) 
		sigma[i] = 2*bits(mt) - 1;
}

/**
 * This method is used to initialize E, M, and their counts at the start of each run.
 */
void MarkovIsing::resetEM(const int run) {
	E = 0;
	for (int i=0;i<N;i++)
		E += sigma[i] * get_field(i,sigma);
	
	E /= 2; // The preceding lines double count the links

	M = 0;
	for (int i=0;i<N;i++)
		M += sigma[i];
}	

/**
 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model.
 * If burned in, store energy and momentu acceptem.
 *
 * Returns true iff we have burned in, and the proposed step has been accepted,
 * so caller can calculate accpetance. 
 */	
bool MarkovIsing::step(const int run, const bool has_burned_in) {

	const int k = d(mt);
	const int h = get_field(k,sigma);
	// assert (h%2==0);
	// assert((-2*neighbours.get_d() <= h) && (h <= 2*neighbours.get_d()));
	const int deltaE = 2 * h * sigma[k];   // FIXME  Issue #55
	const bool accepted = (deltaE <= 0) or (dt(mt) < Upsilon[deltaE/2-1]); // Upsilon = exp(-2 beta), exp(-4 beta), ...
	if (accepted){     // Move to new state
		sigma[k] *= -1;
		E -= deltaE;     // FIXME   Issue #55
		M += 2*sigma[k];
	}
	
	if (has_burned_in) {
		Energies.increment(E,run);
		Magnetization.increment(M,run);
	}

	return has_burned_in and accepted;
}

/**
 * Execute the entirety of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
void MarkovIsing::run(int max_steps, int frequency, const int run,const int burn_in) {
	auto start = std::chrono::steady_clock::now();
	randomize_spins();
	resetEM(run);
	int total_accepted = 0;
	
	for (int i=0;i<max_steps+burn_in;i++){
		if (frequency > 0 && i > 0 && i%frequency ==0)
			std::cout << i << std::endl;
		if (step(run, burn_in <= i))
			total_accepted++;
	}
	auto end = std::chrono::steady_clock::now();
	// std::cout << "beta="<<beta<<", acceptance="<<(100.0*total_accepted)/max_steps <<"%"<< " "
				// << chrono::duration_cast<chrono::seconds>(end - start).count() << " sec" << std::endl;
	
	out << "beta="<<beta<<", total_accepted="<<total_accepted<<", max_steps="<<max_steps << std::endl;
}

/**
 * Calculate field at a particular site
 */
int MarkovIsing::get_field(int i,vector<int> spins) {
	int h = 0;
	for (int j=0;j<2*neighbours.get_d() + 1;j++) {
		const int ij_neighbour = neighbours.get_neighbour(i,j);
		if (ij_neighbour > -1)
			h += spins[ij_neighbour];
	}
	
	return h;
}

/**
 * Output energy and magnetization
 */
int MarkovIsing::dump() {
	const int total_count = Energies.dump(out,"E,N");
	Magnetization.dump(out,"M,N");
	return total_count;
}

int MarkovIsing::get_count(const int energy, const int run){
	return Energies.get_count(energy, run);
}


