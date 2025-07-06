# Copyright (C) 2025 Simon Crase
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>
#
# Makefile snarfed from https://stackoverflow.com/questions/2481269/how-to-make-a-simple-c-makefile

GIT_VERSION := $(shell git describe --tags)
CPPFLAGS  = -g -O3  -D_RUNTIME_CHECKS -pthread -I/sw/include/root  -std=gnu++11 -DVERSION="\"$(GIT_VERSION)\""
LDFLAGS   = -g -O3
LDLIBS    =
CC        = gcc
CXX       = g++
RM        = rm -f
MKDIR     = mkdir
SRCS      =  	

		
OBJS1     = $(subst .cpp,.o,$(SRCS)) 
OBJS      = $(subst .cc,.o,$(OBJS1)) 


MAIN      = direct-pi.exe
TARGETS   = $(MAIN) 

all : $(MAIN)

run : all 
	./$(MAIN)
	

	
clean :
	${RM} *.o *.stackdump

rebuild: clean all

depend: Makefile .depend

install: rebuild
	cp $(MAIN) /usr/local/bin
	
.depend: $(SRCS)   direct-pi.cpp
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;
	sed -i -e 's/\/home\/Weka\/smac\/book\///$g' .depend
	
$(MAIN): $(OBJS) direct-pi.o 
	${CXX} $(LDFLAGS) -o $(MAIN) direct-pi.o ${OBJS} ${LDLIBS}
	

distclean: clean
	$(RM) *~ .depend


include .depend
