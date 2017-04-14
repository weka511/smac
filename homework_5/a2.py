import random, math, pylab

# Compute harmonica wave function

def psi_n_square(x, n):
    if n == -1:
        return 0.0
    else:
        psi = [math.exp(-x ** 2 / 2.0) / math.pi ** 0.25]
        psi.append(math.sqrt(2.0) * x * psi[0])
        for k in range(2, n + 1):
            psi.append(math.sqrt(2.0 / k) * x * psi[k - 1] -
                       math.sqrt((k - 1.0) / k) * psi[k - 2])
        return psi[n] ** 2

# Theoretical probability density

def pi_quant(x):
    return math.sqrt( math.tanh(beta/2) / math.pi)* math.exp( - x*x * math.tanh(beta/2) )

# Potential

def pi_class(x):
    return math.sqrt(beta/ (2*math.pi))*math.exp(- beta * x*x/ 2)
    
if __name__=='__main__': 
    figure_number = 1
    for beta in [0.2, 1, 5]:
        (x,n) = (0.0,0)   # Starting position

        delta = 0.5
        data = []
 
        for k in range(5000000):
            # Attempt to move from (x,n) to (x_new,n)
            x_new = x + random.uniform(-delta, delta)
            psi=psi_n_square(x,n)
            m1 = psi_n_square(x_new,n)/psi if psi!=0 else 1
            if random.uniform(0.0, 1.0) <  m1: 
                x = x_new
            # Attempt to move from (x,n) to (x,n+/-1)
            m = n + random.choice([-1,1])
            if m>=0:
                psi_m_square_v = psi_n_square(x,m) 
                psi_n_square_v = psi_n_square(x,n)
                mult_x = psi_m_square_v/psi_n_square_v if psi_n_square_v>0 else 1
                mult_mn= math.exp(-beta*(m-n))
                if random.uniform(0.0,1.0) < mult_x*mult_mn:
                    n = m
            data.append((x,n))
            
        pylab.figure(figure_number)
        figure_number+=1
        pylab.hist([x for (x,_) in data], 100, normed = 'True',label='Histogram')
        x = [a / 10.0 for a in range(-50, 51)]
        y_quant = [pi_quant(a) for a in x]
        y_class = [pi_class(a) for a in x]
        pylab.plot(x, y_quant, c='red', linewidth=2.0,label='Exact Quantum Distribution')
        pylab.plot(x, y_class, c='magenta', linewidth=2.0,label='Classical Potential')
        pylab.title(r'$Distribution for\ {0}\ samples\ and \ \beta = {1}$'.format(len(data),beta), fontsize = 18)
        pylab.xlabel('$x$', fontsize = 30)
        pylab.ylabel('$Probability$', fontsize = 20)
        pylab.legend(loc='upper left',framealpha=0.5)
        pylab.savefig('plot_harmonic_beta_{0}.png'.format(beta))
    
    pylab.show()
