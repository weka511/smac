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
#include <getopt.h>
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
	while ((c = getopt (argc, argv, "n:wp")) != -1)
		switch(c) {
			case 'n':
				n = atoi(optarg);
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

	cout<<"Enumerate Ising for n="<<n<<" "<<wrapped<<endl;
	enumerate_ising(n,wrapped,progress);
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

void enumerate_ising(int n,bool wrapped,bool progress){
	map<int, long long int> Ns;
	const int N = n*n;
	cout<<"Enumerate Ising for N="<<N<<endl;
	Gray gray(N,progress ? 100000000LL : 0LL);

	int sigma[N];
	for (int i=0;i<N;i++)
		sigma[i]=-1;
	
	int E = -2*N;
	Ns[E] = 2;
 	while (true) {
		int k = gray.next();
		if (k==-1) break;
		int        h = get_field(sigma,k,n,wrapped);
		E          += 2* sigma[k-1]*h;
		if (Ns.find(E)==Ns.end()) Ns[E]=0;
		Ns[E]    += 2;
		sigma[k-1] *= -1;
	}
	

	cout << endl;
	for (map<int, long long int>::iterator it = Ns.begin();it!=Ns.end();it++)
			cout << it->first << ", " << it->second<< endl;
	 
}










