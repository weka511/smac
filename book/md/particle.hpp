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

#include <cassert>
#include <iostream>

using namespace std;

/**
 * This class represents a particle, either a hard disk (2d_ or hard sphere (3d).
 */
class Particle{
	double*      _v;     // Velocity vector
	double*      _x;     // Position vector
	const int    _d;     // dimension - 2 or 3
	
  public:
  
  /**
   *   Create a particle for a new configuration (still need to be initialized)
   */
	Particle(const int d): _d(d) {
		assert(d==2 or d ==3);
		_x = new double[d];
		_v = new double[d];
	}
	
	/**
	 *  Create a particle from a saved configuration.
	 *
	 *  Parameters:
	 *     d         Dimension of space  
	 *     values    A vector whose first 'd' entries are posiion,
     *            	 and the second 'd' the velocity
	 */
	Particle(const int d,double * values): _d(d) {
		int  i=0;
		_x    = new double [d];
		_x[0] = values[i++];
		_x[1] = values[i++];
		if (d==3)
			_x[2] = values[i++];
		_v    = new double[d];
		_v[0] = values[i++];
		_v[1] = values[i++];
		if (d==3)
			_v[2] = values[i++];
	}
	
	/**
	 * Get squared distance between this particle and some other.
	 */
	double get_dist_sq(Particle* other){
		double result = 0;
		for (int i;i<_d;i++)
			result += (_x[i]-other->_x[i]) * (_x[i]-other->_x[i]);
		return result;	
	}

	/**
	 *   Place particle in a random position.
	 */
	void randomizeX(uniform_real_distribution<double> & distr,
					default_random_engine& eng,
					const  double scale[3]);
	
	/**
	 *   Assign random velocity to a particle
	 */
	void randomizeV(uniform_real_distribution<double> & distr,
					default_random_engine& eng,
					const double scale[3]);
	
	/**
	 * Find time for this particle to collide with a specified wall
	 */
	double get_time_to_wall(const int wall,
							double free_space) {
		return (free_space - _x[wall] * copysign(1.0, _v[wall])) /fabs(_v[wall]); // abs was returning int!!
	}
	
	/**
	 * Find time for this particle to collide with a specified other particle
	 */
	double get_time_to_particle(Particle* other, const double sigma);
	
	/**
	 * Determine future position of partcle (must be before next collision)
	 */
	void evolve (const double t) {
		for (int i=0;i<_d;i++)
			_x[i] += _v[i] * t;
	};
	
	/**
	 *  Reverse velocity component when we collide with wall
	 */
	void wall_collide(const int wall) {
		_v[wall] *= -1;
	}
	
	/**
	 *  Collide particle with a specified other particle
	 */
	void pair_collide(Particle* other);
	
	/**
	 *  When patticles destroyed, free up position and velocity
	 */
	virtual ~Particle() {
		delete this->_x;
		delete this->_v;
	}
	
	/**
	 *   Calculate distance between two vectors
	 */
	double delta(double * x, double * y, double * Delta){
		for (int i=0;i<_d;i++)
			Delta[i] = x[i] - y[i];
	}
	
	/**
	 *   Calculate inner product of two vectors
	 */
	double get_inner_product(double *x, double * y){
		double result = 0;
		for (int i=0;i<_d;i++)
			result += x[i]*y[i];
		return result;
	}
	
	/**
	 *  Used to output position and velocity of particle
	 */
	friend ostream & operator<<(ostream & stream, const Particle * particle);
};



#endif
