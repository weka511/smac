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
 * This file tests the neighbour function
 */
 
#include "catch.hpp"
#include "nbr.hpp"


TEST_CASE( "NBR Tests", "[nbr]" ) {
	
	SECTION("Test nbr against SMAC fig 5-2"){
		REQUIRE(nbr(1,1,3)==2);
		REQUIRE(nbr(1,2,3)==4);
		REQUIRE(nbr(1,3,3)==-1);
		REQUIRE(nbr(1,4,3)==-1);
		REQUIRE(nbr(2,1,3)==3);
		REQUIRE(nbr(2,2,3)==5);
		REQUIRE(nbr(2,3,3)==1);
		REQUIRE(nbr(2,4,3)==-1);
		REQUIRE(nbr(3,1,3)==-1);
		REQUIRE(nbr(3,2,3)==6);
		REQUIRE(nbr(3,3,3)==2);
		REQUIRE(nbr(3,4,3)==-1);
		REQUIRE(nbr(4,1,3)==5);
		REQUIRE(nbr(4,2,3)==7);
		REQUIRE(nbr(4,3,3)==-1);
		REQUIRE(nbr(4,4,3)==1);
		REQUIRE(nbr(5,1,3)==6);
		REQUIRE(nbr(5,2,3)==8);
		REQUIRE(nbr(5,3,3)==4);
		REQUIRE(nbr(5,4,3)==2);
		REQUIRE(nbr(6,1,3)==-1);
		REQUIRE(nbr(6,2,3)==9);
		REQUIRE(nbr(6,3,3)==5);
		REQUIRE(nbr(6,4,3)==3);
		REQUIRE(nbr(7,1,3)==8);
		REQUIRE(nbr(7,2,3)==-1);
		REQUIRE(nbr(7,3,3)==-1);
		REQUIRE(nbr(7,4,3)==4);
		REQUIRE(nbr(8,1,3)==9);
		REQUIRE(nbr(8,2,3)==-1);
		REQUIRE(nbr(8,3,3)==7);
		REQUIRE(nbr(8,4,3)==5);
		REQUIRE(nbr(9,1,3)==-1);
		REQUIRE(nbr(9,2,3)==-1);
		REQUIRE(nbr(9,3,3)==8);
		REQUIRE(nbr(9,4,3)==6);
	}
	
	SECTION("Test nbr against SMAC fig 5-2, wrapped"){
		REQUIRE(nbr(1,1,3,true)==2);
		REQUIRE(nbr(1,2,3,true)==4);
		REQUIRE(nbr(1,3,3,true)==3);
		REQUIRE(nbr(1,4,3,true)==7);
		REQUIRE(nbr(2,1,3,true)==3);
		REQUIRE(nbr(2,2,3,true)==5);
		REQUIRE(nbr(2,3,3,true)==1);
		REQUIRE(nbr(2,4,3,true)==8);
		REQUIRE(nbr(3,1,3,true)==1);
		REQUIRE(nbr(3,2,3,true)==6);
		REQUIRE(nbr(3,3,3,true)==2);
		REQUIRE(nbr(3,4,3,true)==9);
		REQUIRE(nbr(4,1,3,true)==5);
		REQUIRE(nbr(4,2,3,true)==7);
		REQUIRE(nbr(4,3,3,true)==6);
		REQUIRE(nbr(4,4,3,true)==1);
		REQUIRE(nbr(5,1,3,true)==6);
		REQUIRE(nbr(5,2,3,true)==8);
		REQUIRE(nbr(5,3,3,true)==4);
		REQUIRE(nbr(5,4,3,true)==2);
		REQUIRE(nbr(6,1,3,true)==4);
		REQUIRE(nbr(6,2,3,true)==9);
		REQUIRE(nbr(6,3,3,true)==5);
		REQUIRE(nbr(6,4,3,true)==3);
		REQUIRE(nbr(7,1,3,true)==8);
		REQUIRE(nbr(7,2,3,true)==1);
		REQUIRE(nbr(7,3,3,true)==9);
		REQUIRE(nbr(7,4,3,true)==4);
		REQUIRE(nbr(8,1,3,true)==9);
		REQUIRE(nbr(8,2,3,true)==2);
		REQUIRE(nbr(8,3,3,true)==7);
		REQUIRE(nbr(8,4,3,true)==5);
		REQUIRE(nbr(9,1,3,true)==7);
		REQUIRE(nbr(9,2,3,true)==3);
		REQUIRE(nbr(9,3,3,true)==8);
		REQUIRE(nbr(9,4,3,true)==6);
	}	
}
