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
#include "particle.hpp"
 
 using namespace std;
 

 void Particle::init_v(mt19937& gen,uniform_real_distribution<>&uniform_v) {
	 for (int i=0;i<3;i++)
		 _v[i]=uniform_v(gen);
	 cout << _v[0] << "," << _v[1] << "," << _v[2] << endl;
}

void Particle::init_x(mt19937& gen,uniform_real_distribution<>&uniform_x) {
	 for (int i=0;i<3;i++)
		 _x[i]=uniform_x(gen);
	  cout << _x[0] << "," << _x[1] << "," << _x[2] << endl;
}
 
 double Particle::get_distance(Particle & other){
	 double sumsq = 0;
	 for (int i=0;i<3;i++){
		 const double delta = _v[i] - other._v[i];
		 sumsq += delta*delta;
	 }
	 return sqrt(sumsq);
 }
 
