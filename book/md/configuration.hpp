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

#ifndef _CONFIGURATION_HPP_
#define _CONFIGURATION_HPP_

#include "particle.hpp"

const int SUCCESS                = 0;
const int FAIL_DISKS_TOO_CLOSE   = SUCCESS + 1;
const int FAIL_BUILD_CONFIG      = FAIL_DISKS_TOO_CLOSE + 1;
	
class WallCollision{
  public:
	const double _time;
	const int    _j;
	const int    _wall;
	WallCollision(const double time, const int j, const int wall) : _time(time), _j(j), _wall(wall){}
};

class ParticleCollision{
  public:
  	const double _time;
	const int _k;
	const int _l;
	ParticleCollision(const double time, const int k, const int l): _time(time), _k(k), _l(l){}
};

class Configuration{

	const int _n;
	const int _d;
	const double _sigma;
	double L[3];
	double V[3];
	std::vector<Particle*> _particles; 
	int n_wall_collisions = 0;
	int n_pair_collisions = 0;
  public:
 
	Configuration(	const int n,
					const int d,
					const double sigma) : _n(n), _d(d), _sigma(sigma)  {
	    L[0] = L[1] = L[2] = 1;
		V[0] = V[1] = V[2] = 1;
		for (int i=0;i<n;i++)
			_particles.push_back(new Particle(d));
	}
	
	Configuration(	const int n,
					const int d,
					const double sigma,
					std::vector<Particle*> particles) : _n(n), _d(d), _sigma(sigma)  {
	    L[0] = L[1] = L[2] = 1;
		V[0] = V[1] = V[2] = 1;
		_particles = particles;
	}
	
	int build_config(std::uniform_real_distribution<double> & distr,
					std::default_random_engine& eng);
	
	int initialize(int n);
	
	virtual ~Configuration() {
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			delete  *particle;
	}
	
	int event_disks();
	
	WallCollision get_next_wall_collision();
	
	ParticleCollision get_next_particle_collision();
	
	void dump(std::ofstream& output) {
		output << "X1,X2,V1,V2"   << std::endl;
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			output << *particle << std::endl;
	}
	
	void save(std::string output_path);

	int get_n_wall_collisions() {return n_wall_collisions;}
	int get_n_pair_collisions() {return n_pair_collisions;}
};

#endif
