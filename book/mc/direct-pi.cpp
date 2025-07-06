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
 * Molecular dynamics simulation for hard disks or hard spheres, as described
 * in Statistical Mechanics: Algorithms and Computations, by Werner Krauth,
 * ISBN 978-0-19-851535-7. This program performs the calculations, and the data
 * in the outout files are analyzed by md-plot.py.
 */
 
 #include <iostream>
 #include <random>
 #include <chrono> 
 
 using namespace std;
 
 int main() {
	auto seed = std::chrono::system_clock::now().time_since_epoch().count();
	auto engine = mt19937(seed);
	auto dist = uniform_real_distribution<double> (-1.0, 1.0);
  
	auto n_hits = 0;
	auto N = 1000000;
	for (auto i = 0; i < N; i++){
		auto x = dist(engine);
		auto y = dist(engine);
		if (x*x + y*y < 1)
			 n_hits ++;
	 } 
	 cout << n_hits << endl;
 }
 