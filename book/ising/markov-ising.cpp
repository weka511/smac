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

MarkovIsing::MarkovIsing(int m,int n,bool wrapped) : N(m*n) {
			neighbours = new Neighbours(m,n,wrapped);
		 	sigma = new int[m*n]; 
		};

void MarkovIsing::prepare() {
	M = 0;
	E = 0;
	for (int i=0;i<N;i++) 
		sigma[i] = 2*(mt()%2) - 1;
	for (int i=0;i<N;i++)  {
		M += sigma[i];
		int h = get_field(i);
		E += sigma[i] * h;

	}
}	
	
void MarkovIsing::step(int k, float rr, float * Upsilon) {
	std::uniform_real_distribution<float> dt(0,1);
	int h = get_field(k);
	int deltaE = 2 * h * sigma[k];
	if (deltaE >= 0 and rr < Upsilon[deltaE/2]){
		sigma[k] *= -1;
		E += deltaE;
		M -= sigma[k];
		std::cout << "k=" <<k << ", E="<< E <<", M="<<M<<std::endl;
	}
}


void MarkovIsing::run() {
	std::uniform_real_distribution<float> dt(0,1);
	std::uniform_int_distribution<int> d(0,N-1);
	float Upsilon[5]; 
	for (int E=0;E<=8;E++)
		Upsilon[E/2] = exp(-beta*E);
	std::cout <<Upsilon[0]<<","<<Upsilon[1]<<","<<Upsilon[2]<<","<<Upsilon[3]<<","<<Upsilon[4]<<","<<std::endl;
	for (int i=0;i<10000;i++)
		step(d(mt),dt(mt),Upsilon);

}

int MarkovIsing::get_field(int i) {
	int h = 0;
	for (int j=0;j<2*neighbours->get_d() + 1;j++) 
		if (neighbours->get_neighbour(i,j) > -1)
			h += sigma[neighbours->get_neighbour(i,j)];
	return h;
}
MarkovIsing::~MarkovIsing(){
	delete neighbours;
	delete [] sigma;
};

int main(int argc, char **argv) {
	std::cout << "Hello Markov" << std::endl;
	MarkovIsing markov(6,6,true);
	markov.prepare();
	markov.run();

}