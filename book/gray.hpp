/**
 * Copyright (C) 2019 Greenweaves Software Limited
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


class Gray {
  private:
	const int         _n;
	signed long long  _i;
	signed long long  _max;
	int*             _tau;
	
  public:
	Gray(int n): _n(n),_i(0),_max(1) {
		for (int i=0;i<n-1;i++)
			_max*=2;
		_max-=1;
		_tau = new int[n+1];
		for (int i=0;i<=n;)
			_tau[i] = ++i;
	}
	
	int next() {
		int k = _tau[0];
		if (k>_N) return -1;
		_tau[k-1]=_tau[k];
		_tau[k] = k+1;
		if (k != 1) _tau[0] = 1;
		return k;
	}
	
	virtual ~Gray() {delete [] _tau;}
};