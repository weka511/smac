/**
 * Copyright (C) 2019-2025 Greenweaves Software Limited
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
#include <fstream>
#include <string>

using namespace std;

#include "enumerate-ising.hpp"



/**
 * Main program: enumerate states and calculate Energy and Magnetization.
 */
 
int main(int argc, char **argv) {
	int c;
	int n         = 4;
	bool wrapped  = false;
	bool progress = false;
	string path   = "out.txt";
	string periodic = "aperiodic";
	while ((c = getopt (argc, argv, "n:wpo:")) != -1)
		switch(c) {
			case 'n':
				n = atoi(optarg);
				break;
			case 'o':
				path = optarg;
				break;
			case 'w':
				wrapped = true;
				periodic = "periodic";
				break;
			case 'p':
				progress = true;
				break;
			default:
				abort();
	}

	ofstream out;
	out.open (path);
	out << "n=" << n << "," << periodic << endl;
	IsingEnumerator enumerator;
	enumerator.enumerate_ising(n,wrapped,progress);
	enumerator.output(out);
	out.close();
	return 0;
}
