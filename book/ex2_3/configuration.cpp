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
 */
 
#include <iostream>
#include <stdexcept>
#include "configuration.hpp"
 
 using namespace std;
 
 Configuration::Configuration(const int n, const double L, const double V, const double sigma, 
						const int m){
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<> uniform_v(-V, V);
	uniform_real_distribution<> uniform_x(0.0, L);
	
	_particles = make_unique<Particle[]>(n);
	for (int i=0;i<n;i++)
		_particles[i].init_v(gen,uniform_v);
	
	auto has_been_validated = false;
	for (int k=0;!has_been_validated && k<m;k++){
		for (int i=0;i<n;i++)
			_particles[i].init_x(gen,uniform_x);
		has_been_validated = _is_valid(_particles,n,sigma);	
	}
	if (!has_been_validated) throw runtime_error("Failed to create valid configuration");
}

bool Configuration::_is_valid(unique_ptr<Particle[]>& particles,const int n,const double sigma){
	for (int i=0;i<n;i++)
		for (int j=0;j<i;j++)
			if (particles[i].get_distance(particles[j])<2*sigma)
				return false;
	return true;
}