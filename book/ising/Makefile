# Copyright (C) 2019-2025 Greenweaves Software Limited
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
SRCS      = markov-ising.cpp     \
            nbr.cpp              \
			enumerate-ising.cpp  \
			field.cpp

TESTS     = test-gray.cpp  	   \
		    test-nbr.cpp       \
			test-enumerate.cpp \
			test-markov.cpp    \
			test-field.cpp
		
OBJS1     = $(subst .cpp,.o,$(SRCS)) 
OBJS      = $(subst .cc,.o,$(OBJS1)) 
TEST_OBJS = $(subst .cpp,.o,$(TESTS))

THREADING = threading.exe

MAIN      = enumerate.exe
TEST_MAIN = tests.exe
MARKOV    = markov-driver.exe

TARGETS   = $(MAIN) $(MARKOV)

all : $(TARGETS) $(TEST_OBJS) $(MD)

run : all
	./$(MAIN)
	
tests : $(TEST_MAIN)
	./$(TEST_MAIN)
	
clean :
	${RM} *.o *.stackdump

rebuild: clean all tests

depend: .depend

install: rebuild
	cp $(MAIN) /usr/local/bin

grand: all tests
	
.depend: $(SRCS)  enumerate.cpp $(TESTS) tests.cpp markov-driver.cpp Makefile
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;
	sed -i -e 's/\/home\/Weka\/smac\/book\///$g' .depend
	
$(MAIN): $(OBJS) enumerate.o 
	${CXX} $(LDFLAGS) -o $(MAIN) enumerate.o ${OBJS} ${LDLIBS}
	
$(TEST_MAIN): $(OBJS) tests.o $(TEST_OBJS)
	${CXX} $(LDFLAGS) -o $(TEST_MAIN) tests.o ${OBJS} $(TEST_OBJS) ${LDLIBS}

$(MARKOV): $(OBJS) markov-driver.o 
	${CXX} $(LDFLAGS) -o $(MARKOV) markov-driver.o ${OBJS} ${LDLIBS}

mi : all
	 ./$(MARKOV) -n6 -b 0.25 -w -r 3

	
distclean: clean
	$(RM) *~ .depend

setup:
	-$(MKDIR) configs
	-$(MKDIR) imgs
	-$(MKDIR) logs
	
include .depend
