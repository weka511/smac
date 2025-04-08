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
 *
 *     Driver program for MCMC Ising
 */
 
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>

#include "markov-ising.hpp"

using namespace std;

/**
 * Parse command line parameters and execute MCMC model.
 */
int main(int argc, char **argv) {
	int c;
	int n = 4;
	bool wrapped  = false;
	string path   = "markov-out.txt";
	int frequency = 0;
	float beta = 2.0;
	int iterations = 100000;
	
	while ((c = getopt (argc, argv, "n:wpo:f:b:i:")) != -1)
		switch(c) {
			case 'n':
				n = atoi(optarg);
				break;
			case 'f':
				frequency = atoi(optarg);
				break;
			case 'w':
				wrapped = true;
				break;
			case 'o':
				path = optarg;
				break;
			case 'b':
				beta = atof(optarg);
				break;
			case 'i':
				iterations = atoi(optarg);
				break;
			default: 
				abort();
		}

	std::cout <<"n="<<n << ", periodic=" << wrapped <<", beta="<< beta<<", iterations=" <<iterations << std::endl;

	ofstream out;
	out.open (path);
	MarkovIsing markov(n,n,wrapped,out,beta=beta);
	markov.run(iterations,frequency);
	out.close();
	
	return 0;
}