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
#include <map>
#include <utility>
#include <getopt.h>
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
	for (int E=0;E<=8;E++)
		Upsilon[E/2] = exp(-beta*E);

	EnergyCounts = new int[2*N +1];
	MagnetizationCounts = new int[N+1];
}

void MarkovIsing::prepare() {
	M = 0;
	E = 0;
	for (int i=0;i<N;i++) 
		sigma[i] = 2*(mt()%2) - 1;
	for (int i=0;i<N;i++)  {
		M += sigma[i];
		int h = get_field(i,sigma);
		E += sigma[i] * h;
	}
	MagnetizationCounts[(M+N)/2] += 1;
	EnergyCounts[M/2+N] += 1;
}	

/**
 * Execute one step of Algorithm 5.7, Local Metropolis algorithm for the Ising Model,
 */	
bool MarkovIsing::step(int k, float rr) {
	std::uniform_real_distribution<float> dt(0,1);
	int h = get_field(k,sigma);
	int deltaE = 2 * h * sigma[k];
	bool accepted = (deltaE <= 0 or rr < Upsilon[deltaE/2]);
	std::cout << "k="<< k << ", deltaE=" << deltaE <<", Upsilon[deltaE/2]=" << Upsilon[deltaE/2]<< ", rr=" << rr <<", accepted=" << accepted << std::endl;
	if (accepted){
		sigma[k] *= -1;
		E += deltaE;
		M -= sigma[k];
	}
	MagnetizationCounts[(M+N)/2] += 1;
	EnergyCounts[M/2+N] += 1;
	return accepted;
}


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
	delete [] EnergyCounts;
	delete [] MagnetizationCounts;
};

