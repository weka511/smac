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

using namespace std;

const int SUCCESS                = 0;
const int FAIL_DISKS_TOO_CLOSE   = SUCCESS + 1;
const int FAIL_BUILD_CONFIG      = FAIL_DISKS_TOO_CLOSE + 1;
const int UNDEFINED              = std::numeric_limits<int>::max();	

/**
 * This class represents a collision with a wall
 */
class WallCollision{
  public:
	const double _time;
	const int    _j;
	const int    _wall;
	WallCollision(const double time, const int j, const int wall) : _time(time), _j(j), _wall(wall){}
};

/**
 * This class represents a collision with a pair of particles
 */
class ParticleCollision{
  public:
  	const double _time;
	const int _k;
	const int _l;
	ParticleCollision(const double time, const int k, const int l): _time(time), _k(k), _l(l){}
};

/**
 * This class represents a box containing particles.
 */
class Configuration{

	const int         _n;           // Number of particles
	const int         _d;           // Dimension of box
	const double      _sigma;    // Radius of a particle
	double *          L;
	double *          V;
	vector<Particle*> _particles; 
	int               n_wall_collisions;
	int               n_pair_collisions;

  public:
 
	/**
	 * Create a new configuration of n particles
	 */
	Configuration(	const int n,
					const int d,
					const double sigma) : _n(n), _d(d), _sigma(sigma), n_wall_collisions(0), n_pair_collisions(0)  {
		L = new double(d);
		V = new double(d);
	    L[0] = L[1] = 1;
		V[0] = V[1] = 1;
		if (d>2){
			L[2] = 1;
			V[2] = 1;
		}
		for (int i=0;i<n;i++)
			_particles.push_back(new Particle(d));
	}
	
	/**
	 * Create a  configuration from an existing set of particles
	 */
	Configuration(	const int n,
					const int d,
					const double sigma,
					vector<Particle*> particles) : _n(n), _d(d), _sigma(sigma), 
														n_wall_collisions(0), n_pair_collisions(0)  {
	   	L = new double(d);
		V = new double(d);
	    L[0] = L[1] = 1;
		V[0] = V[1] = 1;
		if (d>2){
			L[2] = 1;
			V[2] = 1;
		}
		for (vector<Particle*>::iterator it = particles.begin() ; it != particles.end(); ++it)
			_particles.push_back(*it);

	}	
	
	/**
	 * Attempt to populate a configuration with a set of admissable particles.
	 *
	 * Parameters:
	 *     n       Number of attenpts
	 */
	int initialize(int n);
	
	/**
     *  Algorithm 2.1 from SMAC. Work out when the next collision will occur,
     *  then make the collision happen.
     */
	int event_disks();
	
	int get_n_wall_collisions() {return n_wall_collisions;}
	
	int get_n_pair_collisions() {return n_pair_collisions;}
	
	/**
	 *  Output configuration and velocities to specified stream
	 */
	void dump(ofstream& output);
	
	virtual ~Configuration() {
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			delete  *particle;
	}
  private:
  
  	int _build_config(  uniform_real_distribution<double> & distr,
						default_random_engine& eng);
						
	WallCollision     _get_next_wall_collision();
	
	ParticleCollision _get_next_particle_collision();
	
};

#endif
