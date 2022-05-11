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

#include <vector>
#include <cstdlib> 
#include <iostream>
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include "md.hpp"
using namespace std;


/**
 * Main program. 
 */
int main(int argc, char **argv) {
	int N = 100;
	int n = 100;
	int d = 2;
	int M = 100;
	int c;
	double L = 1;
	double V = 1;
	double sigma = 0.01;
	while ((c = getopt (argc, argv, "N:n:s:")) != -1)
		switch(c) {
			case 'N':
				N = atoi(optarg);
				break;
			case 'n':
				n = atoi(optarg);
				break;
			case 'd':
				d = atoi(optarg);
				break;
			case 's':
				sigma = atof(optarg);
				break;
			case 'M':
				M = atoi(optarg);
				break;
			default:
				abort();
	}

 
	Configuration configuration(n,d,sigma);
	if (SUCCESS==configuration.initialize(M))
		for (int i=0;i<N;i++)
			configuration.event_disks();
		
	return SUCCESS;
}

int Configuration::build_config(std::uniform_real_distribution<double> & distr,
								std::default_random_engine& eng){
	double L_reduced[3];
	for (int i=0;i<_d;i++)
		L_reduced[i] = L[i]-_sigma;
	for (int i=0;i<_n;i++) {
		_particles[i]->randomizeX(distr, eng, L_reduced);
		for (int j=0;j<i;j++) 
			if (_particles[i]->get_dist_sq(_particles[j])<4*_sigma*_sigma)
				return FAIL_DISKS_TOO_CLOSE;
	}
	for (int i=0;i<_n;i++)
		_particles[i]->randomizeV(distr, eng, V);
	return SUCCESS;
}
	
int Configuration::initialize(int n){
	std::random_device rd;
	std::default_random_engine eng(rd());
	std::uniform_real_distribution<double> distr(-1, 1);
	for (int i=0;i<n;i++){
		std::cout << i << std::endl;
		if (SUCCESS == build_config(distr,eng))
			return SUCCESS;
	}
	return FAIL_BUILD_CONFIG;
}

int Configuration::event_disks(){
	return SUCCESS;
}

















