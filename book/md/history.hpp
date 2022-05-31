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

#ifndef _HISTORY_HPP_
#define _HISTORY_HPP_

/**
 *  This class allows History to call back to Configuration 
 *  when it dumps the position and velocities
 */
class HistoryPartner {
  public:
     /**
      *   Used to report position to history file
	  */
     virtual void report(ofstream* output)=0;
};

/**
 *  This class is responsible for reporting history
 */
class History {
	ofstream * _history=NULL;
	
  public:
    /**
     * Open stream if user wants history stored.
     */	 
	History(bool history, string path){
		if (history)
			_history = new ofstream(path);
	}
	
	/**
	 *   Report positions and velocities to history file.
	 */
	void report(HistoryPartner  *partner) {
		if (_history!=NULL)
			partner->report(_history);
	}
	
	virtual ~History(){
		if (_history!=NULL)
			_history->close();
	}
};

#endif
