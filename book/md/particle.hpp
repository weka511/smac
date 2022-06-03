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

#ifndef _PARTICLE_HPP_
#define _PARTICLE_HPP_


#include <iostream>
#include <random>

using namespace std;

/**
 * This class represents a particle, either a hard disk (2d) or hard sphere (3d).
 */
class Particle{
	double*      _v;     // Velocity vector
	double*      _x;     // Position vector
	const int    _d;     // dimension - 2 or 3
	
  public:
    
  /**
   *   Create a particle for a new configuration (still need to be initialized)
   */
	Particle(const int d);
	
	/**
	 *  Create a particle from a saved configuration.
	 *
	 *  Parameters:
	 *     d         Dimension of space  
	 *     values    A vector whose first 'd' entries are posiion,
     *            	 and the second 'd' the velocity
	 */
	Particle(const int d,double * values);
	
	/**
	 * Get squared distance between this particle and some other.
	 */
	double get_dist_sq(Particle* other);

	/**
	 *   Place particle at a random position.
	 */
	void randomizeX(uniform_real_distribution<double> & distribution,
					default_random_engine             & engine,
					const  double                     * scale);
	
	/**
	 *   Assign random velocity to a particle
	 */
	void randomizeV(uniform_real_distribution<double> & distribution,
					default_random_engine             & engine,
					const double                      * scale);
	
	/**
	 * Find time for this particle to collide with a specified wall
	 */
	double get_time_to_wall(const int wall,
							double free_space);
	
	/**
	 * Find time for this particle to collide with a specified other particle
	 */
	double get_time_to_particle(Particle* other, const double sigma);
	
	/**
	 * Determine future position of particle (must be before next collision)
	 */
	void evolve (const double t);
	
	/**
	 *  Reverse velocity component when we collide with wall
	 */
	void collide(const int wall);
	
	/**
	 *  Collide particle with a specified other particle
	 */
	void collide(Particle* other);
	
	/**
	 *  When patticles destroyed, free up position and velocity
	 */
	virtual ~Particle();
	
	/**
	 *   Calculate difference between two vectors
	 *
	 *   Delta = x - y
	 */
	void delta(double * x, double * y, double * Delta);
	
	/**
	 *   Calculate inner product of two vectors
	 */
	double get_inner_product(double *x, double * y);
	
	/**
	 * Accessor for velocity
	 */
	double get_velocity(int index) {return _v[index];}
	
	/**
     *   Determine kinetic energy, assuming unit mass
     */
	double get_energy();
	
	/**
	 *  Used to output position and velocity of particle
	 */
	friend ostream & operator<<(ostream & stream, const Particle * particle);
};



#endif
