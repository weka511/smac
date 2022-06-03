/**
 * Copyright (C) 2022 Greenweaves Software Limited
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
 

#include "catch.hpp"
#include "particle.hpp"

TEST_CASE( "Particle Tests", "[particle]" ) {
	
	SECTION("Test distance"){
		double O[] = {0.0, 0.0, 0.0, 0.0};
		Particle p0(2, O);
		double A[] = {3.0, 0.0, 0.0, 0.0};
		Particle p1(2, A);
		double B[] = {0.0, 4.0, 0.0, 0.0};
		Particle p2(2, B);
		REQUIRE (9== p0.get_dist_sq(&p1));
		REQUIRE (16== p2.get_dist_sq(&p0));
		REQUIRE (25== p1.get_dist_sq(&p2));
	}
	
	SECTION("Test gap between two vectors"){
		double O[] = {0.0, 0.0, 0.0, 0.0};
		Particle p0(2, O);
		double A[] = {3.0, 0.0};
		double B[] = {0.0, 4.0};
		double Delta[2];
		p0.delta(A, B, Delta);
		REQUIRE (3.0 == Delta[0]);
		REQUIRE (-4.0 == Delta[1]);
	}
	
	SECTION("Test inner product"){
		double O[] = {0.0,0.0,0.0,0.0};
		Particle p0(2,O);
		double A[] = {1, 2, 3};
		double B[] = {4, 5, 6};
		REQUIRE(14.0 == p0.get_inner_product(A,B));
		double O3[] = {0.0,0.0,0.0,0.0,0.0,0.0};
		Particle p3(23,O3);
		REQUIRE(32.0 == p3.get_inner_product(A,B));
	}
	
	SECTION("Test time to wall"){
		double O1[] = {0.1,0.0,0.2,0.0};
		Particle p1(2,O1);
		REQUIRE(0.9/0.2 == p1.get_time_to_wall(0,1.0));
		double O2[] = {-0.1,0.0,0.2,0.0};
		Particle p2(2,O2);
		REQUIRE(1.1/0.2 == p2.get_time_to_wall(0,1.0));
		double O3[] = {0.1,0.0,-0.2,0.0};
		Particle p3(2,O3);
		REQUIRE(1.1/0.2 == p3.get_time_to_wall(0,1.0));
		double O4[] = {-0.1,0.25,-0.2,0.3};
		Particle p4(2,O4);
		REQUIRE(0.9/0.2 == p4.get_time_to_wall(0,1.0));
		REQUIRE((0.95-0.25)/0.3 == p4.get_time_to_wall(1,0.95));
	}
	
	SECTION("Test time to other particle"){
		double O1[] = {1.0,0.0,-2.0,1.0};
		Particle p1(2,O1);
		double O2[] = {-1,0.0,1,1};
		Particle p2(2,O2);
		double sigma = 0.1;
		double t = p1.get_time_to_particle(&p2,sigma);
		p1.evolve(t);
		p2.evolve(t);
		REQUIRE(4*sigma*sigma == Approx(p1.get_dist_sq(&p2)));
	}
	
	SECTION("Test wall collision"){
		double O1[] = {1.0,0.0,2.0,1.0};
		Particle p1(2,O1);
		p1.collide(0);
		REQUIRE(-2.0 == p1.get_velocity(0));
		REQUIRE(1.0 == p1.get_velocity(1));
	}
	
	SECTION("Test particle collision"){
		double O1[] = {1.0,0.0,-2.0,1.0};
		Particle p1(2,O1);
		double O2[] = {-1,0.0,1,1};
		Particle p2(2,O2);
		double E = p1.get_energy()+p2.get_energy();
		p1.collide(&p2);
		REQUIRE(E==Approx(p1.get_energy()+p2.get_energy()));
	}

}
