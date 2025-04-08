/**
 * Copyright (C) 2025 Greenweaves Software Limited
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
 
#include <iostream>
#include <map>
#include <utility>
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>

#include "markov-ising.hpp"

using namespace std;

int main(int argc, char **argv) {
	int c;
	int n = 4;
	bool wrapped  = false;
	string path   = "markov-out.txt";
	while ((c = getopt (argc, argv, "n:wpo:")) != -1)
	switch(c) {
		case 'n':
			n = atoi(optarg);
			break;
		case 'w':
			wrapped = true;
			break;
		case 'o':
			path = optarg;
			break;
		default: 
			abort();
	}

	std::cout << "Hello Markov " << n <<std::endl;
	if (wrapped)
		std::cout <<"periodic" << std::endl;
	else
		std::cout <<"not periodic" << std::endl;
	ofstream out;
	out.open (path);
	MarkovIsing markov(n,n,wrapped,out);
	markov.run();
	out.close();
	return 0;
}