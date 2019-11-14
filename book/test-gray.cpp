/**
 * Copyright (C) 2019 Greenweaves Software Limited
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
 * This file tests the grey code class
 */
 
#include "catch.hpp"
#include "gray.hpp"

TEST_CASE( "Gray Tests", "[grey]" ) {
	
	SECTION("Iterate Gray"){
		Gray gray(4);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==2);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==3);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==2);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==4);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==2);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==3);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==2);
		REQUIRE(gray.next()==1);
		REQUIRE(gray.next()==-1);
	}
	
	
}
