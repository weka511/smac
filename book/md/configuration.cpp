/**
 * Copyright (C) 2022 Greenweaves Software Limited
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
#include <fstream>
#include <getopt.h>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <sys/stat.h> 
#include <vector>
#include "configuration.hpp"

using namespace std;


int Configuration::_build_config(std::uniform_real_distribution<double> & distr,
								std::default_random_engine& eng){
	double L_reduced[_d];
	
	for (int i=0;i<_d;i++)
		L_reduced[i] = L[i]-_sigma;
	
	for (int i=0;i<_n;i++) {
		_particles[i]->randomizeX(distr, eng, L_reduced);
		for (int j=0;j<i;j++) 
			if (_particles[i]->get_dist_sq(_particles[j])<4*_sigma*_sigma)
				return FAIL_DISKS_TOO_CLOSE;
	}
	
	for (int i=0;i<_n;i++)
		_particles[i]->randomizeV(distr, eng, V);
	
	return SUCCESS;
}
	
int Configuration::initialize(int n){
	std::random_device                     rd;
	std::default_random_engine             eng(rd());
	std::uniform_real_distribution<double> distr(-1, 1);
	for (int i=0;i<n;i++)
		if (SUCCESS == _build_config(distr,eng)){
			cout << "Built configuration after " << (i+1) << " attempts" << endl;
			return SUCCESS;
		}
	
	cout << "Failed to build configuration after " << n << " attempts" << endl;
	return FAIL_BUILD_CONFIG;
}

WallCollision Configuration::_get_next_wall_collision(){
	double t    = std::numeric_limits<double>::infinity();
	double j    = -1;
	double wall = -1;
	for (int i=0;i<_n;i++)
		for (int k=0;k<_d;k++){
			double t0 = _particles[i]->get_time_to_wall(k, L[k]-_sigma);
			if (t0<t) {
				t    = t0;
				j    = i;
				wall = k;
			}
		}			
	return WallCollision(t,j,wall);
}


ParticleCollision Configuration::_get_next_particle_collision(){
	double t = std::numeric_limits<double>::infinity();
	double k = -1;
	double l = -1;
	for (int i=0;i<_n;i++)
		for (int j=0;j<i;j++){
			double t0 = _particles[i]->get_time_to_particle(_particles[j], _sigma);
			if (t0<t) {
				t = t0;
				k = i;
				l = j;
			}
		}
	return ParticleCollision(t,k,l);
}

int Configuration::event_disks(){
	WallCollision next_wall_collision         = _get_next_wall_collision();
	ParticleCollision next_particle_collision = _get_next_particle_collision();
	
	if (next_wall_collision._time<next_particle_collision._time) {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_wall_collision._time);
		
		_particles[next_wall_collision._j]->wall_collide(next_wall_collision._wall);
		n_wall_collisions++;
	} else {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_particle_collision._time);
		
		_particles[next_particle_collision._k]->pair_collide(_particles[next_particle_collision._l]);
		n_pair_collisions++;
	}
	return SUCCESS;
}