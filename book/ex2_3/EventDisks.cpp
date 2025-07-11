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
#include "EventDisks.hpp"

using namespace std;

bool EventDisks::_is_valid(unique_ptr<double[][3]> &x,const int n,  const double sigma){
	auto sigma2 = sigma*sigma;
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < i; ++j) {
			auto DeltaX = array{x[i][0]-x[j][0], x[i][1]-x[j][1], x[i][2]-x[j][2]};
			if (_inner_product(DeltaX,DeltaX) < sigma2) return false;
		}
	return true;
}

EventDisks::EventDisks(const int n, const double L, const double V, const double sigma, const int m): _n(n), _sigma(sigma),_length(L) {
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
	if (!has_been_validated)
		throw runtime_error("Failed to create valid configuration");
	
	_v = make_unique<double[][3]>(n);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < _d; ++j)
			_v[i][j] = uniform_v(gen);
		
	for (int i = 0; i < n; ++i)
		cout << "("<<_x[i][0] << "," << _x[i][1] << "," << _x[i][2] << "," << endl;
}

void EventDisks::event_disks() {
	double t_pair;
	double t_wall;
	int k,l;
	int sphere,wall;
	tie(t_pair,k,l) = get_next_pair_time();
	tie(t_wall,sphere,wall) = get_next_wall_time();
	
	if (t_wall<t_pair){
		move_all(t_wall);
		wall_collision(sphere,wall);
	} else {
		move_all(t_pair);
		pair_collision(k,l);
	}
}
		
double EventDisks::get_pair_time(int i,int j) {
	auto DeltaX = array{_x[i][0]-_x[j][0], _x[i][1]-_x[j][1], _x[i][2]-_x[j][2]};
	auto DeltaV = array{_v[i][0]-_v[j][0], _v[i][1]-_v[j][1], _x[i][2]-_x[j][2]};
	auto DeltaX_Delta_V = _inner_product(DeltaX,DeltaV);
	auto V2 = _inner_product(DeltaV,DeltaV);
	auto Upsilon = DeltaX_Delta_V*DeltaX_Delta_V - V2 * (_inner_product(DeltaX,DeltaX) - 4*_sigma*_sigma);
	if (Upsilon > 0 && DeltaX_Delta_V < 0)
		return -(DeltaX_Delta_V + sqrt(Upsilon))/V2;
	else
		return  numeric_limits<double>::infinity();
}

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
		
double EventDisks::get_wall_time(int sphere, int wall) {
	if (_v[sphere][wall] > 0)
		return (_length-_x[sphere][wall])/_v[sphere][wall];
	if (_v[sphere][wall] < 0)
		return  _x[sphere][wall]/(-_v[sphere][wall]);
	return numeric_limits<double>::infinity();
}

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

void EventDisks::move_all(double t){
	for (int i=0;i<_n;i++)
		for (int j=0;j<_d;j++)
			_x[i][j] += (t * _v[i][j]);
}

void  EventDisks::wall_collision(int sphere,int wall) {
	cout << "Wall " << wall << " collision " << sphere << ": ("  << _x[sphere][0] << "," <<_x[sphere][1] << "," << _x[sphere][2] <<")"<< endl;
	_v[sphere][wall] = -_v[sphere][wall];
}
		
void  EventDisks::pair_collision(int k,int j) {
	cout << "Pair collision " << k <<"," <<j << endl;
	cout << _x[k][0] << "," <<_x[k][1] << "," << _x[k][2] << endl;
	cout << _x[j][0] << "," <<_x[j][1] << "," << _x[j][2] << endl;
	auto DeltaX = array{_x[k][0]-_x[j][0], _x[k][1]-_x[j][1], _x[k][2]-_x[j][2]};
	cout << sqrt(_inner_product(DeltaX,DeltaX)) << endl;
	exit(0);
}
