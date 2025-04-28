# Statistical Mechanics and Computations

Code from the course: [Statistical Mechanics and Computations](https://www.coursera.org/learn/statistical-mechanics/home/welcome). It includes exercises from the textbook
[Statistical Mechanics: Algorithms and Computations by Werner Krauth](https://global.oup.com/ukhe/product/statistical-mechanics-algorithms-and-computations-9780198515364?cc=ca&lang=en&).

#|Folder|File|Description
--|---------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
&nbsp;|[book](https://github.com/weka511/smac/tree/master)||Exercises and algorithms from the [book](https://global.oup.com/ukhe/product/statistical-mechanics-algorithms-and-computations-9780198515364?cc=ca&lang=en&)
1|||Monte Carlo Algorithms: Direct Sampling & Markov Chain sampling
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_1)|direct_pi.py|Algorithm 1.1 - compute pi using direct sampling
&nbsp;|&nbsp;|direct_pi_multirun.py|Compute pi using multiple runs of direct sampling
&nbsp;|&nbsp;|markov_pi.py|Calculate pi using Markov Chain Monte Carlo
&nbsp;|&nbsp;|markov_pi_multirun.py|Calculate pi using multiple runs of Markov Chain Monte Carlo
&nbsp;|&nbsp;|pebble_basic.py|Demonstrate neighbour table for MCMC-Algorithm 1.6
&nbsp;|&nbsp;|pebble_basic_inhomogeneous.py|Demonstrate neighbour table for MCMC-Algorithm 1.6 with inhomogeneous probabilities
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_1)|pebble_basic.py|Move pebble using neighbour Table 1.3
&nbsp;|&nbsp;|pebble_basic_movie.py|Move pebble using neighbour Table 1.3
&nbsp;|&nbsp;|pebble_basic_multirun.py|Move pebble using neighbour Table 1.3
&nbsp;|&nbsp;|pebble_dual_eigen.py|Two games: Illustrate conversion of reducible matrix to irreducible+aperiodic to make motion ergodic
&nbsp;|&nbsp;|pebble_dual_movie.py|'''Two games: Illustrate conversion of reducible matrix to irreducible+aperiodic to make motion  ergodic'''
&nbsp;|&nbsp;|pebble_multirun_all_histogram.py|Show probability for reaching other cells after 0, 1, 2, ... moves
&nbsp;|&nbsp;|pebble_multirun_histogram.py|Show probability for reaching other cells after 0, 1, 2, ... moves
&nbsp;|&nbsp;|pebble_recurrent_eigen.py|Dual pebble: make aperiodic
&nbsp;|&nbsp;|pebble_recurrent_movie.py|Dual pebble: make aperiodic
&nbsp;|&nbsp;|pebble_transfer.py|Model Monte Carlo simulation as a transfer matrix, illustrating speed of convergence
&nbsp;|&nbsp;|pebble_transfer_eigen.py|Eigenvalues and eigenvectors of transfer matrix, illustrating speed of convergence
&nbsp;|&nbsp;|pebble_transfer_sub.py|Model Monte Carlo simulation as a transfer matrix; subtract equilibrium value to show speed of convergence
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_1)|exerciseB.py|Shows that the error of markov_pi follows the law: const / sqrt(N_trials)for large N_trials. The constant is larger (sometimes much larger) than 1.642 and it depends on the stepsize delta.
&nbsp;|&nbsp;|exerciseC.py|Bunching method: compute the error in markov_pi.py from a single run and without knowing the mathematical value of pi.
&nbsp;|&nbsp;|exerciseC1.py|Bunching method: compute the error in markov_pi.py from a single run and without knowing the mathematical value of pi
&nbsp;|&nbsp;|exerciseC3.py|Bunching method: compute the error in markov_pi.py from a single run and without knowing the mathematical value of pi
2|||Hard Disks: from classical mechanics to statistical mechancs
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_2)|direct_disks_box.py|Direct sampling of disks in box, tabula rasa
&nbsp;|&nbsp;|direct_disks_box_a1.py|Direct sampling of disks in box, tabula rasa: investigate success rate
&nbsp;|&nbsp;|direct_disks_box_movie.py|Direct sampling of disks in box, tabula rasa, plotted as movie
&nbsp;|&nbsp;|direct_disks_box_multirun.py|Direct sampling of disks in box, tabula rasa, multiple runs
&nbsp;|&nbsp;|direct_disks_box_multirun_b1.py|Generate histogram of x positions by direct sampling of disks in box, tabula rasa
&nbsp;|&nbsp;|event_disks_box.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box
&nbsp;|&nbsp;|event_disks_box_a3.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box. Repeat
&nbsp;|&nbsp;|event_disks_box_b3.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box. Repeat and generate histogram
&nbsp;|&nbsp;|event_disks_box_movie.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box. Repeat. Plotted as movie
&nbsp;|&nbsp;|markov_disks_box.py|Algorithm 2.2: generating a hard disk configuration from another one using a Markov chain
&nbsp;|&nbsp;|markov_disks_box_a2.py|Algorithm 2.2: generating a hard disk configuration from another one using a Markov chain
&nbsp;|&nbsp;|markov_disks_box_movie.py|Algorithm 2.2: generating a hard disk configuration from another one using a Markov chain
&nbsp;|&nbsp;|markov_disks_box_multirun_b2.py|Algorithm 2.2: generating a hard disk configuration from another one using a Markov chain
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_2)|direct_discrete.py|Create configuration of rods using tabula rasa to give equiprobable distribution
&nbsp;|&nbsp;|direct_disks_any.py|Compute acceptance probability for hard disks as a function of density
&nbsp;|&nbsp;|direct_disks_box.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box
&nbsp;|&nbsp;|direct_disks_box_slow.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box. Build full set of disks, including invalid, then cull.
&nbsp;|&nbsp;|direct_disks_multirun.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box with periodic boundary conditions: multiple runs to collects stats
&nbsp;|&nbsp;|direct_disks_multirun_movie.py|Algorithm 2.1: event-driven molecular dynamics for hard disks in a box with periodic boundary conditions: multiple runs to collects stats
&nbsp;|&nbsp;|random_sequential_discrete.py|Create configuration of rods without tabula rasa: does not give equiprobable distribution
&nbsp;|&nbsp;|random_sequential_discrete_movie.py|Create configuration of rods without tabula rasa: does not give equiprobable distribution
3|||Entropic Interactions and Phase Transitions
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_3)|direct_pins.py|Algorithm 6.1: direct sampling
&nbsp;|&nbsp;|direct_pins_improved.py|Algorithm 6.1: direct sampling
&nbsp;|&nbsp;|direct_pins_movie.py|Algorithm 6.1:  direct sampling
&nbsp;|&nbsp;|direct_pins_noreject.py|Algorithm 6.2: rejection free sampling
&nbsp;|&nbsp;|direct_pins_noreject_movie.py|Algorithm 6.2: rejection free sampling
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_3)|direct_pins.py|Algorithm 6.1: direct sampling
&nbsp;|&nbsp;|direct_pins_density.py|
&nbsp;|&nbsp;|direct_pins_movie.py|
&nbsp;|&nbsp;|direct_pins_noreject.py|
&nbsp;|&nbsp;|direct_pins_noreject_movie.py|
&nbsp;|&nbsp;|direct_pins_noreject_periodic.py|
&nbsp;|&nbsp;|direct_pins_noreject_periodic_pair.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_3)|my_markov_disks.py|
&nbsp;|&nbsp;|preparation1.py|
&nbsp;|&nbsp;|preparation2.py|
4|||Sampling and Integration
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_4)|direct_sphere_3d.py|
&nbsp;|&nbsp;|direct_sphere_3d_movie.py|
&nbsp;|&nbsp;|direct_surface.py|
&nbsp;|&nbsp;|direct_surface_3d.py|
&nbsp;|&nbsp;|direct_surface_3d_movie.py|
&nbsp;|&nbsp;|gauss_2d.py|
&nbsp;|&nbsp;|gauss_2d_movie.py|
&nbsp;|&nbsp;|gauss_3d.py|
&nbsp;|&nbsp;|gauss_3d_movie.py|
&nbsp;|&nbsp;|gauss_test.py|
&nbsp;|&nbsp;|gauss_test_movie.py|
&nbsp;|&nbsp;|naive_gauss.py|
&nbsp;|&nbsp;|naive_gauss_movie.py|
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_4)|basic_use_random.py|
&nbsp;|&nbsp;|gamma_transform.py|
&nbsp;|&nbsp;|gauss_transform.py|
&nbsp;|&nbsp;|markov_gauss.py|
&nbsp;|&nbsp;|markov_gauss_movie.py|
&nbsp;|&nbsp;|markov_inv_sqrt.py|
&nbsp;|&nbsp;|markov_inv_sqrt_movie.py|
&nbsp;|&nbsp;|naive_ran.py|
&nbsp;|&nbsp;|reject_direct_gauss_cut.py|
&nbsp;|&nbsp;|reject_inv_sqrt_cut.py|
&nbsp;|&nbsp;|tower_discrete.py|
&nbsp;|&nbsp;|walker_test.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_4)|data-bunch.py|
&nbsp;|&nbsp;|markov_hypersphere.py|
&nbsp;|&nbsp;|markov_hypersphere_C2.py|
&nbsp;|&nbsp;|markov_sphere_3D.py|
&nbsp;|&nbsp;|markov_sphere_4D.py|
5|||Quantum Statistical Mechancs 1/3: Density Matrices and Path Integrals
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_5)|harmonic_wavefunction.py|
&nbsp;|&nbsp;|harmonic_wavefunction_check.py|
&nbsp;|&nbsp;|harmonic_wavefunction_check_movie.py|
&nbsp;|&nbsp;|harmonic_wavefunction_movie.py|
&nbsp;|&nbsp;|matrix_square_harmonic.py|
&nbsp;|&nbsp;|matrix_square_harmonic_movie.py|
&nbsp;|&nbsp;|naive_harmonic_path.py|
&nbsp;|&nbsp;|naive_harmonic_path_movie.py|
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_5)|free_periodic_complex_exp.py|
&nbsp;|&nbsp;|free_periodic_complex_exp_movie.py|
&nbsp;|&nbsp;|free_periodic_sine_cosine.py|
&nbsp;|&nbsp;|free_periodic_sine_cosine_movie.py|
&nbsp;|&nbsp;|harmonic_trotter_movie.py|
&nbsp;|&nbsp;|quantum_time_evolution.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_5)|a2.py|
&nbsp;|&nbsp;|markov_gauss_a1.py|
&nbsp;|&nbsp;|markov_gauss_movie_a1.py|
&nbsp;|&nbsp;|matrix_square_anharmonic_c1.py|
&nbsp;|&nbsp;|matrix_square_anharmonic_c3.py|
&nbsp;|&nbsp;|matrix_square_harmonic_b1.py|
&nbsp;|&nbsp;|path_Integral_b2.py|
&nbsp;|&nbsp;|path_Integral_c2.py|
6|||Quantum Statistical Mechancs 2/3: Lévy Quantum Paths
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_6)|continuous_random_walk.py|Construct path using a simple random walk (endpoint is not held fixed)
&nbsp;|&nbsp;|levy_free_path.py|Simple simplementation of Levy Free Path Algorithm
&nbsp;|&nbsp;|levy_harmonic_path.py||Simple Lévy path
&nbsp;|&nbsp;|levy_harmonic_path_3D.py|Lévy flight in 3D
&nbsp;|&nbsp;|levy_harmonic_path_movie.py|
&nbsp;|&nbsp;|naive_harmonic_path.py|Construct path using direct sanpling (inefficient)
&nbsp;|&nbsp;|naive_path_slice.py|
&nbsp;|&nbsp;|naive_path_slice_movie.py|
&nbsp;|&nbsp;|trivial_free_path.py|Generate a random walk, then pull back as described in Lecture 6, 20:12. Compare result with Lévy free path
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_6)|naive_boson_trap.py|Enumerate energies in a simple harmonic trap
&nbsp;|&nbsp;|naive_single_particle.py|Enumerate states for Bosons, i.e. indistinguisgable particles
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_6)|a1.py|
&nbsp;|&nbsp;|a2.py|
&nbsp;|&nbsp;|a3.py|
&nbsp;|&nbsp;|b1.py|
&nbsp;|&nbsp;|b2.py|
&nbsp;|&nbsp;|b3.py|
&nbsp;|&nbsp;|c1.py|
&nbsp;|&nbsp;|c2.py|
7|||Quantum Statistical Mechancs 3/3: Bose-Einstein Condensation
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_7)|markov_harmonic_bosons.py|
&nbsp;|&nbsp;|markov_harmonic_bosons_movie.py|
&nbsp;|&nbsp;|permutation_sample.py|
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_7)|canonic_harmonic_recursion.py|
&nbsp;|&nbsp;|canonic_harmonic_recursion_movie.py|
&nbsp;|&nbsp;|direct_harmonic_bosons.py|
&nbsp;|&nbsp;|markov_harmonic_bosons.py|
&nbsp;|&nbsp;|permutation_sample.py|
&nbsp;|&nbsp;|permutation_sample_cycle.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_7)|a1.py|
&nbsp;|&nbsp;|a2.py|
&nbsp;|&nbsp;|a2a.py|
&nbsp;|&nbsp;|a3.py|
&nbsp;|&nbsp;|b1.py|
&nbsp;|&nbsp;|b2.py|
&nbsp;|&nbsp;|c1.py|
8|||Ising Model: Enumerations and Monte-Carlo Algorithms
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_8)|cluster_ising.py|
&nbsp;|&nbsp;|cluster_ising_movie.py|
&nbsp;|&nbsp;|energy_ising.py|5-1 Compute the energy of an Ising configuration
&nbsp;|&nbsp;|enumerate_ising.py|
&nbsp;|&nbsp;|enumerate_ising_mod.py|
&nbsp;|&nbsp;|enumerate_ising_movie.py|
&nbsp;|&nbsp;|gray.py|
&nbsp;|&nbsp;|markov_ising.py|
&nbsp;|&nbsp;|markov_ising_movie.py|
&nbsp;|&nbsp;|thermo_ising.py|
&nbsp;|&nbsp;|thermo_ising_movie.py|
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_8)|heatbath_ising.py|
&nbsp;|&nbsp;|heatbath_ising_random_map.py|
&nbsp;|&nbsp;|heatbath_ising_random_map_movie.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_8)|A1.py|
&nbsp;|&nbsp;|A2.py|
&nbsp;|&nbsp;|B1.py|
&nbsp;|&nbsp;|B2.py|
&nbsp;|&nbsp;|C1.py|
&nbsp;|&nbsp;|C2.py|
9|||Dynamic Monte Carlo, Simulated Annealing
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_9)|dynamic_ising.py|
&nbsp;|&nbsp;|dynamic_ising_patch.py|
&nbsp;|&nbsp;|fast_spin_dynamics.py|
&nbsp;|&nbsp;|fast_throw.py|
&nbsp;|&nbsp;|naive_spin_dynamics.py|
&nbsp;|&nbsp;|naive_spin_dynamics_movie.py|
&nbsp;|&nbsp;|naive_throw.py|
&nbsp;|[Tutorial](https://github.com/weka511/smac/tree/master/tutorial_9)|direct_sphere_disks.py|
&nbsp;|&nbsp;|direct_sphere_disks_any.py|
&nbsp;|&nbsp;|direct_sphere_disks_any_movie.py|
&nbsp;|&nbsp;|direct_sphere_disks_movie.py|
&nbsp;|&nbsp;|example_pylab_visualization.py|
&nbsp;|&nbsp;|markov_sphere_disks.py|
&nbsp;|&nbsp;|resize_disks.py|
&nbsp;|&nbsp;|simulated_annealing.py|
&nbsp;|&nbsp;|simulated_annealing_movie.py|
&nbsp;|[Homework](https://github.com/weka511/smac/tree/master/homework_9)|A1.py|
&nbsp;|&nbsp;|A2.py|
&nbsp;|&nbsp;|B1.py|
&nbsp;|&nbsp;|C1.py|
&nbsp;|&nbsp;|C2.py|
10|||The Alpha and Omega of Monte Carlo
&nbsp;|[Lecture](https://github.com/weka511/smac/tree/master/lecture_10)|direct_gamma.py|Integral of x**gamma, illustrating need for importance sampling
&nbsp;|&nbsp;|direct_gamma_average.py|Integral of x**gamma, illustrating need for importance sampling
&nbsp;|&nbsp;|direct_gamma_average_movie.py|Histogram of Integral of x**gamma, illustrating need for importance sampling
&nbsp;|&nbsp;|direct_gamma_average_rescaled.py|
&nbsp;|&nbsp;|direct_gamma_average_rescaled_movie.py|Integral of x**gamma: rescale, plot histograms, and compare with Lévy distribution
&nbsp;|&nbsp;|direct_gamma_running.py|
&nbsp;|&nbsp;|direct_gamma_running_movie.py|
&nbsp;|&nbsp;|direct_needle.py|Buffon's experiment (with cheat)
&nbsp;|&nbsp;|direct_needle_patch.py|Buffon's experiment
-|utils|backends.py|List graphics backends
&nbsp;|&nbsp;|walker.py|Used to create README.MD from file tree
