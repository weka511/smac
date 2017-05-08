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

beta = 2.0
nsteps = 500000
low = levy_harmonic_path(2)
high = low[:]
data = []
for step in range(nsteps):
    # move 1
    if low[0] == high[0]:
        k = random.choice([0, 1])
        low[k] = levy_harmonic_path(1)[0]
        high[k] = low[k]
    else:
        low[0], low[1] = levy_harmonic_path(2)
        high[1] = low[0]
        high[0] = low[1]
    data += low[:]
    # move 2
    weight_old = (rho_harm_1d(low[0], high[0], beta) *
                  rho_harm_1d(low[1], high[1], beta))
    weight_new = (rho_harm_1d(low[0], high[1], beta) *
                  rho_harm_1d(low[1], high[0], beta))
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        high[0], high[1] = high[1], high[0]