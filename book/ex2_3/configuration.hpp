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

#ifndef _CONFIGURATION_HPP_
#define _CONFIGURATION_HPP_

#include <memory>
#include <tuple>
#include "particle.hpp"

using namespace std;

/**
 * This class is a container for particles.
 */
class Configuration {
  private:
    unique_ptr<Particle[]> _particles;
	const int _n;
	const double _sigma;
	const double _length;

  public:
	Configuration(const int n, const double L, const double V, const double sigma, 
						const int m);
	int size() {return _n;};
	
	tuple<double,int,int> get_next_pair_collision();
	
	tuple<double,int,int> get_next_wall_collision();
	
	/**
	 * Determine position of all particles after a specifed time,
	 * assuming constant veleocity
	 */
	void evolve(double dt) {
		for (int i=0;i<_n;i++)
			_particles[i].evolve(dt);
	}
	
	/**
	 *  Collide two spheres, reversing velocity components normal to tangent plane
	 */	
	void collide(int i, int j) {_particles[i].collide(_particles[j]);};
	
	/**
	 *  Collide particle with wall, reversing velocity component normal to wall
	 */
	void  wall_collision(int i,int wall) {_particles[i].wall_collision(wall);};
	
	void output(const double t,std::ostream& os) {
		for (int i=0;i<_n;i++)
			os << t << "," <<_particles[i] << endl;
	}
	
	
  private:
    bool static _is_valid(unique_ptr<Particle[]> & particles,const int n,const double sigma);
};

#endif // _CONFIGURATION_HPP_
