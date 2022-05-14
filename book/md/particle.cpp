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
#include "particle.hpp"

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
