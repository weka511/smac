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
#include <random>
#include "particle.hpp"
#include "history.hpp"

using namespace std;

/**
 * Used to report success, or identify reasons for failure
 */
enum Status {
	SUCCESS              = 0,
	FAIL_DISKS_TOO_CLOSE = SUCCESS + 1,
	FAIL_BUILD_CONFIG    = FAIL_DISKS_TOO_CLOSE + 1,
	UNDEFINED            = std::numeric_limits<int>::max()
};

/**
 * This class represents a collision with a wall
 */
class WallCollision{
  public:
	const double _time;    // Time when collision will occur
	const int    _j;       // Index of sphere
	const int    _wall;    // The index of the wall (actually a pair of opposite walls)
	WallCollision(const double time, const int j, const int wall) : _time(time), _j(j), _wall(wall){}
};

/**
 * This class represents a collision with a pair of particles
 */
class ParticleCollision{
  public:
  	const double _time;    // Time when collision will occur
	const int _k;          // Index of one sphere
	const int _l;          // Index of the other sphere
	ParticleCollision(const double time, const int k, const int l): _time(time), _k(k), _l(l){}
};

/**
 * This class represents a box containing particles.
 */
class Configuration : public HistoryPartner {

	const int         _n;          // Number of particles
	const int         _d;          // Dimension of box
	const double      _sigma;      // Radius of a particle
	double *          L;           // Dimensions of space
	double *          V;           // Used to scale velocities
	
	/**
	 * We need a place to store the particles. Initially they will be unitinitialized,
	 * but initialize(...) and _build_config(...) will assign valid positions and velocities.
	 */
	vector<Particle*> _particles;
	int               n_wall_collisions;    // Number of collisions with walls
	int               n_pair_collisions;    // Number of collisions between pairs

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
	Configuration(	const int         n,
					const int         d,
					const double      sigma,
					vector<Particle*> particles,
					const int         wall_collisions = 0,
					const int         pair_collisions = 0) : _n(n), 
										_d(d),
										_sigma(sigma), 
										n_wall_collisions(wall_collisions), 
										n_pair_collisions(pair_collisions)  {
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
	
	/**
	 * Number of collisions with walls
	 */
	int get_n_wall_collisions() {return n_wall_collisions;}
	
	/**
	 * Number of collisions between pairs
	 */
	int get_n_pair_collisions() {return n_pair_collisions;}
	
	/**
	 *  Output configuration and velocities to specified stream
	 */
	void dump(ofstream& output);
	
	/**
	 *  Output configuration and velocities to specified stream
	 */
	void report(ofstream* output);
	
	virtual ~Configuration() {
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			delete  *particle;
	}
  private:
  
    /**
     * Used when we initialize Configuration to make one attempt at constructing
     * an admissable set of spheres or disks.
     */
  	int _build_config(  uniform_real_distribution<double> & distr,
						default_random_engine& eng);
	
    /**
     * Determine earliest time when any sphere will hit wall, 
     * ignoring the possibility of an earler collision with
     * another sphere
     */	
	WallCollision     _get_next_wall_collision();
	
	/**
     * Determine earliest time when any sphere will hit another sphere, 
     * ignoring the possibility of an earler collision with a wall
     */	
	ParticleCollision _get_next_particle_collision();
	
};

#endif
