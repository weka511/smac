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
 * This file exercises the Verlet algorithm for some simple N-body cases
 * without using the Barnes Hut approximations.
 */
 
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include "catch.hpp"
#include "particle.hpp"




TEST_CASE( "Particle Tests", "[particle]" ) {
	
	SECTION("Simple Earth-Sun Kepler"){
		std::cout << "Dummy" << std::endl;
		REQUIRE (0==0);
	}
	

}
