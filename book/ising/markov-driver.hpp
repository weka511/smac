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
 *  This is the Driver program for MCMC Ising. It parses the command line
 *  arguments, then executes Markov Ising as many times as required.
 */
 
#ifndef _MARKOV_DRIVER_HPP_
#define _MARKOV_DRIVER_HPP_

using namespace std;

 int  execute(const string path, 
				const int n,
				const bool wrapped,
				const float beta,
				const int iterations,
				const int nruns,
				const int frequency,
				const int burn_in );
 
 #endif //_MARKOV_DRIVER_HPP_
 