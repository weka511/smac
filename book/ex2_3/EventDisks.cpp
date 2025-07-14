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
 *
 * Molecular dynamics simulation for hard disks or hard spheres, as described
 * in Statistical Mechanics: Algorithms and Computations, by Werner Krauth,
 * ISBN 978-0-19-851535-7. This program performs the calculations, and the data
 * in the outout files are analyzed by md-plot.py.
 */

#include <iostream>
#include <random>
#include <limits>
#include <cmath>
#include <stdexcept>
#include <cassert>

#include "EventDisks.hpp"

using namespace std;

/**
 *  Create a valid configuration, comprising positions and velocites.
 */
EventDisks::EventDisks(const int n, const double L, const double V, const double sigma, 
						const int m, double dt_sample,string sample_file): _n(n), _sigma(sigma),_length(L),dt_sample(dt_sample) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_real_distribution<> uniform_v(-V, V);
	std::uniform_real_distribution<> uniform_x(0.0, L);
	
	_x = make_unique<double[][3]>(n);
	auto has_been_validated = false;
	for (int k=0;!has_been_validated && k<m;k++){
		// Create a candidate configuration
		for (int i = 0; i < n; ++i)
			for (int j = 0; j < _d; ++j)
				_x[i][j] = uniform_x(gen);
		// Verify that no two spheres overlap
		has_been_validated = _is_valid(_x,n,sigma);	
	}
	
	if (has_been_validated){
		_v = make_unique<double[][3]>(n);
		for (int i = 0; i < n; ++i)
			for (int j = 0; j < _d; ++j)
				_v[i][j] = uniform_v(gen);
	} else
		throw runtime_error("Failed to create valid configuration");
	
	_sampler = make_unique<Sampler>(n,sample_file);
}

/**
 * Algorithm 2.1: perform one step of the simulation. Determine time to next collision,
 * of either type, update all positions to just befroe collision,
 * then update velocities to just after.
 */
void EventDisks::event_disks() {
	double dt_pair;
	int k,l;
	tie(dt_pair,k,l) = get_next_pair_time();
	double dt_wall;
	int sphere,wall;
	tie(dt_wall,sphere,wall) = get_next_wall_time();

	move_and_sample(min(dt_wall,dt_pair));
	if (dt_wall < dt_pair)
		wall_collision(sphere,wall);
	else
		pair_collision(k,l);
}

/**
 * Validate configuration: make sure no two sphere overlap
 */ 
bool EventDisks::_is_valid(unique_ptr<double[][3]> &x,const int n,  const double sigma){
	auto sigma2 = sigma*sigma;
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < i; ++j) {
			auto DeltaX = array{x[i][0]-x[j][0], x[i][1]-x[j][1], x[i][2]-x[j][2]};
			if (_inner_product(DeltaX,DeltaX) < sigma2) return false;
		}
	return true;
}

/**
 * Algorithm 2.2: calculate time to the next collision of two specified spheres.
 */ 
double EventDisks::get_pair_time(int i,int j) {
	auto epsilon = 0.1;//10e-6;
	auto DeltaX = array{_x[i][0]-_x[j][0], _x[i][1]-_x[j][1], _x[i][2]-_x[j][2]};
	auto DeltaV = array{_v[i][0]-_v[j][0], _v[i][1]-_v[j][1], _x[i][2]-_x[j][2]};
	auto DeltaX_V = _inner_product(DeltaX,DeltaV);
	auto DeltaV_2 = _inner_product(DeltaV,DeltaV);
	auto DeltaX_2 = _inner_product(DeltaX,DeltaX);
	auto Upsilon = DeltaX_V*DeltaX_V - DeltaV_2 * (DeltaX_2 - 4*_sigma*_sigma);
	if (Upsilon > 0 && DeltaX_V < 0){
		auto dt = -(DeltaX_V + sqrt(Upsilon))/DeltaV_2;
		if (dt > epsilon) return dt;
	}

	return  numeric_limits<double>::infinity();
}

/**
 * Calculate time to the next collision of any two spheres.
 */ 	
