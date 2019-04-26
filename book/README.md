# Statistical Mechanics and Computations - Book

Code exercises from the textbook
[*Statistical Mechanics: Algorithms and Computations*](http://blancopeck.net/Statistics.pdf) by *Werner Krauth*.

|#|File|Problem/Algorithm/Description|
|-----|--------------|---------------------------------------------------------------------------------------|
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
||permutation.py|1.9 Sample permutations using Alg. 1.11 and verify that it generate all 120 permutaions of 5 elements equally often|
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
|4|| Bosons|
|5|| Order and disorder in spin systems|
|5.1||The Ising model - exact computations|
||gray.py|Algorithm 5.2: Gray code for spine {1,...N}.|
||enumerate-ising.py|Algorithm 5.3: single flip enumeration for the Ising model.|
|5.2||The Ising model - Monte-C|arlo algorithm|
|5.3||Generalized Ising models| 
|6||Entropic Forces|
|7||Dynamic Monte Carlo Methods|
