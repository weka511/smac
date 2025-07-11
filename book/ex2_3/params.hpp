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
 
#ifndef _PARAMS_HPP_
#define _PARAMS_HPP_

#include <string>
using namespace std;

 /**
 * This class looks after command line paramters.
 */ 
class ParameterSet {
  public:
	int    N               = 10000;
	int    n               = 100;
	int    d               = 3;
	bool   parsing_error   = false;
	
	/**
	 *  Create ParameterSet from command line parameters
	 */
	ParameterSet(int argc, char **argv);
	

	
  private:	
	
  void _extract(const int c);
  
	/**
	 * Display help text.
	 */
	void _help();
	

};

#endif //_PARAMS_HPP_
	