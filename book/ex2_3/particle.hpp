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

#ifndef _PARTICLE_HPP_
#define _PARTICLE_HPP_

#include <array>
#include <random>
#include <iostream>

using namespace std;

/**
 * This class represents a small sphere
 */
class Particle {
	
  private:
   array<double, 3> _x = {0.,0.,0.};
   array<double, 3> _v = {0.,0.,0.};
   
  public:
  
	/**
	 *  This is used to facilitate recording sampled in a CSV filke.
	 */
    friend std::ostream& operator<<(std::ostream& os, Particle const &particle);
	
    /**
     * This is the usual constructor for a Particle. 
	 * It expects that init_x() and init_v() will be called to set up the
	 * the position and velocity to random values
	 */
    Particle () {};
	
	/**
	 * Constructor used for testing only; it sets up known a known position and velocity
	 */
	Particle (double x,double y, double z, double vx=0.0,double vy=0.0, double vz=0.0) { 
		_x[0] = x;
		_x[1] = y;
		_x[2] = z;
		_v[0] = vx;
		_v[1] = vy;
		_v[2] = vz;
	};
	
	/**
	 * Set velocity to a random value.
	 */
    void init_v(mt19937& gen,uniform_real_distribution<>&uniform){
		for (int i=0;i<3;i++)
			_v[i] = uniform(gen);
	};
	
	/**
	 * Set position to random place within box
	 */
	void init_x(mt19937& gen,uniform_real_distribution<>&uniform){
		for (int i=0;i<3;i++)
			_x[i] = uniform(gen);
	};
	
	/**
	 * Calcuklate the distance between the centres of two spheres.
	 */ 
	double get_distance(Particle & other){
		auto difference = _get_difference(_x,other._x);
		return sqrt(_inner_product(difference,difference));
	};
	
	/**
	 * Rescale a vector so it has unit length
	 */
	array<double, 3> static get_normalized(array<double, 3> x){
		auto norm = sqrt(_inner_product(x,x));
		array<double, 3> result = {0,0,0};
		for (int i=0;i<3;i++)
			result[i] = x[i]/norm;
		return result;
	}
	
	/**
	 * Algorithm 2.2: calculate time to the next collision of two specified spheres.
	 */ 
	double get_pair_time(Particle & other, const double sigma=1.0/32.0);
	
	/**
	 * Calculate time to next collision between particle and a specified wall
	 */
	double get_wall_time(const int wall, const double L, const double sigma) ;
	
	/**
	 *  Collide two spheres, reversing velocity components normal to tangent plane
	 */	
	void collide(Particle & other);
	
	/**
	 *  Collide particle with wall, reversing velocity component normal to wall
	 */
	void  wall_collision(int wall) {
		_v[wall] *= -1;
	}
	
	/**
     * Accessor used for testing only.
	 */
	double get_v(const int i) {return _v[i];}
	
	/**
     * Accessor used for testing only.
	 */
	double get_x(const int i) {return _x[i];}
	
	/**
	 * Determine position of particle after a specifed time,
	 * assuming constant veleocity
	 */
	void evolve(const double dt) {
		for (int i=0;i<3;i++)
			_x[i] += (dt * _v[i]);
	}
	
  private:
  
    /**
	 * Subtract one vector from another 
	 */
    array<double, 3> static _get_difference(array<double, 3> &x0, array<double, 3> &x1){
		array<double, 3> difference = {0,0,0};
		for (int i=0;i<3;i++)
			difference[i] = x0[i] - x1[i];
		return difference;
	}
	
	/**
	 * Determine the inner poroduct of two vectors.
	 */
	double static _inner_product(array<double, 3> &u, array<double, 3> &v){
		double result = 0;
		for (int i=0;i<3;i++)
			 result += u[i]*v[i];
	
		return result;
	}
};


#endif //_PARTICLE_HPP_
