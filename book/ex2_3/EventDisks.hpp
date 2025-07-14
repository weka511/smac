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
#include <string>
#include "sampler.hpp"

using namespace std;

/**
 * This class simulates collisions between molecules and the wall.
 */
class EventDisks {
	
	public:	
		/**
		 *  Create a valid configuration, comprising positions and velocites.
		 */
		EventDisks(const int n=10, const double L=1.0, const double V=1.0, 
					const double sigma = 1.0/16.0, const int m=100, double dt_sample=1.0, string sample_file = "samples.csv");
		
		/**
         * Algorithm 2.1: perform one step of the simulation. Determine time to next collision,
         * of either type, update all positions to just befroe collision,
		 * then update velocities to just after.
		 */
		void event_disks();
		
		/**
		 * Algorithm 2.2: calculate time to the next collision of two specified spheres.
		 */ 
		double get_pair_time(int i,int j);
		
		/**
		 * Calculate time to the next collision of any two spheres.
		 */ 	
		tuple<double,int,int> get_next_pair_time();
		
		/**
		 * Calculate time to next collision between a specified sphere and specified wall
		*/
		double get_wall_time(int sphere, int wall);
		
		/**
		 * Calculate time to next collision between any sphere and any wall
		 */
		tuple<double,int,int> get_next_wall_time();
		
		/**
		 *  Run configuration forward for a specified time interval,
		 *  and sample data if it is time.
		 */
		void move_and_sample(double dt);
		
		/**
		  *  Run configuration forward for a specified time interval, updating current time and positions.
		  */
		double move_all_spheres(double dt,double time_new);
		
		/**
		 *  Collide sphere with wall, reversion velocity component normal to wall
		 */
		void wall_collision(int sphere, int wall);
		
		/**
		 *  Collide two spheres, reversing velocity components normal to tangent plane
		 */	
		void pair_collision(int k,int j);
		
		/**
		 *  Accessor for current time
		 */
		double get_time() {return _t;}
		
	private:
		/**
		 *   Positions of centres of spheres
		 */
		unique_ptr<double[][3]> _x;
		
		/**
		 *   Velocities of spheres
		 */
		unique_ptr<double[][3]> _v;
		
		/**
		 *   Number of spheres
		 */
		int _n;
		
		/**
		 * Dimension of space (used for documentation only)
		 */
		int _d = 3;
		
		/**
		 * Length of one side of box.
		 */
		int _length;
		
		/**
		 * Radius of sphere
		 */
		double _sigma = 1.0/8.0;
		
		/**
		 * Current time in simulation
		 */
		double _t = 0.0;
		
		double dt_sample = 1.0;
		
		int n_sampled = 0;
		
		//Sampler _sampler = Sampler();
		unique_ptr<Sampler> _sampler;
		/**
		 * Validate configuration: make sure no two sphere overlap
		 */ 
		static bool _is_valid(unique_ptr<double[][3]> &x,const int n=100,  const double sigma = 1.0/8.0);
		
		/**
		 * Calculate inner product of two vectors.
		 */
		static double _inner_product(array<double,3> &u,array<double,3> &v) {
			auto sum=0.0;
			for (int j=0;j<3;j++)
				sum += u[j]*v[j];
			return sum;
		}
};

#endif //_EVENT_DISKS_HPP_
	