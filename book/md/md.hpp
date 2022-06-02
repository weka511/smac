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
#include "params.hpp"
#include "history.hpp"

/**
 *  Used when we parse saved state.
 */
enum ParserState {
	START     = 0, 
	PARTICLES = 2
};


/**
 *   Check to see whether user wants to terminate program.
 */
bool killed(string kill_file="kill.txt");

/**
 *   Check to see whether a specified file exists
 */
bool file_exists (const char *filename);

/**
 *  Drive configuration forward a specified number of epochs
 */
int evolve( Configuration& configuration,
			string         output_path, 
			int            status, 
			ParameterSet   params,
			History        history,
			string         check_path = "check.csv",
			const int      epoch = 0);

/**
 *    Save configuration to specified file
 */
void save(  string    output_path,
			Configuration& configuration,
			int            epoch, 
			ParameterSet & params);


/**
 * Get date formatted for display
 */
string get_date_string();

#endif

