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
 
#ifndef _PARAMS_HPP_
#define _PARAMS_HPP_

#include "configuration.hpp"

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
    bool   history         = false;
    string history_path;	
	bool   parsing_error   = false;
	/**
	 *  Create ParameterSet from command line parameters
	 */
	ParameterSet(int argc, char **argv);
	
	/**
	 * Save Paramter set
	 */
	void save(ofstream& output,Configuration& configuration);
 
  	/**
	 *  Used to extract one command line parameter and store in Parameter Set
	 */
	int load(const string line);
	
  private:	
	void _load(const string key, const string value);
	
 
	/**
	 * Display help text.
	 */
	void _help();
	
	/**
	 *  Used to extract one command line parameter and store in Parameter Set
	 */
	void _extract(const int c);
};

#endif
	