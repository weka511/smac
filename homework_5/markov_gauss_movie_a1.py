# A1 (continued) The ground-state wave function of a quantum particle in a
# harmonic trap is equal to psi_0(x) = (1/ pi^(1/4)) exp( - x^2 / 2).
# In the limit T->0, the probability pi(x) of a quantum particle to be at
# x is equal to the square of the ground state wave function, psi_0(x))^2. 
# Familiarize yourself with the Markov-chain Monte Carlo algorithm for a 
# particle in a Gaussian potential, using the Metropolis algorithm: namely
# the program markov_gauss.py (this program was discussed in last week's 
# Tutorial, Tutorial 4). Modify this Metropolis algorithm so that it samples
# positions x according to the probability pi(x) = psi_0(x)^2. You should use
# a function for the square of the wave function (def psi_0_sq(x): ...). 
# Furthermore, the program should output the normed histogram of the particle
# positions (use pylab.hist() with "normed=True") and
# compare to the function psi_0^2(x). 
import random, math, pylab

# formular obtained by squaring "psi" as defined in homework
def psi_0_sq(x):
    return math.pi**-0.5*math.exp(-x*x)

x = 0.0
delta = 0.5
data = []
for k in range(5000000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  psi_0_sq(x_new)/psi_0_sq(x): 
        x = x_new 
    data.append(x)

pylab.hist(data, 100, normed = 'True',label='Histogram')
x = [a / 10.0 for a in range(-50, 51)]
y = [psi_0_sq(a) for a in x]
pylab.plot(x, y, c='red', linewidth=2.0,label='$\psi_{0}(x)^{2}$')
pylab.title('Theoretical Gaussian distribution $\psi_{0}(x)^{2}$ and \
    \nnormalized histogram for '+str(len(data))+' samples', fontsize = 18)
pylab.xlabel('$x$', fontsize = 30)
pylab.ylabel('$\psi_{0}(x)^{2}$', fontsize = 20)
pylab.legend(loc='upper right')
pylab.savefig('plot_markov_gauss.png')
pylab.show()
