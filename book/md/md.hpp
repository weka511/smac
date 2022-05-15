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
 */

#ifndef _MD_HPP_
#define _MD_HPP_

#include "particle.hpp"
#include "configuration.hpp"

bool killed(std::string kill_file="kill.txt");

bool file_exists (const char *filename) {
  struct stat   buffer;   
  return (stat (filename, &buffer) == 0);
}

int evolve(Configuration& configuration,int N, int n,int d, int M, 
		double L, double V, double sigma, std::string output_path, int status, int freq);

void help(int N, int n,	int d ,	int M ,	int freq, bool restart,
			double L, double V,	double sigma,  std::string output_path, std::string restart_path);		

#endif

