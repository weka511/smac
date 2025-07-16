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

#ifndef _EVENT_HPP_
#define _EVENT_HPP_

#include <memory>
#include "particle.hpp"

using namespace std;

class Event {
  public:
    virtual void execute() = 0;
};

class CollisionEvent : public Event {
	shared_ptr<Particle> _particle1;
};

class WallCollisionEvent : public CollisionEvent  {
	const int wall=0;
	void execute();
};

class ParticleCollisionEvent : public CollisionEvent  {
	shared_ptr<Particle> _particle2;
	void execute();
};


class SampleEvent : public Event {
	void execute();
};

#endif // _EVENT_HPP_
