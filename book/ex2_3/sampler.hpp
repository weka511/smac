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
 */
 
#ifndef _SAMPLER_HPP_
#define _SAMPLER_HPP_

#include <fstream>
#include <string>
#include "configuration.hpp"

using namespace std;

/**
 * This class is responsible for sampling the positions and velocities of all particles,
 * and writing them to a file.
 */
class Sampler {
	
  public:
	Sampler(int n,string file_name);
	
	/**
	 * Sample configuration at a specified time.
	 */
    void sample(double t,Configuration& configuration);
	
	/**
	 * Used to close output stresm.
	 */
	virtual ~Sampler();
	
  private:
	/**
	 * Number of particles
	 */
     int _n;
	 
	 std::ofstream _outputFile;
};

#endif // _SAMPLER_HPP_
