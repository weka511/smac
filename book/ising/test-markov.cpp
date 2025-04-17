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
 * This file tests methods of MarkovIsing
 */
 
#include <iostream>
#include <fstream>
#include <vector>
#include "catch.hpp"
#include "markov-ising.hpp"

float get_mean_count(MarkovIsing &markov, const int value, const int nruns) {
	float raw_count = 0;
	for (int i=0;i<nruns;i++)
		raw_count += markov.get_count(value,i);
	return raw_count / nruns;
}
TEST_CASE( "Markov Tests", "[markov]" ) {
	
	SECTION("Test MarkovIsing.get_field()"){
		ofstream out;
		out.open ("/dev/null");
		MarkovIsing markov(3,3,false,out,2.0,1);
		vector<int> spins = {-1, -1, -1,
							-1, -1, -1,
							-1, -1, -1
							};
		REQUIRE(-4 == markov.get_field(4,spins));
		spins[0] = +1;
		REQUIRE(-4 == markov.get_field(4,spins));
		spins[1] = +1;
		REQUIRE(-2 == markov.get_field(4,spins));	
		spins[7] = +1;
		REQUIRE(0 == markov.get_field(4,spins));		
	}
	
	
	SECTION("Test MarkovIsing.get_field()1"){
		ofstream out;
		out.open ("/dev/null");
		MarkovIsing markov(3,3,false,out,2.0,1);
		vector<int> spins = {-1, +1, -1,
							+1, -1, +1,
							-1, +1, -1
							};
		REQUIRE(+4 == markov.get_field(4,spins));
		spins[4] = -1;
		REQUIRE(+4 == markov.get_field(4,spins));
	}
	
	SECTION("Test MarkovIsing.Upsilon (based on Python version)"){
		ofstream out;
		out.open ("/dev/null");
		MarkovIsing markov(6,6,true,out,0.25,1);
		REQUIRE(markov.get_upsilon(0) == Approx(0.60653066).epsilon(0.0000001) );
		REQUIRE(markov.get_upsilon(1) == Approx(0.36787944).epsilon(0.0000001) );
		REQUIRE(markov.get_upsilon(2) == Approx(0.22313016).epsilon(0.0000001) );
		REQUIRE(markov.get_upsilon(3) == Approx(0.13533528).epsilon(0.0000001) );
	}
	
	SECTION("Test against enumeration"){
		const int nsteps = 100000;
		const int nruns = 100;
		const int nburn = 100000;
		ofstream out;
		out.open ("/dev/null");
		const double beta = 0.;
		MarkovIsing markov(4,4,true,out,beta,nruns);
		for (int i=0;i<nruns;i++)
			markov.run(nsteps,0,i,nburn);
		REQUIRE(markov.dump() == nsteps*nruns);
		REQUIRE(get_mean_count(markov,-4,nruns)/nsteps == Approx(13568/65536.).epsilon(100.0/65536) );
		REQUIRE(get_mean_count(markov,0,nruns)/nsteps == Approx(20524/65536.).epsilon(100.0/65536) );
		REQUIRE(get_mean_count(markov,4,nruns)/nsteps == Approx(13568/65536.).epsilon(100.0/65536) );
		REQUIRE(get_mean_count(markov,16,nruns)/nsteps == Approx(424/65536.).epsilon(1000.0/65536) );
	
		//TODO load enumeration data
	}
}
