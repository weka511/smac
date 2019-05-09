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
#include "gray.hpp"
#include "nbr.hpp"

using namespace std;

void enumerate_ising(int n);

/**
 * Main program. 
 */
int main(int argc, char **argv) {
	int n=2;
	cout<<"Enumerate Ising for N="<<n<<endl;
	enumerate_ising(n);
}

int field(int* sigma,int k,int n){
	int h=0;
	for (int i=0;i<4;i++) {
		const int j = nbr(k,i,n);
		if (j>-1)
			h+=sigma[j-1];
	}
	return h;
}

void enumerate_ising(int n){
	const int N = n*n;
	Gray gray(N);
	int Ns[2*N+1];
	for (int i=0;i<2*N+1;i++)
		Ns[i]=0;
	int sigma[N];
	for (int i=0;i<N;i++)
		sigma[i]=0;
	
	int E = -N;
	Ns[N+E]=2;
 	while (true) {
		int k = gray.next();
		cout << k << endl;
		if (k==-1)
			return;
		int h = field(sigma,k,n);
		cout << __LINE__ << endl;
		E+=2+sigma[k-1]*h;
			cout << __LINE__ << endl;
		Ns[E+N]+=2;
			cout << __LINE__ << endl;
		sigma[k-1]*=(-1);
		cout << __LINE__ << endl;
	}
	for (int i=0;i<2*N+1;i++) {
		int E = i-N;
		if (Ns[i]>0)
			cout << E << ", " << Ns[i] << endl;
	} 
}










