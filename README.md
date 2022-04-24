# Statistical Mechanics and Computations

Code I have written for course: *Statistical Mechanics and Computations*
 and also to familiarize myself with _git_. Includes exercises from the textbook
*Statistical Mechanics: Algorithms and Computations* by *Werner Krauth*.

## From the Course

#|Folder|File|Description
--|---------|------------------|---------------------------------------------------------------
1|Lectures||
-|Tutorial||
-|Homework||
2|Lectures||
-|Tutorial||
-|Homework||
3|Lectures||
-|Tutorial||
-|Homework||
4|Lectures||
-|Tutorial||
-|Homework||
5|Lectures||
-|Tutorial||
-|Homework||
6|[Lectures](https://github.com/weka511/smac/tree/master/lecture_6)|continuous_random_walk.py|
|||levy_free_path.py|
|||levy_harmonic_path.py |
|||levy_harmonic_path_3D.py|
|||levy_harmonic_path_movie.py |
|||naive_harmonic_path.py |
|||naive_path_slice.py|
|||naive_path_slice_movie.py |
|||trivial_free_path.py|Generate a random walk, then pull back as described in Lecture 6, 20:12. Compare result with Lévy free path
-|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_6)|naive_boson_trap.py|
|||naive_single_particle.py |
-|[Homework](https://github.com/weka511/smac/tree/master/homework_6)|a1.py|
|||a2.py|
|||a3.py|
|||b1.py|
|||b2.py|
|||b3.py|
|||c1.py|
|||c2.py|
7|Lectures||
-|Tutorial||
-|Homework||
8|Lectures||
-|Tutorial||
-|Homework||
9|Lectures||
-|Tutorial||
-|Homework||
10|Lectures||
-|Tutorial||
-|Homework||


## From the Book


#|File|Problem/Algorithm/Description
-----|--------------|---------------------------------------------------------------------------------------
|template.py|Template for python programs
1|smac.c|Useful functions: BoxMuller, CircleThrowing, and SphereGenerator
1.1|direct-plot.py|Implement Algorithm 1.1. Plot error and investigate relationship with N.
-| markov-pi.py|Implement Algorithm 1.2. Plot error and rejection rate.
-|direct.py|1.3 Store state in file
-|smacfiletoken.py|
-|markov-discrete-pebble.py| 1.4 Use table
-|large-markov.py|
-|transfer.m|1.8 Eigenvalues of transfer matrix
-|sphere-test.py|1.13 Vectors within Uniform sphere
1.2|permutation.py|1.9 Sample permutations using Alg. 1.11 and verify that it generate all 120 permutations of 5 elements equally often
-|permutation-histogram.py
-|naivegauss.py|1.12 Gauss
-|boxmuller.py|
-|direct-surface.py|Monte Carlo simulation of Exercise 2.11 of Chaosbook: in higher dimensions, any two vectors are nearly orthogonal
1.3|binomialconvolution.py|1.18 Binomial Convolution
1.4.2|direct-gamma.py|1.22 Importance sampling:Implement Algorithm 1.29, subtract mean value for each sample, and generate histograms of the average of N samples  and the rescaled averages.
-|direct-gamma-zeta.py|
-|markov-zeta.py|Algorithm 1.31, use of Markov Chain to detect non-integrable singularity.
1.4.4|levy-convolution.py|Algorithm 1.32
2.2|directDisksAny.py|
3.1|harmonic_wavefunction.py|Exercise 3.1: verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator
-|harmonic_density.py|Exercise 3.2: determine density matrix
3.2|matrix-square.py|Exercise 3.4: implement Alg 3.3, matrix-square
-|matrix-square-check.py|Exercise 3.4: check results of matrix squaring against exact solution.
-|poeschl-teller.py|Exercise 3.5: plot Poeschl-Teller potential and investigate density matrix and partition function
3.3||The Feynman path integral
3.4||Pair density matrices
3.5||Geometry of Paths
4|| Bosons
5|| Order and disorder in spin systems
5.1||The Ising model - exact computations
|catch.hpp|Support for Test harness for enumerate-ising.cpp
|gray.py|Algorithm 5.2: Gray code for spine {1,...N}.
|enumerate-ising.py|Algorithm 5.3: single flip enumeration for the Ising model.
|enumerate-ising.cpp|Algorithm 5.3: single flip enumeration for the Ising model.
|enumerate-ising.hpp|Algorithm 5.3: single flip enumeration for the Ising model.
|gray.hpp|Greycode for enumerate-ising.cpp
|ising.py|Algorithm 5.3: driver for enumerate-ising.py
|ising-stats|Figure 6.6 - plot data from ising.py
|Makefile|Makefile for enumerate-ising.cpp
|nbr.hpp|Calculate neighbours for enumerate-ising.cpp
|test-gray.cpp|Tests for gray.hpp
|test-nbr.cpp|Tests for nbr.cpp
|tests.cpp|Test harness for enumerate-ising.cpp
5.2||The Ising model - Monte-Carlo algorithm
5.3||Generalized Ising models
6||Entropic Forces
7||Dynamic Monte Carlo Methods
