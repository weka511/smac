import math, numpy, pylab

def V(x,cubic, quartic):
    return x*x* (0.5 + x*(cubic+x*quartic))

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))


def rho_anharmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * ( V(x,cubic, quartic) +  V(xp,cubic, quartic))) \
                         for x in grid] for xp in grid])

# Theoretical probability density for Harmonic
# I've kept this, as it shows the diffeence between harmonic and anharmonic
def pi_quant(x):
    return math.sqrt( math.tanh(beta/2) / math.pi)* math.exp( - x*x * math.tanh(beta/2) )

if __name__=='__main__':
    quartic=1
    cubic= - quartic
    x_max = 5.0
    nx = 100
    dx = 2.0 * x_max / (nx - 1)
    x = [i * dx for i in range(-(nx - 1) // 2, nx // 2 + 1)]
    beta_tmp = 2.0 ** (-5)                   # initial value of beta (power of 2)
    beta     = 2.0 ** 2                      # actual value of beta (power of 2)
    rho = rho_anharmonic_trotter(x, beta_tmp)  # density matrix at initial beta
    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        beta_tmp *= 2.0
        print ('beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp))
    
    Z = sum(rho[j, j] for j in range(nx + 1)) * dx
    pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]
    with open('data_anharmonic_matrixsquaring_beta_{0}.dat'.format(beta), 'w') as f:
        for j in range(nx + 1):
            f.write('{0} {1}\n'.format(x[j], rho[j, j] / Z))
    
    psi_from_matrix_squaring=[rho[j, j] / Z for j in range(nx + 1) ] 
    pi_quants=[pi_quant(a) for a in x]    
    pylab.plot(x,psi_from_matrix_squaring,marker='o',label='Matrix Squaring')
    pylab.plot(x,pi_quants,c='r',label='Theoretical for Harmonic')
    pylab.title(r'$Distribution for \ \beta = {0}$'.format(beta), fontsize = 20)
    pylab.xlabel('$x$', fontsize = 30)
    pylab.ylabel('$Probability$', fontsize = 20)
    pylab.legend(loc='upper left',framealpha=0.5)
    pylab.savefig('plot_square_anharmonic_beta_{0}.png'.format(beta))

pylab.show()    