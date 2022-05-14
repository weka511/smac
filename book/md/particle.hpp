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

class Particle{

	const int    _d;
  public:
	double*      X;  //FIXME
	double*      V;  //FIXME
	Particle(const int d): _d(d) {
		X = new double [d];
		V = new double[d];
	}
	
	Particle(const int d,double values[4]): _d(d) {
		X    = new double [d];
		X[0] = values[0];
		X[1] = values[1];
		V    = new double[d];
		V[0] = values[2];
		V[1] = values[3];
	}
	
	double get_dist_sq(Particle* other){
		double result = 0;
		for (int i;i<_d;i++)
			result += (X[i]-other->X[i]) * (X[i]-other->X[i]);
		return result;	
	}

	void randomizeX(std::uniform_real_distribution<double> & distr,
					std::default_random_engine& eng,
					double scale[3]) {
		for (int i=0;i<_d;i++)
			X[i] = scale[i] * distr(eng);
	}
	
	void randomizeV(std::uniform_real_distribution<double> & distr,
					std::default_random_engine& eng,
					double scale[3]) {
	for (int i=0;i<_d;i++)
		V[i] = scale[i] * distr(eng);
	}
	
	double get_time_to_wall(int wall, double free_space) {
		return (free_space - X[wall] * copysign(1.0, V[wall])) /fabs(V[wall]); // abs was returning int!!
	}
	
	double get_time_to_particle(Particle* other, double sigma);
	
	void evolve (double t) {
		for (int i=0;i<_d;i++)
			X[i] += V[i] * t;
	};
	
	void wall_collide(int wall) {
		V[wall] *= -1;
	}
	
	void pair_collide(Particle* other);
	
	virtual ~Particle() {
		delete this->X;
		delete this->V;
	}
};

std::ostream & operator<<(std::ostream & stream, const Particle * particle);

#endif
