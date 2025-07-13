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
 


#include <getopt.h>
#include <iostream>
#include "params.hpp"

using namespace std;
 
 /**
  * Create ParameterSet from command line parameters
  */
 ParameterSet::ParameterSet(int argc, char **argv){
	 struct option long_options[] = {
			{"iterations",required_argument,	0, 	'N'},
			{"particles", required_argument,	0, 	'n'},
			{"sigma",     required_argument,	0, 	's'},
			{"help",  	  no_argument, 		    0, 	'h'},
			{"freq",      required_argument,	0, 	'f'},
			{"Length",    required_argument,	0, 	'L'},
			{"Velocity",  required_argument,	0, 	'V'},
			{"Attempts",  required_argument,	0, 	'm'},
			{"sample",    required_argument,    0,  'p'},
			{"dsample",   required_argument,    0,  'd'},
			{0, 				0, 				0, 	0}
	};	

	auto c = 0;
	auto option_index = 0;
	while ((c = getopt_long (argc, argv, "N:n:hd:M:f:L:V:s:o:r:y:",long_options, &option_index)) != -1)
		_extract(c);
	 
 }
 
/**
 *   Used to extract one command line parameter and store in Parameter Set
 */
 void ParameterSet::_extract(const int c) {
	 try {
		 switch(c) {
			case 'f':
				freq = stoi(optarg);
				break;
			case 'L':
				L = stod(optarg);
				break;
			case 'V':
				V = stod(optarg);
				break;
			case 'm':
				m = stoi(optarg);
				break;
			case 'N':
				N = stoi(optarg);
				break;
			case 'n':
				n = stoi(optarg);
				break;
			case 's':
				sigma = stod(optarg);
				break;
			case 'p':
				sample_file = optarg;
				break;	
			case 'd':
				dt_sample = stod(optarg);
				break;	
			case 'h':
				_help();
				exit(0);
			default:
				_parsing_error = true;
				return;
		}
	 } catch(exception const & e){
		 char arg = c;
		 cerr<<"error parsing argument: " << arg << " " << optarg << " " << e.what() <<endl;
		 _parsing_error  = true;
	 }

}


/**
 * Display help text.
 */
void ParameterSet::_help() {
	cout << "Molecular Dynamics"                                << endl        << endl;
	cout << "    Parameters"                                                   << endl;
	cout << "\tN\tNumber of iterations\t\t\t\t"                 << N           << endl;
	cout << "\tn\tNumber of spheres\t\t\t\t"                    << n           << endl;
	cout << "\tf\tFrequency\t\t\t\t\t"                     		<< freq        << endl;
	cout << "\ts\tRadius of sphere\t\t\t\t"                     << sigma       << endl;
	cout << "\tL\tLength\t\t\t\t\t\t"                    		<< L           << endl;
	cout << "\tV\tInitial velocity\t\t\t\t"                     << V           << endl;
	cout << "\tm\tNumber of attempts\t\t\t\t"                   << m           << endl;
	cout << "\tm\tsample file name\t\t\t\t"                     << sample_file << endl;
	cout << "\tm\tInterval between samples\t\t\t\t"             << dt_sample   << endl;
}
