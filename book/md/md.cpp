/**
 * Copyright (C) 2022 Greenweaves Software Limited
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


#include <cstdlib> 
#include <fstream>
#include <getopt.h>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <sys/stat.h> 
#include <vector>
#include "md.hpp"

using namespace std;


/**
 * Main program. 
 */
int main(int argc, char **argv) {
	int         N           = 10000;
	int         n           = 100;
	int         d           = 2;
	int         M           = 100;
	int         freq        = 100;
	bool        restart     = false;
	double      L           = 1;
	double      V           = 1;
	double      sigma       = 0.01;
	std::string output_path = "./foo.csv";
	std::string restart_path;
	
	struct option long_options[] = {
			{"epochs",    required_argument,	0, 	'N'},
			{"particles", required_argument,	0, 	'n'},
			{"help",  	  no_argument, 		    0, 	'h'},
			{"dimension", required_argument, 	0, 	'd'},
			{"attempts",  required_argument, 	0, 	'M'},
			{"freq",  	  required_argument, 	0, 	'f'},
			{"length",    required_argument, 	0, 	'L'},
			{"Velocity",  required_argument, 	0, 	'V'},
			{"sigma",  	  required_argument, 	0, 	's'},
			{"output",    required_argument,    0,  'o'},
			{"restart",   required_argument,    0,  'r'},
			{0, 				0, 				0, 	0}
	};	
	
	
	int c;
	int option_index = 0;
	while ((c = getopt_long (argc, argv, "N:n:hd:M:f:L:V:s:o:r:",long_options, &option_index)) != -1)
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
			case 'f':
				freq = atoi(optarg);
				break;
			case 'o':
				output_path = optarg;
				break;
			case 'r':
				restart      = true;
				restart_path = optarg;
				break;
			case 'h':
				help( N,  n,	 d ,	 M ,	 freq,  restart, L,  V,	 sigma ,  output_path, restart_path);
				exit(SUCCESS);
			default:
				abort();
	}

	if (std::ifstream(output_path)){
		std::cerr << "Output file " << output_path << " already exists" << endl;
		exit(EXIT_FAILURE);
	}
	
	int status;
	if (restart) {
		ifstream restart_stream(restart_path);
		string line;
		int line_number = 0;
		std::vector<Particle*> particles;
		while (getline(restart_stream,line)){
			if (line_number<7){
				std::string delimiter = "=";
				int pos = line.find(delimiter);
				std::string token = line.substr(0, pos);
				std::string value = line.substr(pos+1);
				cout<<token<<" :: "<< value << endl;
				switch (line_number){
					case 0:
						N = std::stoi(value);
						break;
					case 1:
	 					n =std::stoi(value);
						break;
					case 2:
						d=std::stoi(value);
						break;
					case 3:
						M = std::stoi(value);
						break;
					case 4:
						L = std::stoi(value);
						break;
					case 5:
						V = std::stoi(value);
						break;
					case 6:
						sigma = std::stod(value);
				}
			}
			if (line_number>7){
				double values[4];
				std::string delimiter = ",";
				int start = 0;
				for (int i=0; i<4;i++) {
					int pos = line.find(delimiter, pos=start);
					std::string token = line.substr(start, pos-start);
					start = pos+1;
					values[i] = stod(token);
				}
				Particle* p = new Particle(d,values);
				particles.push_back(p);
			}
			line_number++;
		}
		Configuration configuration(n,d,sigma,particles);
		status = evolve(configuration, N,  n, d,  M, L,  V,  sigma,  output_path,  status, freq);
	} else {
		Configuration configuration(n,d,sigma);
		status = configuration.initialize(M);
		status = evolve(configuration, N,  n, d,  M, L,  V,  sigma,  output_path,  status, freq);
	}


	return status;
}

int evolve(Configuration& configuration,int N, int n,int d, int M, 
		double L, double V, double sigma, std::string output_path, int status, int freq) {
	
		for  (int i=0; SUCCESS==status && i<N && !killed();i++) {
		if (i%freq ==0)
			cout << "Epoch " << (i+1) << ", "<<
		    configuration.get_n_pair_collisions() << " pair collisions, " <<
			configuration.get_n_wall_collisions() << " wall collisions, " << endl;
		status = configuration.event_disks();
	}
	ofstream output(output_path);
	output << "N="<<N         << endl;
	output << "n="<<n         << endl;
	output << "d="<<d         << endl;
	output << "M="<<M         << endl;
	output << "L="<<L         << endl;
	output << "V="<<V         << endl;
	output << "sigma="<<sigma << endl;
	configuration.dump(output);
	output.close();
	return status;
}



bool killed(std::string kill_file){
	bool kill = file_exists(kill_file.c_str());
	if (kill) {
		cout << "Killed" << endl;
		remove(kill_file.c_str());
	}
	return kill;
}

void help(int N, int n,	int d ,	int M ,	int freq, bool restart,
			double L, double V,	double sigma,  std::string output_path, std::string restart_path) {


	cout << "Molecular Dynamics"                                 <<endl<<endl;
	cout << "    Parameters"                                     << endl;
	cout << "\tN\tNumber of iterations\t\t\t\t"                  << N<<endl;
	cout << "\tn\tNumber of spheres\t\t\t\t"                     <<n <<endl;
	cout << "\td\tDimension of box\t\t\t\t"                      <<d <<endl;
	cout << "\tM\tNumber of attempts to build configuration\t"   <<M<<endl;
	cout << "\tfreq\tFrequency for indicating progress\t\t"      <<freq<<endl;
	cout << "\trestart\tSet if Configuration is to be restarted" <<endl;
	cout << "\tL\tLength of side of box\t\t\t\t"                 <<L<<endl;
	cout << "\tV\tNormalizer of initial velocity\t\t\t"          <<V<<endl;
	cout << "\tsigma\tRadius of sphere\t\t\t\t"                  <<sigma<<endl;
	cout << "\toutput_path" <<endl;
	cout << "\trestart_path" <<endl;
}















