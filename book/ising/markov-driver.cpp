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
 *  This is the Driver program for MCMC Ising. It parses the command line
 *  arguments, then executes Markov Ising as many times as required.
 */
 
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>
#include <chrono>

#include "markov-ising.hpp"
#include "markov-driver.hpp"

using namespace std;

/**
 * Parse command line parameters and execute MCMC model.
 */
int main(int argc, char **argv) {
	int c;
	int n = -1;
	bool wrapped  = false;
	string path   = "markov-out.txt";
	int frequency = 0;
	float beta = -1;
	int iterations = 100000;
	int nruns = 1;
	int burn_in = -1;
	while ((c = getopt (argc, argv, "n:wo:f:b:i:r:u:")) != -1)
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
			case 'r':
				nruns = atoi(optarg);
				break;
			case 'u':
				burn_in = atoi(optarg);
				break;
			default: 
				std::cout << "Unrecognized option: " << char(c) << std::endl;
				exit(1);
		}

	if (burn_in<0)
		burn_in = iterations/10;
	
	if (n>0 && beta>0){
		std::cout <<"n="<<n << ", periodic=" << wrapped <<", beta="<< beta<<", iterations=" 
				<<iterations <<", nruns="<< nruns << ",burn in="<< burn_in<<std::endl;
		execute(path, n, wrapped,  beta, iterations, nruns, frequency,burn_in);
	} else{
		std:cout<< "Both n and beta need to be specified" << std::endl;
		exit(1);
	}
}

int execute(const string path,
			const int n,
			const bool wrapped,
			const float beta,
			const int iterations,
			const int nruns,
			const int frequency,
			const int burn_in){
	auto start = std::chrono::steady_clock::now();
	ofstream out;
	out.open (path);
	MarkovIsing markov(n,n,wrapped,out,beta,nruns);
	
	for (int i=0;i<nruns;i++) 
		markov.run(iterations,frequency,i,burn_in);
		
	markov.dump();
	out.close();
	
	auto end = std::chrono::steady_clock::now();
	int64_t elapsed = chrono::duration_cast<chrono::seconds>(end - start).count();
	std:cout<< "Elapsed time="<<elapsed <<" seconds, average="<< ((float)elapsed)/nruns << " sec." << std::endl;
	return 0;
}