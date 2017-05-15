#-*- coding: ISO-8859-1 -*-

import random, math

# To simulate ideal bosons in a 3D harmonic trap, we start with the 
# identity permutation and with random positions sampled from the diagonal
# harmonic density matrix in x, y and z. For each particle move, we sample a 
# random particle, identify its permutation cycle, and sample a new Lévy 
# quantum path for the entire cycle. For each permutation move, 
# we sample 2 random particles like this and this,
# and we attempt an exchange of their permutation partners.
 
'''
This function is used at multiples of the inverse temperature beta,
corresponding to the length of some permutation cycle. 
We use it to resample the positions of the entire cycle.

  Parameters:
    k       Length of some permutation cycle
    beta    Inverse temperature
    
  Returns:
    A vector containg 'k' points in 3 dimensional space
'''
def levy_harmonic_path(k, beta):
    xk = tuple([random.gauss(0.0,
                             1.0 / math.sqrt(2.0 *math.tanh(k * beta / 2.0)))
                for d in range(3)])
    x = [xk]
    for j in range(1, k):
        Upsilon_1 = (1.0 / math.tanh(beta) + 1.0 / math.tanh((k - j) * beta))
        Upsilon_2 = [x[j - 1][d] / math.sinh(beta) + xk[d] /
                     math.sinh((k - j) * beta) for d in range(3)]
        x_mean = [Upsilon_2[d] / Upsilon_1 for d in range(3)]
        sigma = 1.0 / math.sqrt(Upsilon_1)
        xk_next = [random.gauss(x_mean[d], sigma) for d in range(3)]
        x.append(tuple(xk_next))
    return x

'''
This function computes the off-diagonal harmonic density matrix.
We use it to organize the exchange of two elements.
''' 
def rho_harm(x, xp, beta):
    Upsilon_1 = sum((x[d] + xp[d]) ** 2 / 4.0 *
                    math.tanh(beta / 2.0) for d in range(3))
    Upsilon_2 = sum((x[d] - xp[d]) ** 2 / 4.0 /
                    math.tanh(beta / 2.0) for d in range(3))
    return math.exp(- Upsilon_1 - Upsilon_2)

# At high temperature, particles are quite far from each other, and attempts
# to perform a transposition are usually rejected. At lower temperature, beta
# becomes larger and the transpositions are accepted more easily.
# All of a sudden particles clamp together. The transpositions are accepted
# and particles are on long permutation cycles. On long permutation cycles,
# they seem to be at much lower temperature. In fact, they are in the ground
# state. This is the essence of Bose-Einstein condensation. We will treat it
# again in more detail in this week's tutorial. 

N = 128     # Number of particles
T_star = 0.9
beta = 1.0 / (T_star * N ** (1.0 / 3.0))
nsteps = 10000000

# In this very short program, there are no particle indices. The particle
# positions x, y and z, are the "keys" of a "dictionary" called "positions".
# These are the positions at tau=0. The "values" of this dictionary are the
# positions at tau=beta, the positions of the permutation partners. 

# At high temperature, particles are quite far from each other, and attempts
# to perform a transposition are usually rejected. At lower temperature,
# beta becomes larger and the transpositions are accepted more easily. All of
# a sudden particles clamp together. The transpositions are accepted and
# particles are on long permutation cycles. On long permutation cycles,
# they seem to be at much lower temperature. In fact, they are in the ground
# state. This is the essence of Bose-Einstein condensation.

positions = {}
for j in range(N):
    a = levy_harmonic_path(1, beta) # Since k is 1, len(a)=1
    positions[a[0]] = a[0]
    
for step in range(nsteps):
    # Sample a random particle
    boson_a = random.choice(list(positions.keys()))
    
    # Compute the permutation cycle it is on.
    perm_cycle = []

    while True:
        perm_cycle.append(boson_a)
        # Here we sample a random key, and the pop operation outputs the positions
        # of the permutation partner.
        boson_b = positions.pop(boson_a)   
        if boson_b == perm_cycle[0]: break # a
        else: boson_a = boson_b
        
    # Length of permutation cycle. I have done some experiments,  
    # and length reached 19 with 1000000 steps, 27 with 10000000 
    k = len(perm_cycle)

    # Resample the entire path of the cycle from the Levy quantum path. 
    perm_cycle = levy_harmonic_path(k, beta)
    positions[perm_cycle[-1]] = perm_cycle[0]
    for j in range(len(perm_cycle) - 1):
        positions[perm_cycle[j]] = perm_cycle[j + 1]
        
    # And here, we pick two particles and attempt an exchange.      
    a_1 = random.choice(list(positions.keys()))
    b_1 = positions.pop(a_1)
    a_2 = random.choice(list(positions.keys()))
    b_2 = positions.pop(a_2)
    
    # Metropolis
    
    weight_new = rho_harm(a_1, b_2, beta) * rho_harm(a_2, b_1, beta)
    weight_old = rho_harm(a_1, b_1, beta) * rho_harm(a_2, b_2, beta)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        positions[a_1] = b_2
        positions[a_2] = b_1
    else:
        positions[a_1] = b_1
        positions[a_2] = b_2
