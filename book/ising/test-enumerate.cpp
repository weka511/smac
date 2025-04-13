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
 * This file tests the neighbour function
 */
 
 using namespace std;
 
 #include "catch.hpp"
#include "enumerate-ising.hpp"


TEST_CASE( "Enumerate Ising Tests", "[eit]" ) {
	
	SECTION("Test get_field: wrapped"){
		IsingEnumerator enumerator;
		vector<int> sigma;
		for (int i=0;i<9;i++)
			sigma.push_back(-1);
	
		REQUIRE(enumerator.get_field(sigma,5,3,true) == -4);
		REQUIRE(enumerator.get_field(sigma,4,3,true) == -4);
		sigma[1] = +1;
		REQUIRE(enumerator.get_field(sigma,5,3,true) == -2);
		REQUIRE(enumerator.get_field(sigma,4,3,true) == -4);
	}
	
	SECTION("Test get_field: not wrapped"){
		IsingEnumerator enumerator;
		vector<int> sigma;
		for (int i=0;i<9;i++)
			sigma.push_back(-1);
	
		REQUIRE(enumerator.get_field(sigma,5,3,false) == -4);
		REQUIRE(enumerator.get_field(sigma,4,3,false) == -3);
		sigma[1] = +1;
		sigma[5] = +1;
		REQUIRE(enumerator.get_field(sigma,5,3,false) == 0);
	}
	
	SECTION("Test enumeration"){
		IsingEnumerator enumerator;
		enumerator.enumerate_ising(4,true,false);
		REQUIRE(enumerator.Ns[make_pair(8,0)] ==  4224);
		REQUIRE(enumerator.Ns[make_pair(32,0)] ==  4);
		REQUIRE(enumerator.Ns[make_pair(-32,16)] ==  2);
		REQUIRE(enumerator.Ns[make_pair(0,4)] ==  5856);
	}
}
