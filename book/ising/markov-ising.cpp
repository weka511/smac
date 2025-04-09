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
#include <string>

#include "gray.hpp"
#include "nbr.hpp"
#include "markov-ising.hpp"

using namespace std;

MarkovIsing::MarkovIsing(int m,int n,bool wrapped,ofstream &out, float beta) :
			out(out), beta(beta),N(m*n) {
	neighbours = new Neighbours(m,n,wrapped);
	
	sigma = new int[m*n]; 
	
	Upsilon = new float[5];
	for (int E=0;E<=2*neighbours->get_d();E++)
		Upsilon[E/2] = exp(-beta*E);
		
	for (int i=0;i<2*N +1;i++)
		Energies.push_back(make_pair(2*i-2*N,0));
	for (int i=0;i<2*N+1;i++)
		Magnetization.push_back(make_pair(i-N,0));

}

/**
 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
 */
void MarkovIsing::prepare() {
	for (int i=0;i<N;i++) 
		sigma[i] = 2*(mt()%2) - 1;
	
	M = 0;
	for (int i=0;i<N;i++)
		M += sigma[i];
	
	E = 0;
	for (int i=0;i<N;i++)  {
		int h = get_field(i,sigma);
		E += sigma[i] * h;
	}
	std::cout << E << ", " << M <<std::endl;
	increment(Energies,E/2+N);
	increment(Magnetization,(M+N));
}	

/**
 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
bool MarkovIsing::step(int k, float rr) {
	std::uniform_real_distribution<float> dt(0,1);
	const int h = get_field(k,sigma);
	const int deltaE = 2 * h * sigma[k];
	const bool accepted = (deltaE <= 0 or rr < Upsilon[deltaE/2]);
	// std::cout << "k="<< k << ", deltaE=" << deltaE <<", Upsilon[deltaE/2]=" << Upsilon[deltaE/2]<< ", rr=" << rr <<", accepted=" << accepted << std::endl;
	if (accepted){
		sigma[k] *= -1;
		E += deltaE;
		M -= sigma[k];
	}
	increment(Energies,E/2+N);
	increment(Magnetization,(M+N));
	return accepted;
}

/**
 * Execute the entirity of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
void MarkovIsing::run(int max_steps, int frequency) {
	std::uniform_real_distribution<float> dt(0,1);	
	std::uniform_int_distribution<int> d(0,_N-1);

	prepare();
	int total_accepted = 0;
	for (int i=0;i<max_steps;i++){
		if (frequency > 0 && i > 0 && i%frequency ==0)
			std::cout << i << std::endl;
		if (step(d(mt),dt(mt)))
			total_accepted += 1;
	}
	std::cout << beta<<", "<<((float)total_accepted)/max_steps << std::endl;
	dump(out);
}

/**
 * Calculate field at a particular site
 */
int MarkovIsing::get_field(int i,int * spins) {
	int h = 0;
	for (int j=0;j<2*neighbours->get_d() + 1;j++) 
		if (neighbours->get_neighbour(i,j) > -1)
			h += spins[neighbours->get_neighbour(i,j)];
	return h;
}

MarkovIsing::~MarkovIsing(){
	delete neighbours;
	delete [] sigma;
	// delete [] EnergyCounts;
	// delete [] MagnetizationCounts;
	delete [] Upsilon;
};

void MarkovIsing::dump(ofstream & out) {
	for (vector<pair<int,int>>::const_iterator i = Energies.begin(); i < Energies.end(); i++) 
        out << i->first << " "<< i->second << std::endl;
	for (vector<pair<int,int>>::const_iterator i = Magnetization.begin(); i < Magnetization.end(); i++) 
        out << i->first << " "<< i->second << std::endl;
}