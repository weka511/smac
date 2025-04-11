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
	neighbours.prepare(m,n,wrapped);
	out << "m="<<m <<",n="<<n<<",periodic="<<wrapped<<",beta="<<beta <<std::endl;
}

/**
 * This method is used to initialize the spins, E, M, and the counts at the start of each run.
 */
void MarkovIsing::prepare() {
	for (int i=1;i<=2*neighbours.get_d();i++){
		const int deltaE = 2*i;
		Upsilon.push_back(exp(-beta*deltaE));
	}
		
	std::uniform_int_distribution<int> bits(0,1);
	for (int i=0;i<N;i++) 
		sigma.push_back(2*bits(mt) - 1);

	Energies.prepare(-2*N,2*N,2);		
	E = 0;
	for (int i=0;i<N;i++)
		E += sigma[i] * get_field(i,sigma);
	
	assert(E%4==0);
	Energies.increment(E);

	Magnetization.prepare(-N,N,1);
	M = 0;
	for (int i=0;i<N;i++)
		M += sigma[i];
	Magnetization.increment(M);
}	

/**
 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
bool MarkovIsing::step() {
	const int k = d(mt);
	const int h = get_field(k,sigma);
	const int deltaE = 2 * h * sigma[k];
	const bool accepted = deltaE <= 0 or dt(mt) < Upsilon[deltaE/2-1];
	
	if (accepted){
		sigma[k] *= -1;
		E += deltaE;
		M += 2*sigma[k];
	}

	Energies.increment(M);
	Magnetization.increment(M);

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
void MarkovIsing::dump(ofstream & out) {
	Energies.dump(out,"E,N");
	Magnetization.dump(out,"M,N");
}

void Field::increment(const int x){
	const int k = (x-min)/step;
	assert (0 <=k and k<container.size());
	const int i = container[k].first;
	int j = container[k].second;
	j++;
	container[k] = make_pair(i,j);
}

void Field::prepare(int min,int max,int step){
	for (int i=min;i<=max;i+=step)
		container.push_back(make_pair(i,0));
	this->min = min;
	this->step = step;
}
