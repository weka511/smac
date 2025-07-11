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
 
#ifndef _EVENT_DISKS_HPP_
#define _EVENT_DISKS_HPP_

#include <array>
#include <memory>
#include <tuple>

using namespace std;

class EventDisks {
	public:
		EventDisks(const int n, const double L=1.0, const double V=1.0, const double sigma = 1.0/8.0);
		
		void event_disks();
		
		double get_pair_time(int i,int j);
		
		tuple<double,int,int> get_next_pair_time();
		
		double get_wall_time(int i, int wall);
		
		tuple<double,int> get_next_wall_time();
		
		void move_all(double t);
		
		void wall_collision(int j);
		
		void pair_collision(int k,int j);
		
	private:
		unique_ptr<double[][3]> _x;
		unique_ptr<double[][3]> _v;
		int _n;
		int _d = 3;
		double _sigma = 1.0/8.0;
		
		double _inner_product(array<double,3> &u,array<double,3> &v) {
			return u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
		}
};

#endif //_EVENT_DISKS_HPP_
	