tuple<double,int,int> EventDisks::get_next_pair_time(){
	double t0 =  numeric_limits<double>::infinity();
	tuple<double,int,int> result = make_tuple(t0,-1,-1);
	for (int i=0;i<_n;i++)
		for (int j=0;j<i;j++){
			const double t1 = get_pair_time(i,j);
			if (t1 < t0){
				result = make_tuple(t1,i,j);
				t0 = t1;
			} 
		}
	return result;
}
		
/**
 * Calculate time to next collision between a specified sphere and specified wall
 */
double EventDisks::get_wall_time(int sphere, int wall) {
	if (_v[sphere][wall] > 0){
		auto dt = (_length-_x[sphere][wall])/_v[sphere][wall];
		assert (dt > 0);
		return dt;
	}
	if (_v[sphere][wall] < 0){
		auto dt =  _x[sphere][wall]/(-_v[sphere][wall]);
		assert (dt > 0);
		return dt;
	}
	return numeric_limits<double>::infinity();
}

/**
 * Calculate time to next collision between any sphere and any wall
 */
tuple<double,int,int> EventDisks::get_next_wall_time(){
	double best_wall_time =  numeric_limits<double>::infinity();
	tuple<double,int,int> result = make_tuple(best_wall_time,-1,-1);
	for (int sphere=0;sphere<_n;sphere++)
		for (int wall=0;wall<_d;wall++){
			const double t = get_wall_time(sphere,wall);
			if (t < best_wall_time){
				best_wall_time = t;
				result = make_tuple(best_wall_time,sphere,wall);
			} 
		}
	return result;
}

/**
 *  Run configuration forward for a specified time interval,
 *  and sample data if it is time.
 */
void EventDisks::move_and_sample(double dt){
	assert(dt > 0);
	auto t_next_sample = (n_sampled + 1) * dt_sample;
	auto t_next_collision = _t + dt;
	if (t_next_collision < t_next_sample)
		_t = move_all_spheres(dt,t_next_collision);
	else {
		/**
		 *  Run configuration forward until the time when the next sample is due,
		 * then sample it. Note that multiple samples may be needed.
		 */
		while (t_next_collision >= t_next_sample) {
			auto dt_next_sample = t_next_sample - _t;
			_t = move_all_spheres(dt_next_sample,t_next_sample);
			_sampler->sample(t_next_sample,_x,_v);
			n_sampled++;
			t_next_sample = (n_sampled + 1) * dt_sample;
		}
		_t = move_all_spheres(t_next_collision - _t,t_next_collision);
	}
}

/**
 *  Run configuration forward for a specified time interval, updating current time and positions.
 */
double EventDisks::move_all_spheres(double dt,double time_new) {
	for (int i=0;i<_n;i++)
		for (int j=0;j<_d;j++)
			_x[i][j] += (dt * _v[i][j]);
	
	return time_new;
}

/**
 *  Collide sphere with wall, reversing velocity component normal to wall
 */
void  EventDisks::wall_collision(int sphere,int wall) {
	_v[sphere][wall] = -_v[sphere][wall];
}

/**
 *  Collide two spheres, reversing velocity components normal to tangent plane
 */	
void  EventDisks::pair_collision(int k,int j) {
	auto e_perpendicular = array{_x[k][0]-_x[j][0], _x[k][1]-_x[j][1], _x[k][2]-_x[j][2]}; 
	auto norm = sqrt(_inner_product(e_perpendicular,e_perpendicular));

	for (int i=0;i<_d;i++)
		e_perpendicular[i] /= norm;
	
	auto DeltaV = array{_v[k][0]-_v[j][0], _v[k][1]-_v[j][1], _v[k][2]-_v[j][2]};
	auto DeltaV_perp = _inner_product(e_perpendicular,DeltaV);
	
	for (int i=0;i<_d;i++){
		_v[k][i] -= DeltaV_perp*e_perpendicular[i];
		_v[j][i] += DeltaV_perp*e_perpendicular[i];
	}
}
