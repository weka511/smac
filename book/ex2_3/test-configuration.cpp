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
 * This file contains tests for the Configuration class
 */
 

#include "catch.hpp"
#include "configuration.hpp"

using namespace std;

double create_bad_configuration() {
	Configuration configuration(250, 1.0, 1.0, 1.0/32.0, 10);
	return 0;
}

TEST_CASE( "Configuration Tests", "[config]" ) {
	
	SECTION("Test distance"){
		Configuration configuration(10, 1.0, 1.0, 1.0/32.0, 10);
		REQUIRE(10==configuration.size());
		REQUIRE_THROWS_AS(create_bad_configuration(), runtime_error);
	}
	
}
