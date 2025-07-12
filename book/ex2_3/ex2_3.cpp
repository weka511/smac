/**
 * Copyright (C) 2025 Simon Crase
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
 *
 * Molecular dynamics simulation for hard disks or hard spheres, as described
 * in Statistical Mechanics: Algorithms and Computations, by Werner Krauth,
 * ISBN 978-0-19-851535-7.
 */

#include <iostream>
#include "params.hpp"
#include "EventDisks.hpp"

using namespace std;

int main(int argc, char **argv) {
	ParameterSet params(argc, argv);
	if (params.has_parsing_error()) {
		cerr << "Terminating because of errors" << endl;
		exit(1);
	}
	
	cout << "ex2_3: " << VERSION << endl;
	cout << "n="<< params.n << ", L=" <<params.L<< ", V=" <<params.V<< ", sigma=" <<params.sigma<< ", m=" <<params.m<< endl;
	cout << "N=" << params.N << endl;
	try {
		EventDisks ed(params.n,params.L,params.V,params.sigma,params.m);
		for (int i=0;i<params.N;i++){
			if (i%params.freq==0)
				cout << "Epoch " << i << ", T=" << ed.get_time()<<endl;
			ed.event_disks();
		}
	}  catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }
}