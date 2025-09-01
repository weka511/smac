# Exercises and algorithms from the Book

#|File|Problem/Algorithm/Description
-----|--------------|---------------------------------------------------------------------------------------
-|template.py|Template for python programs
1.1.1|exercise_1_1.py|Implement Algorithm 1.1. Plot error and investigate relationship with N.
-|exercise_1_3.py|Problems 1.1 and 1.3
-|smacfiletoken.py|Allow program to be stopped by creating kill token
1.1.2|exercise_1_2.py|Implement Algorithm 1.2. Plot error and rejection rate.
1.1.3|direct-needle.py|Exercise 1.6: implement Alg 1.4 direct needle and Alg 1.5 direct-needle(patch)
1.1.4|nbr.py|Table 1.3 Neighbour table
-|exercise_1_4.py|Exercise 1.4: implement algorithm 1.6, markov-discrete-pebble, using a subroutine for the numbering scheme and neighbour table. Check that, during long runs, all sites are visited equally often.
-|exercise_1_5.py|Exercise 1.5: For the 3x3 pebble game, find a rejection-free local Monte Carlo algorithm--WIP
-|exercise_1_6.py|Exercise 1.6: implement Alg 1.4 direct needle and Alg 1.5 direct-needle(patch).
1.2|-|Basic Sampling
1.2.2|permutation.py|Exercise1.9 Sample permutations using Alg. 1.11 and verify that it generate all 120 permutations of 5 elements equally often
-|permutation-histogram.py
-|ran-perm.py|Exercise 1.9 (a) Sample permutations using algoritm 1.11 and check that this algorithm generates all 120 permutations of 5 elements equally often.  (b) Determine the cycle representation of each permutation that is generated.
-|ran-perm-alt.py|Exercise 1.9 (c) Alternative algorithm
1.2.3|exercise_1_16.py|Exercise 1.16. Compare sampling efficiencies of Algorithms 1.13 (reject-finite) and 1.14 (tower-sampling)
1.2.4|exercise_1_17.py|Exercise 1-17: Use a sample transformation to derive random numbers distributed as 0.5 sin(phi)
1.2.5|exercise_1_12.py|Exercise 1.12. Implement both naive Algorithm 1.17 (naive Gauss) and 1.18 (Box Muller). For what value of K can you still detect statistially significant differences between the two algorithms?
-|exercise_1_12a.py|Exercise 1.12 - plot results of KS test.
-|exercise_1_13.py|Exercise 1-13: generate uniformly distributed vectors inside sphere, then augment with an additional component in the range (-1,+1), and reject if length exceeds 1. Use to estimate ratios of volumes.
-|exercise_1_14.py|Exercise 1.14. Sample random vectors on the surface of a sphere using Algorithm 1.22 and plot x[0]**2 + y[0]**2
-|exercise_1_15.py|Exercise 1.15. Generate 3 dimensional orthonormal coordinate systems with axes randomly oriented in space, using Algorithm 1.22. Test by computing average scalar products for pairs of random coordinate systems.
-|chaosbook_2_11.py|Monte Carlo simulation of Exercise 2.11 of Chaosbook: in higher dimensions, any two vectors are nearly orthogonal
1.3.1|exercise_1_18.py|Exercise 1.18 and Algorithm 1.25 from Krauth
1.3.5|exercise_1_20.py|Exercise 1.20. Implemement algorithm 1.28 (data-bunch). First part: test with a single, very long, simulation of Alg 1.2, markov-pi, with throwing ranges of 0.03, 0.1, 0.3.
-|exercise_1_20a.py|Exercise 1.20. Implemement algorithm 1.28 (data-bunch). Second part: test it also with the output of Alg 1.6, markov-discrete-pebble.py.
1.4.2|exercise_1_22.py|1.22 Importance sampling:Implement Algorithm 1.29, subtract mean value for each sample, and generate histograms of the average of N samples  and the rescaled averages.
-|direct-gamma-zeta.py|Implement Algorithm 1.30: using importance sampling to compute the gamma integral.
1.4.3|exercise_1_21.py|Exercise 1.21 Determine the mean value of x**(gamma-zeta) in a simple implementation of Algorithm 1.31 (markov-zeta)
-|markov-zeta.py|Algorithm 1.31 Markov-chain Monto Carlo algorithm for a point x on the interval [0,1] with probability proportional to x**zeta. Algorithm 1.31 Markov-chain Monto Carlo algorithm for a point x on the interval [0,1]
    with probability proportional to x**zeta. The code illustrates both an integrable and a non-integrable singularity.
