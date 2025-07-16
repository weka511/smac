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
CPPFLAGS = -g -O3  -D_RUNTIME_CHECKS -pthread -I/sw/include/root  -std=c++23 -DVERSION="\"$(GIT_VERSION)\""
LDFLAGS = -g -O3
LDLIBS =
CXX = g++
RM = rm -f
MKDIR = mkdir
SRCS = params.cpp sampler.cpp particle.cpp configuration.cpp event-disks.cpp
OBJS = $(subst .cpp,.o,$(SRCS)) 
MAIN = ex2_3.exe
TARGETS = $(MAIN) 
TESTS = test-particle.cpp	test-configuration.cpp
TEST_OBJS = $(subst .cpp,.o,$(TESTS))
TEST_MAIN = tests.exe

all : $(MAIN)

run : all 
	./$(MAIN)
	
tests : $(TEST_MAIN)
	./$(TEST_MAIN)
	
clean :
	${RM} *.o *.stackdump

rebuild: clean all

depend: Makefile .depend 

install: rebuild
	cp $(MAIN) /usr/local/bin
	
.depend: $(SRCS) $(TESTS)  ex2_3.cpp
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;
	sed -i -e 's/\/home\/Weka\/smac\/book\///$g' .depend
	
$(MAIN): $(OBJS) ex2_3.o
	${CXX} $(LDFLAGS) -o  $(MAIN) ex2_3.o ${OBJS} ${LDLIBS}

$(TEST_MAIN): $(OBJS) tests.o $(TEST_OBJS)
	${CXX} $(LDFLAGS) -o $(TEST_MAIN) tests.o ${OBJS} $(TEST_OBJS) ${LDLIBS}
	
distclean: clean
	$(RM) *~ .depend

setup:
	-$(MKDIR) configs
	-$(MKDIR) imgs
	-$(MKDIR) logs
	
include .depend
