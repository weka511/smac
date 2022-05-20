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

#include <cassert>
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

enum ParserState {
	START     = 0, 
	PARTICLES = 2
};
int         N           = 10000;
int         n           = 100;
int         d           = 2;
int         M           = 100;
int         freq        = 100;

double      L           = 1;
double      V           = 1;
double      sigma       = 0.01;
	
/**
 * Main program. 
 */
int main(int argc, char **argv) {

	bool        restart = false;
	string output_path  = "./foo.csv";
	string restart_path;
	
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
				help( restart, output_path, restart_path);
				exit(SUCCESS);
			default:
				abort();
	}

	if (std::ifstream(output_path)){
		std::cerr << "Output file " << output_path << " already exists" << endl;
		exit(EXIT_FAILURE);
	}
	
	int status = UNDEFINED;

	if (restart) {
		ParserState parser_state = START;
		int epoch  = 0;
		ifstream restart_stream(restart_path);
		string line;
		vector<Particle*> particles;
		while (getline(restart_stream,line)){
			int pos;
			switch(parser_state){
				case START:
					pos = line.find("=");
					if (pos>-1) {
						string key = line.substr(0,pos);
						string value = line.substr(pos+1);
						
						if (key=="N")
							epoch = stoi(value);
						else if (key=="n")
							n = stoi(value);
						else if (key=="d")
							d = stoi(value);
						else if (key=="M")
							M = stoi(value);
						else if (key=="L")
							L = stoi(value);
						else if (key=="V")
							V = stoi(value);
						else if (key=="sigma")
							sigma = stod(value);
					} else
						parser_state = PARTICLES;
					break;
				case PARTICLES:{
						double values[2*d];
						string delimiter = ",";
						int start = 0;
						for (int i=0; i<2*d;i++) {
							int pos = line.find(delimiter, pos=start);
							string token = line.substr(start, pos-start);
							start = pos+1;
							values[i] = stod(token);
						}
			
						particles.push_back(new Particle(d,values));
				}	
				break;
			}
		}
		assert(n==particles.size());
		cout << "Restarting from Epoch " <<epoch <<", max=" << N<< endl;
		Configuration configuration(n,d,sigma,particles);
		status = SUCCESS;
		status = evolve(configuration, output_path,  status,  "check.csv", epoch);
	} else {
		Configuration configuration(n,d,sigma);
		status = configuration.initialize(M);
		status = evolve(configuration,  output_path,  status);
	}

	return status;
}


/**
 *  Drive configuration forward a specified number of epochs
 */
int evolve(Configuration& configuration,
			string         output_path, 
			int            status, 
			string         check_path,
			const int      epoch) {
	
	for  (int i=epoch; SUCCESS==status && i<N && !killed();i++) {
		if (i%freq ==0) {
			cout << "Epoch " << (i+1) << ", "<<
		    configuration.get_n_pair_collisions() << " pair collisions, " <<
			configuration.get_n_wall_collisions() << " wall collisions, " << endl;
			if (file_exists(check_path.c_str())){
				std:string cp = "cp " + check_path + " " + check_path+"~";
				system (cp.c_str());
			}
			save(check_path, configuration,i);
		}
			
		status = configuration.event_disks();
	}

	save(output_path, configuration,N);
	
	return status;
}

/**
 *    Save configuration to specified file
 */
void save(string output_path,
		Configuration& configuration,
		const int epoch) {
	ofstream output(output_path);
	output << "N="               <<epoch                                   << endl;
	output << "n="               <<n                                       << endl;
	output << "d="               <<d                                       << endl;
	output << "M="               <<M                                       << endl;
	output << "L="               <<L                                       << endl;
	output << "V="               <<V                                       << endl;
	output << "sigma="           <<sigma                                   << endl;
	output << "wall_collisions=" <<  configuration.get_n_wall_collisions() << endl;
	output << "pair_collisions=" <<  configuration.get_n_pair_collisions() << endl;
	configuration.dump(output);
	output.close();
}

/**
 *   Check to see whether a specified file exists
 */
bool file_exists (const char *filename) {
  struct stat   buffer;   
  return (stat (filename, &buffer) == 0);
}

/**
 *   Check to see whether user wants to terminate program.
 */
bool killed(string kill_file){
	const bool kill_file_found = file_exists(kill_file.c_str());
	if (kill_file_found) {
		cout << "File " <<kill_file << " found. Terminating program." << endl;
		remove(kill_file.c_str());
	}
	return kill_file_found;
}

/**
 * Display help text.
 */
void help(	bool   restart,
			string output_path,
			string restart_path) {
	cout << "Molecular Dynamics"                                 << endl        << endl;
	cout << "    Parameters"                                                    << endl;
	cout << "\tN\tNumber of iterations\t\t\t\t"                  << N           << endl;
	cout << "\tn\tNumber of spheres\t\t\t\t"                     << n           << endl;
	cout << "\td\tDimension of box\t\t\t\t"                      << d           << endl;
	cout << "\tM\tNumber of attempts to build configuration\t"   << M           << endl;
	cout << "\tfreq\tFrequency for indicating progress\t\t"      << freq        << endl;
	cout << "\tL\tLength of side of box\t\t\t\t"                 << L           << endl;
	cout << "\tV\tNormalizer of initial velocity\t\t\t"          << V           << endl;
	cout << "\tsigma\tRadius of sphere\t\t\t\t"                  << sigma       << endl;
	cout << "\toutput\tPath name for output file\t\t\t"          << output_path << endl;
	cout << "\trestart\tRestart run from file\t\t\t"                            << endl;
}















