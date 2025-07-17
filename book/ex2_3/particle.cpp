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
#include <cmath>
#include <limits>
#include <cassert>
#include "particle.hpp"
 
 using namespace std;
 
 /**
  * Algorithm 2.2: calculate time to the next collision of two specified spheres.
  */ 
  double Particle::get_pair_time(Particle & other, const double sigma){
	auto DeltaX =  _get_difference(_x,other._x);
	auto DeltaV = _get_difference(_v,other._v);
	auto DeltaX_V = _inner_product(DeltaX,DeltaV);
	auto DeltaV_2 = _inner_product(DeltaV,DeltaV);
	auto DeltaX_2 = _inner_product(DeltaX,DeltaX);
	auto Upsilon = DeltaX_V*DeltaX_V - DeltaV_2 * (DeltaX_2 - 4*sigma*sigma);
	if (Upsilon > 0 && DeltaX_V < 0){
		auto dt = -(DeltaX_V + sqrt(Upsilon))/DeltaV_2;
		if (dt > 0) return dt;
	}

	return  numeric_limits<double>::infinity();
  }
  
  
 /**
 * Calculate time to next collision between particle and a specified wall
 */
double Particle::get_wall_time(const int wall, const double L, const double sigma) {
	if (_v[wall] > 0){
		auto dt = (L - sigma -_x[wall])/_v[wall];
		assert (dt > 0);
		return dt;
	}
	if (_v[wall] < 0){
		auto dt =  (_x[wall]-sigma)/(-_v[wall]);
		assert (dt > 0);
		return dt;
	}
	return numeric_limits<double>::infinity();
}

/**
 *  Collide two spheres, reversing velocity components normal to tangent plane
 */	
void Particle::collide(Particle & other){
	auto e_perpendicular =  get_normalized(_get_difference(_x,other._x));
	auto DeltaV = _get_difference(_v,other._v);
	auto DeltaV_perp = _inner_product(e_perpendicular,DeltaV);
	for (int i=0;i<3;i++){
		_v[i] -= DeltaV_perp*e_perpendicular[i];
		other._v[i] += DeltaV_perp*e_perpendicular[i];
	}
}

/**
 *  This is used to facilitate recording samples in a CSV filke.
 */
std::ostream &operator<<(std::ostream &os, Particle const &particle) { 
    return os << particle._x[0] << "," << particle._x[1] << "," << particle._x[2] << "," <<particle._v[0] << "," << particle._v[1] << "," << particle._v[2];
}
	
 
