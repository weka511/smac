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

#include <cassert>
#include <cstdlib> 
#include <fstream>
#include "particle.hpp"

/**
*   Create a particle for a new configuration (still need to be initialized)
*/
Particle::Particle(const int d): _d(d) {
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
Particle::Particle(const int d,double * values): _d(d) {
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

double Particle::get_dist_sq(Particle* other){
	double result = 0;
	for (int i;i<_d;i++)
		result += (_x[i] - other->_x[i]) * (_x[i] - other->_x[i]);
	return result;	
}

/**
 *   Place particle in a random position.
 */
void Particle::randomizeX(  uniform_real_distribution<double> & distribution,
							default_random_engine             & engine,
							const  double                     * scale) {
	for (int i=0;i<_d;i++)
		_x[i] = scale[i] * distribution(engine);
}
	
/**
 *   Assign random velocity to a particle
 */
void Particle::randomizeV(  uniform_real_distribution<double> & distribution,
							default_random_engine             & engine,
							const double                      * scale) {
for (int i=0;i<_d;i++)
	_v[i] = scale[i] * distribution(engine);
}

/**
 * Find time for this particle to collide with a specified wall
 */
double Particle::get_time_to_wall(const int wall,
						double free_space) {
	return (free_space - _x[wall] * copysign(1.0, _v[wall])) /fabs(_v[wall]); // abs was returning int!!
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
 * Determine future position of particle (must be before next collision)
 */
void Particle::evolve (const double t) {
	for (int i=0;i<_d;i++)
		_x[i] += _v[i] * t;
};


/**
 *  Collide particle with a specified other particle
 */
void Particle::collide(Particle* other) {
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
 *  Reverse velocity component when we collide with wall
 */
void Particle::collide(const int wall) {
	_v[wall] *= -1;
}

/**
 *   Calculate difference between two vectors
 *
 *   Delta = x - y
 */
void Particle::delta(double * x, double * y, double * Delta){
	for (int i=0;i<_d;i++)
		Delta[i] = x[i] - y[i];
}

/**
 *   Calculate inner product of two vectors
 */
double Particle::get_inner_product(double *x, double * y){
	double result = 0;
	for (int i=0;i<_d;i++)
		result += x[i]*y[i];
	return result;
}

/**
 *   Determine kinetic energy, assuming unit mass
 */
double Particle::get_energy() {
	double energy = 0.0;
	for (int i=0;i<_d;i++)
		energy += _v[i]*_v[i];
	return 0.5 * energy;
}
	
/**
 *  Used to output position and velocity of particle
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

/**
 *  When patticles destroyed, free up position and velocity
 */
Particle::~Particle() {
	delete this->_x;
	delete this->_v;
}
