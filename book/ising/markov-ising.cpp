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

#include "gray.hpp"
#include "nbr.hpp"
#include "markov-ising.hpp"

using namespace std;

MarkovIsing::MarkovIsing(int m,int n,bool wrapped,ofstream &out, float beta) :
			out(out), beta(beta), N(m*n), dt(0,1), d(0,m*n-1) {
	neighbours = new Neighbours(m,n,wrapped);
	out << "m="<<m <<",n="<<n<<",periodic="<<wrapped<<",beta="<<beta <<std::endl;
}

/**
 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
 */
void MarkovIsing::prepare() {
	
	for (int E=0;E<=2*neighbours->get_d();E+=2)
		Upsilon.push_back(exp(-beta*E));
		
	std::uniform_int_distribution<int> bits(0,1);
	for (int i=0;i<N;i++) 
		sigma.push_back(2*bits(mt) - 1);

	for (int i=0;i<2*N +1;i++)
		Energies.push_back(make_pair(2*i-2*N,0));
	
	E = 0;
	for (int i=0;i<N;i++)  {
		int h = get_field(i,sigma);
		E += sigma[i] * h;
	}
	
	assert(E%4==0);
	E /= 2;
	increment(Energies,E/2+N);

	for (int i=0;i<2*N+1;i++)
			Magnetization.push_back(make_pair(i-N,0));
	
	M = 0;
	for (int i=0;i<N;i++)
		M += sigma[i];
	
	increment(Magnetization,(M+N));
}	

/**
 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
bool MarkovIsing::step() {
	const int k = d(mt);
	const int h = get_field(k,sigma);
	const int deltaE = 2 * h * sigma[k];
	const bool accepted = deltaE <= 0 or dt(mt) < Upsilon[deltaE/2];
	
	if (accepted){
		sigma[k] *= -1;
		E += deltaE;
		M += 2*sigma[k];
	}
	increment(Energies,E/2+N);
	increment(Magnetization,M+N);
	return accepted;
}

/**
 * Execute the entirity of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
void MarkovIsing::run(int max_steps, int frequency) {

	prepare();
	int total_accepted = 0;
	
	for (int i=0;i<max_steps;i++){
		if (frequency > 0 && i > 0 && i%frequency ==0)
			std::cout << i << std::endl;
		if (step())
			total_accepted++;
	}
	std::cout << "beta="<<beta<<", acceptance="<<(100.0*total_accepted)/max_steps <<"%"<< std::endl;
	dump(out);
}

/**
 * Calculate field at a particular site
 */
int MarkovIsing::get_field(int i,vector<int> spins) {
	int h = 0;
	for (int j=0;j<2*neighbours->get_d() + 1;j++) 
		if (neighbours->get_neighbour(i,j) > -1)
			h += spins[neighbours->get_neighbour(i,j)];
	return h;
}

/**
 * Output energy and magnetization
 */
void MarkovIsing::dump(ofstream & out) {
	out << "E,N" <<std::endl;
	for (vector<pair<int,int>>::const_iterator i = Energies.begin(); i < Energies.end(); i++) 
        out << i->first << ","<< i->second << std::endl;
	out << "M,N" <<std::endl;
	for (vector<pair<int,int>>::const_iterator i = Magnetization.begin(); i < Magnetization.end(); i++) 
        out << i->first << ","<< i->second << std::endl;
}

MarkovIsing::~MarkovIsing(){
	delete neighbours;
}