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
 
#include <iostream>
#include <cassert>

#include "field.hpp"

using namespace std;

/**
 * Used to initialize data storage to all zeros
 */
void Field::prepare(const int min, const int max, const int step, const int width){
	row zeros;
	for (int j=0;j<width;j++)
		zeros.push_back(0);
	for (int i=min;i<=max;i+=step)
		container.push_back(make_pair(i,zeros));
	this->min = min;
	this->step = step;
	this->max = max;
}

/**
 * Used to increment Energies or Magnetization
 */
void Field::increment(const int value,const int run){
	const int k = (value - min)/step;
	if (k < 0 or k >= container.size()){
		std::cout << __FILE__ << " " << __LINE__ <<": k="<<value <<",min="<< min <<",max="<<max<<",step="<<step<<std::endl;
		return;
	}
	assert (0 <=k and k<container.size());
	const int i = container[k].first;
	row the_row = container[k].second;
	the_row[run]++;
	container[k] = make_pair(i,the_row);
}

/**
 * Accessor to retrieve count for a specified value
 */
int Field::get_count(const int value, const int run) {
	const int k = (value - min)/step;
	assert (0 <=k and k<container.size());
	const int i = container[k].first;
	assert(i == value);
	row r = container[k].second;
	return r[run];
}


/**
  * Used to output data.
  *
  * Returns: Total of all counts
  */
int Field::dump(ofstream & out,std::string header){
	int total_count = 0;
	out << header << std::endl;
	for (vector<CountedData>::const_iterator i = container.begin(); i < container.end(); i++) {
		row counts = i->second;
		if (all_zero(counts))	continue;
		
		out << i->first;
		for (vector<int>::const_iterator j = counts.begin(); j < counts.end(); j++){
			total_count += *j;
			out << "," << *j;
		}
		out  << std::endl;	
	}
	return total_count;
}

