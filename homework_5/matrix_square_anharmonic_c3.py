import math, numpy

def V(x,cubic, quartic):
    return x*x* (0.5 + x*(cubic+x*quartic))

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

def rho_anharmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * ( V(x,cubic, quartic) +  V(xp,cubic, quartic))) \
                         for x in grid] for xp in grid])

# Theoretical probability density for Harmonc
# I've kept this, as it shows the diffeence between harmon and anharmonic
def pi_quant(x):
    return math.sqrt( math.tanh(beta/2) / math.pi)* math.exp( - x*x * math.tanh(beta/2) )

def Energy_pert(n, cubic, quartic):
    return n + 0.5 - 15.0 / 4.0 * cubic **2 * (n ** 2 + n + 11.0 / 30.0) \
         + 3.0 / 2.0 * quartic * (n ** 2 + n + 1.0 / 2.0)

def Z_pert(cubic, quartic, beta, n_max):
    return sum(math.exp(-beta * Energy_pert(n, cubic, quartic)) for n in range(n_max + 1))
    

if __name__=='__main__':
    for quartic in [0.001,0.01,0.1,0.2,0.3,0.4,0.5]:
        cubic= - quartic
        x_max = 5.0
        nx = 100
        dx = 2.0 * x_max / (nx - 1)
        x = [i * dx for i in range(-(nx - 1) // 2, nx // 2 + 1)]
        beta_tmp = 2.0 ** (-5)                   # initial value of beta (power of 2)
        beta     = 2.0 ** 1                      # actual value of beta (power of 2)
        rho = rho_anharmonic_trotter(x, beta_tmp)  # density matrix at initial beta
        while beta_tmp < beta:
            rho = numpy.dot(rho, rho)
            rho *= dx
            beta_tmp *= 2.0
            #print ('beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp))
        
        Z = sum(rho[j, j] for j in range(nx + 1)) * dx
        try:
            Zp=Z_pert(cubic, quartic, beta, nx)
            print ('{0}\t{1}\t{2}\t{3:.1f}%'.format(quartic,Z,Zp,100*abs(Z-Zp)/Z))
        except OverflowError:
            print('{0} ***'.format(quartic))
