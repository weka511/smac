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
 */

#ifndef _MARKOV_FIELD_HPP_
#define _MARKOV_FIELD_HPP_

#include <utility>
#include <vector>
#include <fstream>

using namespace std;

/**
 * This type represents a collection of counts from different runs
 */
typedef vector<int> row;

/**
 * This type represents a value (Energy or Magnetism), plus its collection of counts from different runs
 */
typedef pair<int,row> CountedData;

/**
 *  This class is used to record counts of energy and magnetization
 */
class Field: public vector<pair<int,int>>{
	private:
		
		/**
		 * The next three fields record the allowable values of the firld, which
		 * are min, min+step, ,,, max.
		 */
		int min;
		int max;
		int step;
		
		/**
		 * Number of columns in data table, one for each run.
		 */ 
		int width;

	public:		
		/**
		 * This method verifies that a particular row comprises all zeros.
		 */
		bool all_zero(row counts) {
			for (vector<int>::const_iterator j = counts.begin(); j < counts.end(); j++)
				if (*j > 0) return false;
			return true;
		}
		
		vector<CountedData> container;
		
	    /**
		 * Used to initialize data storage to all zeros
		 */
		void prepare(const int min, const int max, const int step, const int width);
	
		/**
		 * Used to increment Energies or Magnetization
		 */
		void increment(const int value,const int run);
		
		/**
		 * Accessor to retrieve count for a specified value
		 */
		int get_count(const int value, const int run);
		
		/**
		 * Used to output data.
		 *
		 * Returns: Total of all counts
		 */
		int dump(ofstream & out,std::string header);
		
};

#endif //_MARKOV_FIELD_HPP_
