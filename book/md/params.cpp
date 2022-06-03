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

 using namespace std;
 #include "params.hpp"
 
 /**
  * Create ParameterSet from command line parameters
  */
 ParameterSet::ParameterSet(int argc, char **argv){
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
			{"history",   required_argument,    0,  'h'},
			{0, 				0, 				0, 	0}
	};	

	int c;
	int option_index = 0;
	while ((c = getopt_long (argc, argv, "N:n:hd:M:f:L:V:s:o:r:y:",long_options, &option_index)) != -1)
		_extract(c);
	 
 }
 
/**
 *   Used to extract one command line parameter and store in Parameter Set
 */
 void ParameterSet::_extract(const int c) {
	 try {	switch(c) {
				case 'N':
					N = stoi(optarg);
					break;
				case 'n':
					n = stoi(optarg);
					break;
				case 'd':
					d = stoi(optarg);
					break;
				case 's':
					sigma = stof(optarg);
					break;
				case 'M':
					M = stoi(optarg);
					break;
				case 'f':
					freq = stoi(optarg);
					break;
				case 'o':
					output_path = optarg;
					break;
				case 'r':
					restart      = true;
					restart_path = optarg;
					break;
				case 'h':
					_help();
					exit(SUCCESS);
				case 'y':
					history      = true;
					history_path = optarg;
					break;
				default:
					parsing_error   = true;
					return;
		}
	 } catch(std::exception const & e){
		 char arg = c;
		 cerr<<"error parsing argument: " << arg << " " << optarg << " " << e.what() <<endl;
		 parsing_error   = true;
	 }

}

 	/**
	 *  Used to extract one command line parameter and store in Parameter Set
	 */
int ParameterSet::load(const string line){
	const int pos = line.find("=");
	if (pos>-1)
		_load(line.substr(0,pos),line.substr(pos+1));
	return pos;
}
	
/**
 * Used to load one command line parameter from stored file
 */
	 
void ParameterSet::_load(const string key, const string value) {
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
	else if (key=="wall_collisions")
		wall_collisions = stoi(value);
	else if (key=="pair_collisions")
		pair_collisions = stoi(value);
}

/**
 *  Used to save all parameters
 */
void ParameterSet::save(ofstream& output,Configuration& configuration) {
	output << "N="               <<epoch                                   << endl;
	output << "n="               <<n                                       << endl;
	output << "d="               <<d                                       << endl;
	output << "M="               <<M                                       << endl;
	output << "L="               <<L                                       << endl;
	output << "V="               <<V                                       << endl;
	output << "sigma="           <<sigma                                   << endl;
	output << "wall_collisions=" <<  configuration.get_n_wall_collisions() << endl;
	output << "pair_collisions=" <<  configuration.get_n_pair_collisions() << endl;
}

/**
 * Display help text.
 */
void ParameterSet::_help() {
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
