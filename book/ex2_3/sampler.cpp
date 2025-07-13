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
 * MERCHANTABILITY or FITNESS FOR A file forPARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>
 *
 * Molecular dynamics simulation for hard disks or hard spheres, as described
 * in Statistical Mechanics: Algorithms and Computations, by Werner Krauth,
 * ISBN 978-0-19-851535-7. This program performs the calculations, and the data
 * in the outout files are analyzed by md-plot.py.
 */

#include <iostream>
#include <array>
#include <memory>
#include <stdexcept>
#include "sampler.hpp"

using namespace std;

/**
 *   Create file for recording positions and velocities.
 */
Sampler::Sampler(int n,string file_name) :_n(n){
	_outputFile.open(file_name);
	if (!_outputFile.is_open())
        throw runtime_error( "error: Unable to open file.");
}

/**
 * Sample configuration at a specified time.
 */
void Sampler::sample(double t,unique_ptr<double[][3]>& x,unique_ptr<double[][3]>& v) {
	for (int i=0;i<_n;i++)
		_outputFile << t << "," << x[i][0] << "," << x[i][1]<< "," << x[i][2]<< "," << v[i][0]<< "," << v[i][1]<< "," << v[i][2]<<endl;
}

Sampler::~Sampler(){
	_outputFile.close();
}
