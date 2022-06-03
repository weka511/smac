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

#include "configuration.hpp"
#include "md.hpp"
using namespace std;

/**
 * Used when we initialize Configuration to make one attempt at constructing
 * an admissable set of spheres or disks.
 */
int Configuration::_build_config(	uniform_real_distribution<double> & distribution,
									default_random_engine             & engine){
	double L_reduced[_d];
	
	for (int i=0;i<_d;i++)
		L_reduced[i] = L[i]-_sigma;
	
	for (int i=0;i<_n;i++) {
		_particles[i]->randomizeX(distribution, engine, L_reduced);
		for (int j=0;j<i;j++) 
			if (_particles[i]->get_dist_sq(_particles[j])<4*_sigma*_sigma)
				return FAIL_DISKS_TOO_CLOSE;
	}
	
	for (int i=0;i<_n;i++)
		_particles[i]->randomizeV(distribution, engine, V);
	
	return SUCCESS;
}
	
/**
  * Attempt to populate a configuration with a set of admissable particles.
  *
  * Parameters:
  *     n       Number of attenpts
  */
int Configuration::initialize(int n){
	random_device                     rd;
	default_random_engine             engine(rd());
	uniform_real_distribution<double> distribution(-1, 1);
	for (int i=0;i<n;i++)
		if (SUCCESS == _build_config(distribution,engine)){
			cout << "Built configuration after " << (i+1) << " attempts" << endl;
			return SUCCESS;
		}
	
	cout << "Failed to build configuration after " << n << " attempts" << endl;
	return FAIL_BUILD_CONFIG;
}

/**
 *  Algorithm 2.1 from SMAC. Work out when the next collision will occur,
 *  then make the collision happen.
 */
int Configuration::event_disks(){
	WallCollision next_wall_collision         = _get_next_wall_collision();
	ParticleCollision next_particle_collision = _get_next_particle_collision();
	
	if (next_wall_collision._time<next_particle_collision._time) {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_wall_collision._time);
		
		_particles[next_wall_collision._j]->collide(next_wall_collision._wall);
		n_wall_collisions++;
	} else {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_particle_collision._time);
		
		_particles[next_particle_collision._k]->collide(_particles[next_particle_collision._l]);
		n_pair_collisions++;
	}
	return SUCCESS;
}

/**
 * Determine earliest time when any sphere will hit wall, 
 * ignoring the possibility of an earler collision with
 * another sphere
 */
WallCollision Configuration::_get_next_wall_collision(){
	double t    = numeric_limits<double>::infinity();
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

/**
 * Determine earliest time when any sphere will hit another sphere, 
 * ignoring the possibility of an earler collision with a wall
 */	
ParticleCollision Configuration::_get_next_particle_collision(){
	double t = numeric_limits<double>::infinity();
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

/**
 *  Output configuration and velocities to specified stream
 */
void Configuration::dump(ofstream& output) {

		if (_d==2)
			output << "X1,X2,V1,V2"   << endl;
		else
			output << "X1,X2,X3,V1,V2,V3"   << endl;

	for (auto particle = begin (_particles); particle != end (_particles); ++particle)
		output << *particle << std::endl;
}

void Configuration::report(ofstream* output) {

	for (auto particle = begin (_particles); particle != end (_particles); ++particle)
		*output << *particle << std::endl;
}

