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
 * This file contains tests for the Particle class
 */
 
#include <cmath>
#include "catch.hpp"
#include "particle.hpp"

TEST_CASE( "Particle Tests", "[particle]" ) {
	
	SECTION("Test distance"){
		Particle particle_1(1,2,3);
		Particle particle_2;
		Particle particle_3(3,2,1);
		REQUIRE(sqrt(14.0) == particle_1.get_distance(particle_2));
		REQUIRE(sqrt(14.0) == particle_2.get_distance(particle_1));
		REQUIRE(0.0 == particle_1.get_distance(particle_1));
		REQUIRE(sqrt(8.0) == particle_1.get_distance(particle_3));
	}
}
