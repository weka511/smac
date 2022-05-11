/**
 * Copyright (C) 2019 Greenweaves Software Limited
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

#include <cstdlib> 
#include <iostream>
#include <map>
#include <utility>
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>
#include "md.hpp"
using namespace std;


/**
 * Main program. 
 */
int main(int argc, char **argv) {
	int N = 100;
	int n = 10;
	int d = 2;
	int c;
	double L = 1;
	while ((c = getopt (argc, argv, "N:n:")) != -1)
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
			default:
				abort();
	}

	double X[n][d];
	
	for (int i=0;i<n;i++)
		for (int j=0;j<d;j++){
		X[i][j]=2*L*(double)rand()/(double)RAND_MAX-L;
		cout << X[i][j] <<endl;
		}
/* 	for (int epoch=0;epoch<N;epoch++) {
		cout << epoch <<endl;
	} */
	return 0;
	
}














