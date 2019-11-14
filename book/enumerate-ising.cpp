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
 
#include <iostream>
#include <map>
#include <utility>
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>

#include "gray.hpp"
#include "nbr.hpp"
#include "enumerate-ising.hpp"

using namespace std;


/**
 * Main program. 
 */
int main(int argc, char **argv) {
	int c;
	int n         = 4;
	bool wrapped  = false;
	bool progress = false;
	string path   = "out.txt";
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
				break;
			case 'p':
				progress = true;
				break;
			default:
				abort();
	}

	ofstream out;
	out.open (path);
	out<<"n="<<n<<endl;
	enumerate_ising(n,out,wrapped,progress);
	out.close();
	return 0;
}

/**
 *  Compute molecular field at location k, i.e.
 *  the total contribution of all neighbours
 */
int get_field(int sigma[],int k,int n,bool wrapped){
	int h=0;
	for (int i=1;i<=4;i++) {
		const int j = nbr(k,i,n,wrapped);
		if (j>-1)
			h+=sigma[j-1];
	}

	return h;
}

void enumerate_ising(int n,ofstream &out,bool wrapped,bool progress){
	map<pair<int,int>, long long int> Ns;
	const int N = n*n;

	Gray gray(N,progress ? 100000000LL : 0LL);

	int sigma[N];
	for (int i=0;i<N;i++)
		sigma[i]=-1;
	
	int E = -2*N;
	int M = -N;
	pair<int,int> key(E,M);
	Ns[key] = 2;
 	while (true) {
		int k = gray.next();
		if (k==-1) break;
		int h      = get_field(sigma,k,n,wrapped);
		E          += 2* sigma[k-1]*h;
		sigma[k-1] *= -1;
		M          += 2*sigma[k - 1]; 
		pair<int,int> key(E,M);
		if (Ns.find(key)==Ns.end()) Ns[key]=0;
		Ns[key]    += 2;
	}
	
	out << "E,M,N" << endl;
	for (map<pair<int,int>, long long int>::iterator it = Ns.begin();it!=Ns.end();it++){
		const pair<int,int> key = it->first;
		const int E = key.first;
		const int M = key.second;	
		out << E << ", " << M<< ", " << it->second<< endl;
	}
}










