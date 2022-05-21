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
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <sys/stat.h> 
#include <vector>

#include "params.hpp"
#include "md.hpp"

using namespace std;

/**
 * Main program. 
 */
int main(int argc, char **argv) {
	ParameterSet params(argc, argv);
	
	if (ifstream(params.output_path)){
		cerr << "Output file " << params.output_path << " already exists" << endl;
		exit(EXIT_FAILURE);
	}
	
	int status = UNDEFINED;

	if (params.restart) {
		ParserState       parser_state = START;
		ifstream          restart_stream(params.restart_path);
		string            line;
		vector<Particle*> particles;

		while (getline(restart_stream,line)){
			int    pos;
			double values[2*params.d];
			int    start = 0;
			switch(parser_state){
				case START:
					if (params.load(line)==-1)
						parser_state = PARTICLES;
					break;
				case PARTICLES: 
					start = 0;
					for (int i=0; i<2*params.d;i++) {
						int pos      = line.find(",", pos=start);
						string token = line.substr(start, pos-start);
						start        = pos+1;
						values[i]    = stod(token);
					}
					particles.push_back(new Particle(params.d,values));
					
				break;
			}
		}

		assert(params.n==particles.size());
		cout << "Restarting from Epoch " <<params.epoch <<", max=" << params.N<< endl;
		Configuration configuration(params.n,params.d,params.sigma,particles,params.wall_collisions,params.pair_collisions);
		status = SUCCESS;
		status = evolve(configuration, params.output_path,  status,  params, "check.csv", params.epoch);
	} else {
		Configuration configuration(params.n,params.d,params.sigma);
		status = configuration.initialize(params.M);
		status = evolve(configuration,  params.output_path,  status, params);
	}

	return status;
}


/**
 *  Drive configuration forward a specified number of epochs
 */
int evolve(Configuration& configuration,
			string         output_path, 
			int            status,
			ParameterSet   params,
			string         check_path,
			const int      epoch) {
	
	for  (int i=params.epoch; SUCCESS==status && i<params.N && !killed();i++) {
		if (i%params.freq ==0) {
			cout << "Epoch " << (i+1) << ", "<<
		    configuration.get_n_pair_collisions() << " pair collisions, " <<
			configuration.get_n_wall_collisions() << " wall collisions, " << endl;
			if (file_exists(check_path.c_str())){
				string cp = "cp " + check_path + " " + check_path+"~";
				system (cp.c_str());
			}
			save(check_path, configuration,i,params);
		}
			
		status = configuration.event_disks();
	}

	save(output_path, configuration,params.N,params);
	
	return status;
}

/**
 *    Save configuration to specified file
 */
void save(string           output_path,
			Configuration& configuration,
			const int      epoch,
			ParameterSet & params) {
	ofstream output(params.output_path);
	params.epoch = epoch;
	params.save(output,configuration);
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















