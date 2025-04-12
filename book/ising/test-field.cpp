/**
 * Copyright (C) 2025 Greenweaves Software Limited
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
 * This file tests methods of Field
 */
 
#include <iostream>
#include <fstream>
#include <vector>
#include "catch.hpp"
#include "field.hpp"

TEST_CASE( "Markov Field", "[field]" ) {
	
	SECTION("Test MarkovIsing.get_field()"){
		// ofstream out;
		// out.open ("/dev/null");
		// MarkovIsing markov(3,3,false,out);
		// vector<int> spins = {-1, -1, -1,
							// -1, -1, -1,
							// -1, -1, -1
							// };
		// REQUIRE(-4 == markov.get_field(4,spins));
		// spins[0] = +1;
		// REQUIRE(-4 == markov.get_field(4,spins));
		// spins[1] = +1;
		// REQUIRE(-2 == markov.get_field(4,spins));	
		// spins[7] = +1;
		// REQUIRE(0 == markov.get_field(4,spins));		
	}
	
	
	
}
