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
 
#include <utility>
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#include "gray.hpp"
#include "nbr.hpp"
#include "enumerate-ising.hpp"

/**
 *  Compute molecular field at location k, i.e.
 *  the total contribution of all neighbours
 */
int get_field(vector<int> sigma,int k,int n,bool wrapped){
	int h=0;
	for (int i=1;i<=4;i++) {
		const int j = nbr(k,i,n,wrapped);
		if (j>-1)
			h+=sigma[j-1];
	}

	return h;
}

/**
 *  Enumerate energy levels
 */
void IsingEnumerator::enumerate_ising(const int n, const bool wrapped, const bool progress){

	const int N = n*n;

	Gray gray(N,progress ? 100000000LL : 0LL);

	vector<int> sigma;
	
	for (int i=0;i<N;i++)
		sigma.push_back(-1);//[i]=-1;
	
	int E = -2*N;
	int M = -N;
	pair<int,int> key(E,M);
	Ns[key] = 2;
 	while (true) {
		const int k = gray.next();
		if (k==-1) break;
		const int h = get_field(sigma,k,n,wrapped);
		E          += 2* sigma[k-1]*h;
		sigma[k-1] *= -1;
		M          += 2*sigma[k - 1]; 
		pair<int,int> key(E,M);
		if (Ns.find(key)==Ns.end()) Ns[key]=0;
		Ns[key]    += 2;
	}
}

/**
 *  Output E, M, and their count
 */
void IsingEnumerator::output(ofstream &out){	
	out << "E,M,N" << endl;
	for (map<pair<int,int>, long long int>::iterator it = Ns.begin();it!=Ns.end();it++){
		const pair<int,int> key = it->first;
		const int E = key.first;
		const int M = key.second;	
		out << E << ", " << M<< ", " << it->second<< endl;
	}
}

/**
 *  Compute molecular field at location k, i.e.
 *  the total contribution of all neighbours
 */
int IsingEnumerator::get_field(const vector<int> sigma, const int k, const int n, const bool wrapped){
	int h=0;
	for (int i=1;i<=4;i++) {
		const int j = nbr(k,i,n,wrapped);
		if (j>-1)
			h+=sigma[j-1];
	}

	return h;
}











