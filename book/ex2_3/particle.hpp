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

using namespace std;

class Particle {
  private:
   array<double, 3> _x = {0.,0.,0.};
   array<double, 3> _v = {0.,0.,0.};
   
  public:
    Particle () {};
	
	Particle (double x,double y, double z, double vx=0.0,double vy=0.0, double vz=0.0) {
		_x[0] = x;
		_x[1] = y;
		_x[2] = z;
	};
	
    void init_v(mt19937& gen,uniform_real_distribution<>&uniform){
		for (int i=0;i<3;i++)
			_v[i] = uniform(gen);
	};
	
	void init_x(mt19937& gen,uniform_real_distribution<>&uniform){
		for (int i=0;i<3;i++)
			_x[i] = uniform(gen);
	};
	
	double get_distance(Particle & other){
		auto difference = _get_difference(_x,other._x);
		return sqrt(_inner_product(difference,difference));
	};
	
	/**
	 * Algorithm 2.2: calculate time to the next collision of two specified spheres.
	 */ 
	double get_pair_time(Particle & other,double _sigma=1.0/32.0);
	
  private:
    array<double, 3> static _get_difference(array<double, 3> &x0, array<double, 3> &x1){
		array<double, 3> difference = {0,0,0};
		for (int i=0;i<3;i++)
			difference[i] = x0[i] - x1[i];
		return difference;
	}
	
	double static _inner_product(array<double, 3> &u, array<double, 3> &v){
		double result = 0;
		for (int i=0;i<3;i++)
			 result += u[i]*v[i];
	
		return result;
	}
};



#endif //_PARTICLE_HPP_
