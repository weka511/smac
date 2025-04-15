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
	
	SECTION("test field"){
		Field field;
		field.prepare(-16, 16, 2, 3);
		for (vector<CountedData>::const_iterator i = field.container.begin(); i < field.container.end(); i++) {
			row counts = i->second;
			REQUIRE(field.all_zero(counts));
		}
		REQUIRE(field.get_count(0,0) == 0);
		field.increment(-12,2);
		REQUIRE(field.get_count(12,2) == 0);
		int j = 0;
		for (vector<CountedData>::const_iterator i = field.container.begin(); i < field.container.end(); i++) {
			row counts = i->second;
			if (j==2)
				REQUIRE(!field.all_zero(counts));
			else
				REQUIRE(field.all_zero(counts));
			j++;
		}
	}
	
	
	
}
