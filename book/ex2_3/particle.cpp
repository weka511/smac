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
#include "particle.hpp"
 
 using namespace std;
 
 /**
  * Algorithm 2.2: calculate time to the next collision of two specified spheres.
  */ 
  double Particle::get_pair_time(Particle & other, double _sigma){
	auto DeltaX =  _get_difference(_x,other._x);
	auto DeltaV = _get_difference(_v,other._v);
	auto DeltaX_V = _inner_product(DeltaX,DeltaV);
	auto DeltaV_2 = _inner_product(DeltaV,DeltaV);
	auto DeltaX_2 = _inner_product(DeltaX,DeltaX);
	auto Upsilon = DeltaX_V*DeltaX_V - DeltaV_2 * (DeltaX_2 - 4*_sigma*_sigma);
	if (Upsilon > 0 && DeltaX_V < 0){
		auto dt = -(DeltaX_V + sqrt(Upsilon))/DeltaV_2;
		if (dt > 0) return dt;
	}

	return  numeric_limits<double>::infinity();
  }
	
	
 
