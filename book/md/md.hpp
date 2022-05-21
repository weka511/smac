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

#ifndef _MD_HPP_
#define _MD_HPP_

#include "particle.hpp"
#include "configuration.hpp"

enum ParserState {
	START     = 0, 
	PARTICLES = 2
};


/**
 * This class looks after command line paramters.
 */ 
class ParameterSet {
  public:
	int    N               = 10000;
	int    n               = 100;
	int    d               = 2;
	int    M               = 100;
	int    freq            = 100;
	double L               = 1;
	double V               = 1;
	double sigma           = 0.01;
	bool   restart         = false;
	string output_path     = "./foo.csv";
	string restart_path;
	int    wall_collisions = 0;
	int    pair_collisions = 0;
	int    epoch           = 0;	
	
	void extract(int c);
	
	void load(string key, string value);
	
	void save(ofstream& output,Configuration& configuration);
	/**
	 * Display help text.
	 */
	void help();
};	

/**
 *   Check to see whether user wants to terminate program.
 */
bool killed(string kill_file="kill.txt");

/**
 *   Check to see whether a specified file exists
 */
bool file_exists (const char *filename);

/**
 *  Drive configuration forward a specified number of epochs
 */
int evolve( Configuration& configuration,
			string         output_path, 
			int            status, 
			ParameterSet   params,
			string         check_path = "check.csv",
			const int      epoch = 0);

/**
 *    Save configuration to specified file
 */
void save(  string    output_path,
			Configuration& configuration,
			int            epoch, 
			ParameterSet & params);


#endif

