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
#include "configuration.hpp"

using namespace std;

class EventDisks {
  private:
	const double _dt_sample;
	double _t = 0;
	
  public: 
	EventDisks(double dt_sample) : _dt_sample(dt_sample) {};
    void event_disks(Configuration& configuration) {;}
	/**
	 *  Accessor for current time
	 */
	double get_time() {return _t;}
	
};

#endif // _EVENT_DISKS_HPP_
