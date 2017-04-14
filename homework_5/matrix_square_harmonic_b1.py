import math, numpy, pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

# Theoretical probability density

def pi_quant(x):
    return math.sqrt( math.tanh(beta/2) / math.pi)* math.exp( - x*x * math.tanh(beta/2) )

if __name__=='__main__':
    x_max = 5.0
    nx = 100
    dx = 2.0 * x_max / (nx - 1)
    x = [i * dx for i in range(-(nx - 1) // 2, nx // 2 + 1)]
    beta_tmp = 2.0 ** (-5)                   # initial value of beta (power of 2)
    beta     = 2.0 ** 2                      # actual value of beta (power of 2)
    rho = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        beta_tmp *= 2.0
        print ('beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp))
    
    Z = sum(rho[j, j] for j in range(nx + 1)) * dx
    pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]
    with open('data_harm_matrixsquaring_beta_{0}.dat'.format(beta), 'w') as f:
        for j in range(nx + 1):
            f.write('{0} {1}\n'.format(x[j], rho[j, j] / Z))
    
    psi_from_matrix_squaring=[rho[j, j] / Z for j in range(nx + 1) ] 
    pi_quants=[pi_quant(a) for a in x]    
    pylab.plot(x,psi_from_matrix_squaring,marker='o',label='Matrix Squaring')
    pylab.plot(x,pi_quants,c='r',label='Theoretical')
    pylab.suptitle(r'$Distribution for \ \beta = {0}$'.format(beta), fontsize = 20)
    pylab.title('NB: agreement between curves is so good that red line overwrites blue', fontsize = 12)
    pylab.xlabel('$x$', fontsize = 30)
    pylab.ylabel('$Probability$', fontsize = 20)
    pylab.legend(loc='upper left',framealpha=0.5)
    pylab.savefig('plot_matrix_squaring_beta_{0}.png'.format(beta))

pylab.show()    