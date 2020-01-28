# Statistical Mechanics and Computations - Book

Code exercises from the textbook
[*Statistical Mechanics: Algorithms and Computations*](http://blancopeck.net/Statistics.pdf) by [*Werner Krauth*](http://www.lps.ens.fr/~krauth/index.php/Main_Page).

|#|File|Problem/Algorithm/Description|
|-----|--------------|---------------------------------------------------------------------------------------|
||template.py|Template for python programs|
|1||Monte Carlo Methods|
||smac.c|Useful functions: BoxMuller, CircleThrowing, and SphereGenerator|
|1.1||Popular Games in Monaco|
||direct-plot.py|Implement Algorithm 1.1. Plot error and investigate relationship with N.|
|| markov-pi.py|Implement Algorithm 1.2. Plot error and rejection rate.|
||direct.py|1.3 Store state in file|
||smacfiletoken.py||
||markov-discrete-pebble.py| 1.4 Use table|
||large-markov.pi||
||transfer.m|1.8 Eigenvalues of transfer matrix|
||sphere-test.py|1.13 Vectors within Uniform sphere|
|1.2||Basic Sampling|
||permutation.py|1.9 Sample permutations using Alg. 1.11 and verify that it generate all 120 permutations of 5 elements equally often|
||permutation-histogram.py|
||naivegauss.py|1.12 Gauss|
||boxmuller.py||
|1.3||Statistical data analysis|
||binomialconvolution.py|1.18 Binomial Convolution|
|1.4||Computing|
|1.4.2||Importance Sampling|
||direct-gamma.py|1.22 Importance sampling:Implement Algorithm 1.29, subtract mean value for each sample, and generate histograms of the average of N samples  and the rescaled averages.
||direct-gamma-zeta.py||
||markov-zeta.py|Algorithm 1.31, use of Markov Chain to detect non-integrable singularity.|
|1.4.4||Stable Distribution|
||levy-convolution.py|Algorithm 1.32|
| 2|| Hard Disks and Spheres|
|2.2||Boltzmann's Statistical Mechanics|
||directDisksAny.py||
|3||Density Matrices and Path Integrals|
|3.1||Density Matrices|
||harmonic_wavefunction.py|Exercise 3.1: verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator|
||harmonic_density.py|Exercise 3.2: determine density matrix|
|3.2||Matrix Squaring|
||matrix-square.py|Exercise 3.4: implement Alg 3.3, matrix-square|
||matrix-square-check.py|Exercise 3.4: check results of matrix squaring against exact solution.|
||poeschl-teller.py|Exercise 3.5: plot Poeschl-Teller potential and investigate density matrix and partition function|
|3.3||The Feynman path integral|
|3.4||Pair density matrices|
|3.5||Geometry of Paths|
|4|| Bosons|
|5|| Order and disorder in spin systems|
|5.1||The Ising model - exact computations|
||catch.hpp|Support for Test harness for enumerate-ising.cpp|
||gray.py|Algorithm 5.2: Gray code for spine {1,...N}.|
||enumerate-ising.py|Algorithm 5.3: single flip enumeration for the Ising model.|
||enumerate-ising.cpp|Algorithm 5.3: single flip enumeration for the Ising model.|
||enumerate-ising.hpp|Algorithm 5.3: single flip enumeration for the Ising model.|
||gray.hpp|Greycode for enumerate-ising.cpp|
||ising.py|Algorithm 5.3: driver for enumerate-ising.py|
||ising-stats|Figure 6.6 - plot data from ising.py|
||Makefile|Makefile for enumerate-ising.cpp|
||nbr.hpp|Calculate neighbours for enumerate-ising.cpp|
||test-gray.cpp|Tests for gray.hpp|
||test-nbr.cpp|Tests for nbr.cpp|
||tests.cpp|Test harness for enumerate-ising.cpp|
|5.2||The Ising model - Monte-Carlo algorithm|
|5.3||Generalized Ising models| 
|6||Entropic Forces|
|7||Dynamic Monte Carlo Methods|
