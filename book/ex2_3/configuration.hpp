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

#ifndef _CONFIGURATION_HPP_
#define _CONFIGURATION_HPP_

#include <memory>
#include "particle.hpp"

using namespace std;

class Configuration {
  private:
    unique_ptr<Particle[]> _particles;
	const int _n;
  public:
	Configuration(const int n, const double L, const double V, const double sigma, 
						const int m);
	int size() {return _n;};
	
  private:
    bool static _is_valid(unique_ptr<Particle[]> & particles,const int n,const double sigma);
};

#endif // _CONFIGURATION_HPP_
