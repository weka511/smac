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
#include <getopt.h>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <sys/stat.h> 
#include <vector>
#include "md.hpp"

using namespace std;


/**
 * Main program. 
 */
int main(int argc, char **argv) {
	std::string output_path = "./foo.csv";
	int         N           = 10000;
	int         n           = 100;
	int         d           = 2;
	int         M           = 100;
	int         freq        = 100;
	double      L           = 1;
	double      V           = 1;
	double      sigma       = 0.01;
	
	struct option long_options[] = {
			{"epochs",    required_argument,	0, 	'N'},
			{"particles", required_argument,	0, 	'n'},
			{"help",  	  no_argument, 		    0, 	'h'},
			{"dimension", required_argument, 	0, 	'd'},
			{"attempts",  required_argument, 	0, 	'M'},
			{"freq",  	  required_argument, 	0, 	'f'},
			{"length",    required_argument, 	0, 	'L'},
			{"Velocity",  required_argument, 	0, 	'V'},
			{"sigma",  	  required_argument, 	0, 	's'},
			{"output",    required_argument,    0,  'o'},
			{0, 				0, 				0, 	0}
	};	
	
	
	int c;
	int option_index = 0;
	while ((c = getopt_long (argc, argv, "N:n:hd:M:f:L:V:s:o:",long_options, &option_index)) != -1)
		switch(c) {
			case 'N':
				N = atoi(optarg);
				break;
			case 'n':
				n = atoi(optarg);
				break;
			case 'd':
				d = atoi(optarg);
				break;
			case 's':
				sigma = atof(optarg);
				break;
			case 'M':
				M = atoi(optarg);
				break;
			case 'f':
				freq = atoi(optarg);
				break;
			case 'o':
				output_path = optarg;
				break;
			default:
				abort();
	}

	if (std::ifstream(output_path)){
		std::cerr << "Output file " << output_path << " already exists" << std::endl;
		exit(EXIT_FAILURE);
	}
	Configuration configuration(n,d,sigma);
	int status = configuration.initialize(M);
	for  (int i=0; SUCCESS==status && i<N && !killed();i++) {
		if (i%freq ==0)
			std::cout << "Epoch " << (i+1) << std::endl;
		status = configuration.event_disks();
	}
	ofstream output(output_path);
	output << "N="<<N         << std::endl;
	output << "n="<<n         << std::endl;
	output << "d="<<d         << std::endl;
	output << "M="<<M         << std::endl;
	output << "L="<<L         << std::endl;
	output << "V="<<V         << std::endl;
	output << "sigma="<<sigma << std::endl;
	configuration.dump(output);
	output.close();
	return status;
}


double Particle::get_time_to_particle(Particle* other, double sigma) {
	double DeltaX[3], DeltaV[3];
	for (int i=0;i<_d;i++)
		DeltaX[i] = X[i] - other->X[i];
	for (int i=0;i<_d;i++)
		DeltaV[i] = V[i] - other->V[i];
	double DeltaVX = 0;
	double DeltaV2 = 0;
	double DeltaX2 = 0;
	for (int i=0;i<_d;i++){
		DeltaVX += X[i]*V[i];
		DeltaX2 += X[i]*X[i];
		DeltaV2 += V[i]*V[i];
	}
	
	const double Upsilon = DeltaVX*DeltaVX - DeltaV2*(DeltaX2-4*sigma*sigma);
	if (Upsilon>0 && DeltaVX<0)
		return -(DeltaVX + sqrt(Upsilon))/DeltaV2;
	else
		return std::numeric_limits<double>::infinity(); 
	}

void Particle::pair_collide(Particle* other) {
	double DeltaX[_d], DeltaV[_d];
	for (int i=0;i<_d;i++)
		DeltaX[i] = X[i] - other->X[i];
	for (int i=0;i<_d;i++)
		DeltaV[i] = V[i] - other->V[i];
	double DeltaX2 = 0;
	for (int i=0;i<_d;i++)
		DeltaX2 += DeltaX[i]*DeltaX[i];
	double e_perpendicular[_d];
	for (int i=0;i<_d;i++)
		e_perpendicular[i] = DeltaX[i]/sqrt(DeltaX2);
	double DeltaV_e = 0;
	for (int i=0;i<_d;i++)
		DeltaV_e += DeltaV[i]*e_perpendicular[i];
	for (int i=0;i<_d;i++){
		V[i]        -= DeltaV_e * e_perpendicular[i];
		other->V[i] += DeltaV_e * e_perpendicular[i];
	}
}

std::ostream & operator<<(std::ostream & stream, const Particle * particle) {
    stream << particle->X[0] << ", " << particle->X[1]<< ", " << particle->V[0] << ", " << particle->V[1];
    return stream;
}

int Configuration::build_config(std::uniform_real_distribution<double> & distr,
								std::default_random_engine& eng){
	double L_reduced[3];
	
	for (int i=0;i<_d;i++)
		L_reduced[i] = L[i]-_sigma;
	
	for (int i=0;i<_n;i++) {
		_particles[i]->randomizeX(distr, eng, L_reduced);
		for (int j=0;j<i;j++) 
			if (_particles[i]->get_dist_sq(_particles[j])<4*_sigma*_sigma)
				return FAIL_DISKS_TOO_CLOSE;
	}
	
	for (int i=0;i<_n;i++)
		_particles[i]->randomizeV(distr, eng, V);
	
	return SUCCESS;
}
	
int Configuration::initialize(int n){
	std::random_device rd;
	std::default_random_engine eng(rd());
	std::uniform_real_distribution<double> distr(-1, 1);
	for (int i=0;i<n;i++)
		if (SUCCESS == build_config(distr,eng)){
			std::cout << "Built configuration after " << (i+1) << " attempts" << std::endl;
			return SUCCESS;
		}
	
	std::cout << "Failed to build configuration after " << n << " attempts" << std::endl;
	return FAIL_BUILD_CONFIG;
}

WallCollision Configuration::get_next_wall_collision(){
	double t    = std::numeric_limits<double>::infinity();
	double j    = -1;
	double wall = -1;
	for (int i=0;i<_n;i++)
		for (int k=0;k<_d;k++){
			double t0 = _particles[i]->get_time_to_wall(k, L[k]-_sigma);
			if (t0<t) {
				t    = t0;
				j    = i;
				wall = k;
			}
		}			
	return WallCollision(t,j,wall);
}


ParticleCollision Configuration::get_next_particle_collision(){
	double t = std::numeric_limits<double>::infinity();
	double k = -1;
	double l = -1;
	for (int i=0;i<_n;i++)
		for (int j=0;j<i;j++){
			double t0 = _particles[i]->get_time_to_particle(_particles[j], _sigma);
			if (t0<t) {
				t = t0;
				k = i;
				l = j;
			}
		}
	return ParticleCollision(t,k,l);
}
	
int Configuration::event_disks(){
	WallCollision next_wall_collision         = get_next_wall_collision();
	ParticleCollision next_particle_collision = get_next_particle_collision();
	
	if (next_wall_collision._time<next_particle_collision._time) {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_wall_collision._time);
		
		_particles[next_wall_collision._j]->wall_collide(next_wall_collision._wall);
	} else {
		for (int i=0;i<_n;i++)
			_particles[i]->evolve(next_particle_collision._time);
		
		_particles[next_particle_collision._k]->pair_collide(_particles[next_particle_collision._l]);
	}
	return SUCCESS;
}

bool killed(std::string kill_file){
	bool kill = file_exists(kill_file.c_str());
	if (kill) {
		std::cout << "Killed" << std::endl;
		remove(kill_file.c_str());
	}
	return kill;
}

















