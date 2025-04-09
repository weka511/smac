# Ising

C++ implementations of Algorithm 5.3 (single flip enumeration for the Ising model) and 5.7 (MCMC)

File|Description
------------------|-----------------------------------------------------------------------------------------------------------------------
catch.hpp|Support for Test harness for enumerate-ising.cpp
enumerate-ising.cpp|Algorithm 5.3: single flip enumeration for the Ising model.
enumerate-ising.hpp|Algorithm 5.3: single flip enumeration for the Ising model.
gray.hpp|Greycode for enumerate-ising.cpp, plus iterator for neighbours
Makefile|Makefile for enumerate-ising.cpp and markov-driver.cpp
markov-driver.cpp|Execute MCMC
markov-ising.cpp|Algorithm 5.3: MCMC for Ising
markov-ising.hpp|MCMC for Ising
nbr.cpp|Calculate neighbours
nbr.hpp|Calculate neighbours
test-gray.cpp|Tests for gray.hpp
test-nbr.cpp|Tests for nbr.cpp
test-markov.cpp|Tests for markov-ising.cpp
tests.cpp|Test harness for enumerate-ising.cpp
