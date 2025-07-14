/**
 * Copyright (C) 2025 Greenweaves Software Limited
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
 

 #include "particle.hpp"
 
 using namespace std;
 

 void init_v(mt19937& gen,uniform_real_distribution<>&uniform_v) {
	 ;
}
 
 Configuration::Configuration(const int n, const double L, const double V, const double sigma, 
						const int m){
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<> uniform_v(-V, V);
	uniform_real_distribution<> uniform_x(0.0, L);
	_particles = make_unique<Particle[]>(n);
}