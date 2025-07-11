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
#include "EventDisks.hpp"

using namespace std;

EventDisks::EventDisks(const int n, const double L, const double V): _n(n) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_real_distribution<> uniform_v(-V, V);
	std::uniform_real_distribution<> uniform_x(0.0, L);
	_x = make_unique<double[][3]>(n);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < _d; ++j)
			_x[i][j] = uniform_x(gen);

	_v = make_unique<double[][3]>(n);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < _d; ++j)
			_v[i][j] = uniform_v(gen);
		
	for (int i = 0; i < n; ++i)
		cout << "("<<_x[i][0] << "," << _x[i][1] <<"," << _x[i][2] <<"), ("<< _v[i][0] << "," << _v[i][1] <<"," << _v[i][2] << ")"<< endl;
}

void EventDisks::event_disks() {
	double t_pair, t_wall;
	int j,k,l;
	tie(t_pair,k,l) = get_next_pair_time();
	tie(t_wall,j) = get_next_wall_time();
	move_all(min(t_pair,t_wall));
	if (t_wall<t_pair)
		wall_collision(j);
	else
		pair_collision(k,j);
}
		
double EventDisks::get_pair_time(int i,int j) {
	double inf = numeric_limits<double>::infinity();
	return inf;
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
		
double EventDisks::get_wall_time(int i, int j) {
	double inf = std::numeric_limits<double>::infinity();
	return inf;
}

tuple<double,int> EventDisks::get_next_wall_time(){
	double t0 =  numeric_limits<double>::infinity();
	tuple<double,int> result = make_tuple(t0,-1);
	for (int i=0;i<_n;i++)
		for (int j=0;j<2*_d;j++){
			const double t1 = get_wall_time(i,j);
			if (t1 < t0){
				result = make_tuple(t1,i);
				t0 = t1;
			} 
		}
	return result;
}

void EventDisks::move_all(double t){}

void  EventDisks::wall_collision(int j) {}
		
void  EventDisks::pair_collision(int k,int j) {}
