/**
 * Copyright (C) 2025 Simon Crase
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

#include <string>

using namespace std;

 /**
 * This class parses command line paramters.
 */ 
class ParameterSet {
	
  public:
	/**
	 *   Number of iterations
	 */
	int N = 1000000;
	
	/**
	 *    Number of spheres.
	 */
	int n = 100;
	
	/**
	 *  Radius of each sphere 
	 */
	float sigma = 1.0/32;
	
	/**
	 *   Interval between tracing statements.
	 */
	int freq = 10000;
	
	/**
	 *   Length of one side
	 */
	double L = 1.0;
	
	/**
	 *   Limit for veloecities when we initialize
	 */
	double V = 1.0;
	
	/**
	 *   Number of attempts to create configuratio
	 */
	double m = 500;
	
	/**
	 *   Time interval between samples
	 */
	double dt_sample = 1.0;
	
	/**
	 *   File name for storing samples
	 */
	string sample_file = "samples.csv";
	
	/**
	 *  Create ParameterSet from command line parameters
	 */
	ParameterSet(int argc, char **argv);
	
	/**
	 *  Indicates that an error occured while parsing command line parameters
	 */
	bool has_parsing_error() {return _parsing_error;};
	
  private:	
  
  	/**
	 *  Indicates that an error occured while parsing command line parameters
	 */
  	bool _parsing_error = false;
	
	/**
	 * Parse one command liune parameter.
	 */
	void _extract(const int c);
  
	/**
	 * Display help text.
	 */
	void _help();
};

#endif //_PARAMS_HPP_
	