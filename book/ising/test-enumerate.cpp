/**
 * Copyright (C) 2019-2025 Greenweaves Software Limited
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
 * This file tests the neighbour function
 */
 
 using namespace std;
 
#include "catch.hpp"
#include "enumerate-ising.hpp"


TEST_CASE( "Enumerate Ising Tests", "[eit]" ) {
	
	SECTION("Test get_field: wrapped"){
		vector<int> sigma;
		for (int i=0;i<9;i++)
			sigma.push_back(-1);
	
		REQUIRE(get_field(sigma,5,3,true) == -4);
		REQUIRE(get_field(sigma,4,3,true) == -4);
	}
	
	SECTION("Test get_field: not wrapped"){
		vector<int> sigma;
		for (int i=0;i<9;i++)
			sigma.push_back(-1);
	
		REQUIRE(get_field(sigma,5,3,false) == -4);
		REQUIRE(get_field(sigma,4,3,false) == -3);
	}
}
