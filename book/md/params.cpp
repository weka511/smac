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
 

#include <fstream>
#include <getopt.h>
#include <iostream>
#include <limits>
#include <random>
#include <string>

 using namespace std;
 #include "params.hpp"
 
 void ParameterSet::extract(int c) {
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
			help();
			exit(SUCCESS);
		default:
			abort();
	}
}

void ParameterSet::load(string key, string value) {
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
void ParameterSet::help() {
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
