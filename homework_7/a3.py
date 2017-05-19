import math, random, pylab

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)

def prob_r_distinguishable(r, beta):
    sigma = math.sqrt(2.0) / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return (math.sqrt(2.0 / math.pi) / sigma) * math.exp(- r ** 2 / 2.0 / sigma ** 2)

beta = 0.1
nsteps = 1000000
low_1, low_2 = levy_harmonic_path(2)
x = {low_1:low_1, low_2:low_2}
data = []
distances = []
for step in range(nsteps):
    # move 1
    a = random.choice(list(x.keys()))
    if a == x[a]:
        dummy = x.pop(a)
        a_new = levy_harmonic_path(1)[0]
        x[a_new] = a_new
    else:
        a_new, b_new = levy_harmonic_path(2)
        x = {a_new:b_new, b_new:a_new}
    # move 2
    (low1, high1), (low2, high2) = x.items()
    weight_old = rho_harm_1d(low1, high1, beta) * rho_harm_1d(low2, high2, beta)
    weight_new = rho_harm_1d(low1, high2, beta) * rho_harm_1d(low2, high1, beta)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        x = {low1:high2, low2:high1}
    distances.append(abs(list(x.keys())[1] - list(x.keys())[0]))
    
_,rs,_=pylab.hist(distances,normed=True,bins=120,label='Empirical')
pylab.plot(rs,
           [prob_r_distinguishable(r, beta) for r in rs],
           color='r',
           label='Theoretical')
pylab.xlabel('$r$')
pylab.ylabel('$Probability$')
pylab.title(r'$A3:\ Distinguishable\ particles\ in\ a\ trap.\ \beta={0},\ nsteps={1:,}$'.format(beta,nsteps))
pylab.legend()
pylab.savefig('A3.png')

# In the histogram above, I observe that the general shape is similar to the 
# analytic expression, up to a pronounced peak at short distance,
#in which the histogram height doubles.

#This effect that we see at play in its simplest realization (two particles 
# in one dimension) is called boson bunching, and corresponds to the doubling
# of the statistical weight of configurations in which the two particles 
# are at a short distance (approximately, smaller than sqrt(2*pi*beta)).
# It is a pure consequence of bosonic permutations, which takes place at any temperature.


# NB: The real explanation is that for small distances (distance smaller 
# than the de Broglie wavelength), the weight of the || configuration 
# (two cycles of length 1) is the same as the weight of the X configuration 
#(cycle of length 2), whereas at large distance only the || term contributes.
# This also explains why the density is twice the classical density.
# 