1.4.4|levy-convolution.py|Algorithm 1.32 Levy convolution: distribution is convoluted with itself, after being padded as in Figure 1.47.
2.1.4|exercise_2_4.py|Exercise 2-4: Sinai's system of two large sphere in a box. Show histogram of positions.
2.2.1|pair-time.py|Exercise 2.1: Implement algorithm 2.2 (pair-time) and incorporate it into a test program  generating 2 random positions with ans(delta_x) > 2 sigma. Propagate both disks up to t_pair if finite and verify that they touch; otherwise verify that delta_x.delta_v = 0.
-|exercise_2_2.py|Exercise 2.2/Algorithm 2.3 (pair collision). Verify that energy and momentum are both conserved in a collision.
-|exercise_2_3.py|Exercise 2.3. Exercise 2.3. Implement algorithm 2.1 (event disks) for disks in a square box without periodic boundary conditions. Start from a legal configuration, allowing restart as discussed in exercise 1.3. Sample at regular intervals, and generate histograms of position and velocity.
-|md|Algorithm 2.3 Pair collision
-|md.py|Algorithm 2.3 Pair collision
-|md-viz.py|Visualize data generated by md.py
-|md-plot.py|Visualize output from md.cpp. Plot distribution of distances from wall, and compare energy histogram with Bolzmann distribution.
-|geometry.py|This class models the space in which spheres move. It supports the use of both periodic and bounded boundary conditions in Exercises 2.6-2.8
-|exercise_2_6.py|Exercise 2.6: directly sample the positions of 4 disks in a square box without periodic boundary conditions, for different covering densities
-|exercise_2_7.py|Exercise 2.7: directly sample the positions of 4 disks in a square box with periodic boundary conditions. Compare with histograms from Algorithms 2.1, 2.7, and 2.9
2.2.2|exercise_2_8.py|Exercise 2.8: Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC
-|markov-disks.py|Exercise 2.8 and Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC.
-|exercise_2_9.py|Exercise 2.9: Implement Algorithm 2.8, direct-disks-any, in order to determine the acceptance rate of algorithm 2.7, direct-disks.
2.2.3|exercise_2_10.py|Exercise 2.10: Algorithm 2.9. Generating a hard disk configuration from an earlier valid configuration using MCMC. Compare with algorithm  2.7 - direct-disks.
2.3.3|exercise_2_12.py|Exercise 2.12: Sample the gamma distribution using the naive algorithm contained in Algorithm 2.13. Likewise implement Algorithm 2.15, gamma-cut. (WIP)
3.1|harmonic_wavefunction.py|Exercise 3.1: verify orthonormality of the solutions to Schroedinger's equation for Simple Harmonic Oscillator
-|harmonic_density.py|Exercise 3.2: determine density matrix
3.2|matrix-square.py|Exercise 3.4: implement Alg 3.3, matrix-square
-|matrix-square-check.py|Exercise 3.4: check results of matrix squaring against exact solution.
-|poeschl-teller.py|Exercise 3.5: plot Poeschl-Teller potential and investigate density matrix and partition function
3.3||The Feynman path integral
3.4||Pair density matrices
3.5||Geometry of Paths
4|| Bosons
5.1|energy_ising.py|5.1: Compute energy of a simple Ising configuration
-|edge_ising.py|Algorithm 5.5 edge-ising. Gray code enumeration of the loop configurations in Figure 5.8
-|enumerate_ising.py|Algorithm 5.3: single flip enumeration for the Ising model.
-|exercise_5_2.py|Exercise 5-2. Generate configurations from binary representation (incomplete)
-|exercise_5_4.py|Exercise 5-4: Implement thermo-ising for mean energ and cV
-|exercise_5_6.py|Exercise 5-6.Plot magnetization as a function of temperature
-|exercise_5_7.py|Exercise 5.7. Compute Partition function using loop configurations as described in 5.1.3
-|ising.py|Shared code for Ising model: Algorithm 5.2, Gray code for spins; generate neighbours of a spin; calculate energy for a configuration.
-|ising_enum.py|Algorithm 5.3: Single spin-slip enumeration for Ising model
-|ising-stats.py|Figure 6.6 - plot data from ising.py
-|ising|C++ implementations of Algorithm 5.3 (single flip enumeration for the Ising model) and 5.7 (MCMC)
5.2|cluster_ising.py|Algorithm 5-9: cluster ising
-|exercise_5_10a.py|Exercise 5.10: Implement Local Metropolis algorithm and test it against the specific heat capacity.
-|exercise_5_10b.py|Exercise 5.10: Plot M against T
-|exercise_5_11.py|Exercise 5-11/Algorithm 5-9: cluster ising
-|ising_db.py|Exercise 5-11: a library to facilite reuseing data from previous runs
-|thermo_ising.py|Exercise 5-11: calculate thermodynamic quantities
-|thermo_db.py|Exercise 5-11: calculate thermodynamic quantities from database
-|markov_ising.py|Algorithm 5.7: Local Metropolis algorithm for the Ising model
-|thermo.py|Exercise 5-11: calculate thermodynamic quantities
-|bench42.sh|Benchmark effect of [Issue #42](https://github.com/weka511/smac/issues/42)
-|cpp_mcmc.py|Script to plot C++ MCMC outpu
5.3||Generalized Ising models
6||Entropic Forces
7||Dynamic Monte Carlo Methods

File|Problem/Algorithm/Description
--------------|---------------------------------------------------------------------------------------
preferential.py|Simulate preferential attachment
