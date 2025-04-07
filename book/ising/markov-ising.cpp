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

#include "gray.hpp"
#include "nbr.hpp"
#include "markov-ising.hpp"

using namespace std;

MarkovIsing::MarkovIsing(int m,int n,bool wrapped) : N(m*n) {
			neighbours = new Neighbours(m,n,wrapped);
			sigma = new int[m*n];
		};

void MarkovIsing::prepare() {
	for (int i=0;i<N;i++) 
		sigma[i] = 2*(mt()%2)-1;
}		
void MarkovIsing::step() {


}



MarkovIsing::~MarkovIsing(){
	delete neighbours;
	delete [] sigma;
};

int main(int argc, char **argv) {
	std::cout << "Hello Markov" << std::endl;
	MarkovIsing markov(6,6,true);
	markov.prepare();
	markov.step();
}