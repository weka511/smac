# Copyright (C) 2019-2022 Greenweaves Software Limited
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
SRCS      = configuration.cpp 	\
			particle.cpp 		\
			params.cpp 			\
			history.cpp

TESTS     = test-particle.cpp	
		
OBJS1     = $(subst .cpp,.o,$(SRCS)) 
OBJS      = $(subst .cc,.o,$(OBJS1)) 
TEST_OBJS = $(subst .cpp,.o,$(TESTS))

THREADING = threading.exe

MAIN      = md.exe
TARGETS   = $(MAIN) 
TEST_MAIN = tests.exe

all : $(MAIN)

run : all 
	${RM} foo.csv
	./$(MAIN)
	
tests : $(TEST_MAIN)
	./$(TEST_MAIN)
	
clean :
	${RM} *.o *.stackdump

rebuild: clean all

depend: Makefile .depend

install: rebuild
	cp $(MAIN) /usr/local/bin
	
.depend: $(SRCS)   $(TESTS)  md.cpp
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;
	sed -i -e 's/\/home\/Weka\/smac\/book\///$g' .depend
	
$(MAIN): $(OBJS) md.o 
	${CXX} $(LDFLAGS) -o $(MAIN) md.o ${OBJS} ${LDLIBS}
	
$(TEST_MAIN): $(OBJS) tests.o $(TEST_OBJS)
	${CXX} $(LDFLAGS) -o $(TEST_MAIN) tests.o ${OBJS} $(TEST_OBJS) ${LDLIBS}
	
distclean: clean
	$(RM) *~ .depend

setup:
	-$(MKDIR) configs
	-$(MKDIR) imgs
	-$(MKDIR) logs
	
include .depend
