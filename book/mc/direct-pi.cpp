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
 * Simple Monte-Carlo example, Algorithm 1.1, as described
 * in Statistical Mechanics: Algorithms and Computations, by Werner Krauth,
 * ISBN 978-0-19-851535-7.
 */
 
 #include <iostream>
 #include <random>
 #include <chrono> 
 
 using namespace std;
 
 int main() {
	auto seed = chrono::system_clock::now().time_since_epoch().count();
	auto rng = mt19937(seed);
	auto uniform_real = uniform_real_distribution<double> (-1.0, 1.0);
  
	auto n_hits = 0;
	auto N = 1000000000;
	for (auto i {0}; i < N; i++){
		auto x = uniform_real(rng);
		auto y = uniform_real(rng);
		if (x*x + y*y < 1)
			 n_hits ++;
	 } 
	 cout << (4.0 * n_hits) / N<< endl;
 }
 