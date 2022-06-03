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
  
 using namespace std;

 #include "history.hpp"
 
/**
 * Open stream if user wants history stored.
 */	 
History::History(bool history, string path){
	if (history){
		_history = new ofstream(path);
		*_history << VERSION << endl;
	}
}

/**
 *   Report positions and velocities to history file.
 */
void History::report(HistoryPartner  *partner) {
	if (_history!=NULL)
		partner->report(_history);
}

History::~History(){
	if (_history!=NULL)
		_history->close();
}
 
 