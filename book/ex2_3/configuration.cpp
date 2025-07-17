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
#include <limits>
#include "configuration.hpp"
 
 using namespace std;
 
 Configuration::Configuration(const int n, const double L, const double V, const double sigma, 
						const int m) : _n(n),_sigma(sigma),_length(L){
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<> uniform_v(-V, V);
	uniform_real_distribution<> uniform_x(sigma, L-sigma);
	
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

/**
 * Calculate time to the next collision of any two spheres.
 */ 	
tuple<double,int,int> Configuration::get_next_pair_collision(){
	double t0 =  numeric_limits<double>::infinity();
	tuple<double,int,int> result = make_tuple(t0,-1,-1);
	for (int i=0;i<_n;i++)
		for (int j=0;j<i;j++){
			const double t1 = _particles[i].get_pair_time(_particles[j],_sigma);
			if (t1 < t0){
				result = make_tuple(t1,i,j);
				t0 = t1;
			} 
		}
	return result;
}

/**
 * Calculate time to next collision between any sphere and any wall
 */
tuple<double,int,int> Configuration::get_next_wall_collision(){
	double best_wall_time =  numeric_limits<double>::infinity();
	tuple<double,int,int> result = make_tuple(best_wall_time,-1,-1);
	for (int i=0;i<_n;i++)
		for (int wall=0;wall<3;wall++){
			const double t = _particles[i].get_wall_time(wall,_length,_sigma);
			if (t < best_wall_time){
				best_wall_time = t;
				result = make_tuple(best_wall_time,i,wall);
			} 
		}
	return result;
}