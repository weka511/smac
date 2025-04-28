# md Molecular dynamics

Implementation of Algorithm 2.3 Pair collision

File||Problem/Algorithm/Description
--------------|--------------|---------------------------------------------------------------------------------------
Makefile||
configuration.cpp|configuration.hpp|Manage a box full of particles
history.cpp|history.hpp|Used to store positions and velocities to history file.
md.cpp|md.hpp|Algorithm 2.3 Pair collision
params.cpp|params.hpp|Manage ParameterSet, created from command line parameters
particle.cpp|particle.hpp|Represents one single particle
test-particle.cpp||Tests for particle.cpp
test.cpp|catch.hpp|Unit test framework
