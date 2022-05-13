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

#ifndef _MD_HPP_
#define _MD_HPP_

const int SUCCESS                = 0;
const int FAIL_DISKS_TOO_CLOSE   = SUCCESS + 1;
const int FAIL_BUILD_CONFIG      = FAIL_DISKS_TOO_CLOSE + 1;

bool killed(std::string kill_file="kill.txt");

bool file_exists (const char *filename) {
  struct stat   buffer;   
  return (stat (filename, &buffer) == 0);
}

class Particle{

	const int    _d;
  public:
	double*      X;  //FIXME
	double*      V;  //FIXME
	Particle(const int d): _d(d) {
		X = new double [d];
		V = new double[d];
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
	
class WallCollision{
  public:
	const double _time;
	const int    _j;
	const int    _wall;
	WallCollision(const double time, const int j, const int wall) : _time(time), _j(j), _wall(wall){}
};

class ParticleCollision{
  public:
  	const double _time;
	const int _k;
	const int _l;
	ParticleCollision(const double time, const int k, const int l): _time(time), _k(k), _l(l){}
};

class Configuration{

	const int _n;
	const int _d;
	const double _sigma;
	double L[3];
	double V[3];
	std::vector<Particle*> _particles; 
  public:
 
	Configuration(	const int n,
					const int d,
					const double sigma) : _n(n), _d(d), _sigma(sigma)  {
	    L[0] = L[1] = L[2] = 1;
		V[0] = V[1] = V[2] = 1;
		for (int i=0;i<n;i++)
			_particles.push_back(new Particle(d));
	}
	
	int build_config(std::uniform_real_distribution<double> & distr,
					std::default_random_engine& eng);
	
	int initialize(int n);
	
	virtual ~Configuration() {
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			delete  *particle;
	}
	
	int event_disks();
	
	WallCollision get_next_wall_collision();
	
	ParticleCollision get_next_particle_collision();
	
	void dump(std::ofstream& output) {
		output << "X1,X2,V1,V2"   << std::endl;
		for (auto particle = begin (_particles); particle != end (_particles); ++particle)
			output << *particle << std::endl;
	}
};
#endif

