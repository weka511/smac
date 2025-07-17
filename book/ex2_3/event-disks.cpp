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

#include "event-disks.hpp"

using namespace std;

EventDisks::EventDisks(double dt_sample,Configuration& configuration, Sampler& sampler)
  : _dt_sample(dt_sample),_sampler(sampler),_configuration(configuration) {
};

/**
 * Algorithm 2.1: perform one step of the simulation. Determine time to next collision,
 * of either type, update all positions to just befroe collision,
 * then update velocities to just after.
 */	
void EventDisks::event_disks() {
	double dt_pair;
	int k,l;
	tie(dt_pair,k,l) = _configuration.get_next_pair_collision();
	double dt_wall;
	int sphere,wall;
	tie(dt_wall,sphere,wall) = _configuration.get_next_wall_collision();
	double dt_next_collision = min(dt_wall,dt_pair);
	double t_next_collision = _t + dt_next_collision;
	while (t_next_collision > get_t_next_sample_due()) {
		_configuration.evolve(get_t_next_sample_due() - _t);
		_t = get_t_next_sample_due();
		_sampler.sample(_t,_configuration);
		_n_sampled ++;
	}
	
	_configuration.evolve(t_next_collision - _t);
	
	if (dt_wall < dt_pair)
		_configuration.wall_collision(sphere,wall);
	else
		_configuration.collide(k,l);
	
	_t = t_next_collision;
}