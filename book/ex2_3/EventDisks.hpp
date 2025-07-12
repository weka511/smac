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
		EventDisks(const int n=10, const double L=1.0, const double V=1.0, const double sigma = 1.0/16.0, const int m=100);
		
		void event_disks();
		
		double get_pair_time(int i,int j);
		
		tuple<double,int,int> get_next_pair_time();
		
		double get_wall_time(int sphere, int wall);
		
		tuple<double,int,int> get_next_wall_time();
		
		void move_all(double t);
		
		void wall_collision(int sphere, int wall);
		
		void pair_collision(int k,int j);
		
		double get_time() {return _t;}
		
	private:
		unique_ptr<double[][3]> _x;
		
		unique_ptr<double[][3]> _v;
		
		int _n;
		
		int _d = 3;
		
		int _length;
		
		double _sigma = 1.0/8.0;
		
		double _t = 0;
		
		/**
		 * Verify that configuration is valid, i.e. no two spheres overlap
		 */
		static bool _is_valid(unique_ptr<double[][3]> &x,const int n=100,  const double sigma = 1.0/8.0);
		
		static double _inner_product(array<double,3> &u,array<double,3> &v) {
			auto sum=0.0;
			for (int j=0;j<3;j++)
				sum += u[j]*v[j];
			return sum;
		}
		
	
};

#endif //_EVENT_DISKS_HPP_
	