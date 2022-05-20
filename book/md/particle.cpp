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


#include <cstdlib> 
#include <fstream>
#include <random>
#include "particle.hpp"


/**
 *   Place particle in a random position.
 */
void Particle::randomizeX(uniform_real_distribution<double> & distr,
							default_random_engine& eng,
							const  double scale[3]) {
	for (int i=0;i<_d;i++)
		_x[i] = scale[i] * distr(eng);
}
	
/**
 *   Assign random velicities to a particle
 */
void Particle::randomizeV(uniform_real_distribution<double> & distr,
							default_random_engine& eng,
							const double scale[3]) {
for (int i=0;i<_d;i++)
	_v[i] = scale[i] * distr(eng);
}

/**
 * Find time for this particle to collide with a specified other particle
 */
double Particle::get_time_to_particle(	Particle* other,
										const double sigma) {
	double DeltaX[_d];
	delta(_x, other->_x,DeltaX);
	double DeltaV[_d];
	delta(_v, other->_v,DeltaV);
	const double DeltaVX = get_inner_product(DeltaX,DeltaV);
	const double DeltaV2 = get_inner_product(DeltaV,DeltaV);
	const double DeltaX2 = get_inner_product(DeltaX,DeltaX);
	const double Upsilon = DeltaVX*DeltaVX - DeltaV2*(DeltaX2-4*sigma*sigma);
	return (Upsilon>0 && DeltaVX<0) ? -(DeltaVX + sqrt(Upsilon))/DeltaV2: std::numeric_limits<double>::infinity(); 
}

/**
 *  Collide particle with another
 */
void Particle::pair_collide(Particle* other) {
	double DeltaX[_d];
	delta(_x, other->_x,DeltaX);
	double DeltaV[_d];
	delta(_v, other->_v,DeltaV);
	const double DeltaX2 = get_inner_product(DeltaX,DeltaX);
	double e_perpendicular[_d];
	for (int i=0;i<_d;i++)
		e_perpendicular[i] = DeltaX[i]/sqrt(DeltaX2);
	double DeltaV_e = 0;
	for (int i=0;i<_d;i++)
		DeltaV_e += DeltaV[i]*e_perpendicular[i];
	for (int i=0;i<_d;i++){
		_v[i]        -= DeltaV_e * e_perpendicular[i];
		other->_v[i] += DeltaV_e * e_perpendicular[i];
	}
}

/**
 *  Used to outout position and velocity of particle
 */
ostream & operator<<(ostream & stream,
					const Particle * particle) {
    stream << particle->_x[0] << ", " << particle->_x[1]<< ", ";
	if (particle->_d==3)
		stream<<particle->_x[2] << ", ";
	stream  << particle->_v[0] << ", " << particle->_v[1]<< ", ";
	if (particle->_d==3)
		stream<<particle->_v[2] ;
    return stream;
}
