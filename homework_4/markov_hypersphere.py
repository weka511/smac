import random, math, getopt, sys,re,os, numpy as np, matplotlib.pyplot as plt

# Used to show precisely which revision of code was used
# This comes from the Subversion repository

def get_revision():
    match=re.match('.* ([0-9]+) .*','$LastChangedRevision: 936 $')
    return int(match.group(1))

# Used to create heading identifying program and revision

def produced_by():
    return 'Produced by: {0}, revision {1}'.format(os.path.basename(__file__),get_revision())

# Volume of unit sphere of specified dimension

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

# Generate and display table of volumes (calculated by formula)

def tabulate_volumes(min_d,max_d):
    V_prev=1
    for d in range(min_d, max_d):
        V = V_sph(d)
        print (d, V,V/V_prev)
        V_prev=V

# Calculate volume using Markov Monte Carlo
#
# d         Dimension of sphere
# n_trials  Number of trials
# delta     Used on Markov step
# freq      Used to minitor progress. If freq>0 print number 
#           of trials so far for each 'freq' trials
# V         Volume of sphere of dimension d-1
#
# Return: volume of sphere of dimension d

def run(d,n_trials,delta,freq,V):
    figure=1
    x=[0]*(d-1)
    radius_squared=0
    n_hits = 0
    n_accepted = 0
    rs=[]

    for i in range(n_trials):
        if freq>0 and i>0 and i%freq==0 and n_accepted>0:
            print ('After {0} trials <Q_{1}>={2:.6f}'.format(i,d,2*n_hits/i))
        if len(x)>0:
            k=random.randint(0,len(x)-1)
            x_old =x[k]
            x_new=x_old+random.uniform(-delta,delta)
            radius_squared_new=radius_squared+x_new*x_new-x_old*x_old
            if radius_squared_new<1.0:
                x[k]=x_new
                radius_squared=radius_squared_new
                n_accepted+=1
                if plot:
                    rs.append(math.sqrt(radius_squared))
        z=random.uniform(-1,1)
        if radius_squared+z*z<1:
            n_hits+=1
    
    Q = 2*n_hits/n_trials
    V*=Q                   # Update volume using Q
    
    print ('Delta={0:.3f}, acceptance={1:.2f}, <Q_{2}>={3:.6f}, V_sph({2})={4:.4g}'.\
           format(delta, n_accepted/n_trials, d, Q, V ))  
    
    if plot:
        plt.figure(figure)
        plt.hist(rs, normed=True, facecolor='blue')
        plt.plot(rs,[d*r**(d-1) for r in rs],'r.')
        plt.title('Dimension={0}, N Trials={1}, delta={2:.3f}'.format(d,n_trials, delta))
        plt.xlabel('r')
        plt.ylabel('p')
        plt.savefig('figure{0}.jpg'.format(figure))

    return V

#---------------------- Main program ---------------------------------

if __name__=='__main__':

    print(produced_by())
    #   Program can be executed with optional parameters
    #   N   The number of trials
    #   n   Specify N as 2**n
    #   d   Dimension
    #   D   Dimension (if specifed, program processes dimensions from d to D
    #   p   Used at the command line to generate plots
    #   t   Tabulate volumes of hyperspheres
    #   l   delta
    #   f   Used to stipulate that a line is to be printed every 'f' trials to track progress
    #   b   Used to specifiy a file into which estimates of <Q_d> will be stored so
    #       we can analyze bunching with a separat program

    # Default values - can be overridden by command line parameters (below)
    
    N    = 2**10     # Number of trials
    n     = 0
    d    = 4
    D    = -1
    plot = False
    tab  = False
    delta = 0.75
    freq  = 0
    

    try:
        opts, args = getopt.getopt( \
              sys.argv[1:],\
              'N:n:d:D:ptl:f:',\
              [
                  'n_trials',
                  'log_n_trials',
                  'dimension',
                  'max-dimension',
                  'plot',
                  'tabulate',
                  'delta',
                  'freq'
              ])
        for opt, arg in opts:
            if opt in ['-N','--n_trials'] and n==0:
                N = int(arg)
            if opt in ['-n','--log_n_trials']:
                n = int(arg)
                N = 2**n
            if opt in ['-d','--dimension']:
                d = int(arg)
            if opt in ['-D','--max-dimension']:
                D = int(arg)            
            if opt in ['-p','--plot']:
                plot = True
            if opt in ['-t','--tabulate']:
                tab = True
            if opt in ['-l','--delta']:
                delta = float(arg)
            if opt in ['-f','--freq']:
                freq=int(arg)
                
    except getopt.GetoptError as error:
        print (error)
        sys.exit(2)
    except ValueError as error:
        print ('Error processing option "{0}": {1}'.format(opt,error))
        sys.exit(2)        

    # If number of trials has been epecified as 2**n, freq is specifed the same way
    if n>0 and freq>0:
        freq=2**freq
    
    if D<0:
        D = d
    if tab:
        tabulate_volumes(d,D+1)
     
    print ('{0}. Starting {1} trials'.format(produced_by(),N))   

    V = 1      # This is the estimate of the volume, which will be updated each iteration
    Vs = []    # Accumulate data for plotting
    ds = []    # Accumulate data for plotting
    calcs = [] # Accumulate data for plotting
    for dd in range(d,D+1):
        V=run(dd,N,delta,freq,V)
        Vs.append(V)
        ds.append(dd)
        calcs.append(V_sph(dd))
    estimates,=plt.plot(ds,Vs,'ro',label='MCMC')
    theoretical,=plt.plot(ds,calcs,'b-',label='Theoretical')
    plt.yscale('log')
    plt.ylabel('V_Sph(d)')
    plt.xlabel('d')
    plt.title('Volume as a function of dimension')
    plt.legend([estimates,theoretical])
    plt.savefig('C1.png')
    plt.show()
        
    if plot:
        plt.show()  #not needed in IDE, only for command line
        