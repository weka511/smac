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

#include <memory>
#include <cassert>
#include "configuration.hpp"
#include "sampler.hpp"

using namespace std;

class EventDisks {
	
  private:
	/**
	 *    Time interval between samples
	 */
	const double _dt_sample;

	/**
	 * Current time in simulation
	 */
	double _t = 0.0;
	
	/**
	 *   Used to record time when we next need to sample. Calculated from
	 */
	double _t_next_sample_due = 0.0;
		
	/**
	 * Number of samples at present time.
	 */
	int _n_sampled = 0;
		
	Sampler& _sampler;
	
	Configuration& _configuration;
	
  public: 
	EventDisks(double dt_sample,Configuration& configuration, Sampler& sampler);

	/**
	 * Algorithm 2.1: perform one step of the simulation. Determine time to next collision,
	 * of either type, update all positions to just befroe collision,
	 * then update velocities to just after.
	 */	
    void event_disks();
	
	/**
	 *  Accessor for current time
	 */
	double get_time() {return _t;}
	
  private:
	/**
	 *   Used to determine  when we next need to sample.
	 */
	double get_t_next_sample_due() {return (_n_sampled+1) * _dt_sample;}
	
};

#endif // _EVENT_DISKS_HPP_
