import random, math, getopt, sys,re,os, numpy as np, matplotlib.pyplot as plt

# Used to show precisely which revision of code was used
# This comes from the Subversion repository

def get_revision():
    match=re.match('.* ([0-9]+) .*','$LastChangedRevision: 931 $')
    return int(match.group(1))

# Used to create heading identifying program and revision

def produced_by():
    return 'Produced by: {0}, revision {1}'.format(os.path.basename(__file__),get_revision())

# Volume of unit sphere of specified dimension

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

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
        z=random.uniform(-1,1)
        if radius_squared+z*z<1:
            n_hits+=1
    
    Q = 2*n_hits/n_trials
    V*=Q

    return V

#---------------------- Main program ---------------------------------
#
# NB, I tried to calculate the error using sqrt(<V_sph(20)^2> - <V_sph(20)>^2)/sqrt(n_runs)
# but this gives a domain error (real sqrt of number a negative number), so I chand to the "traditional"
# definition of standard deviation (sqrt of sum (v-average)**2 all divided by n_trials.
#
# sqrt(<V_sph(20)^2> - <V_sph(20)>^2)/sqrt(n_runs) is less labour intensive (I was
# taught to use it 40 years ago with a hand calculator), but the slight gain in efficiency
# isn't worth the problems caused by roundoff error on a fully atomated calculation.

if __name__=='__main__':
    print (produced_by())
    n_runs=20
    print ('n_trials | <V_sph(20)> |  V_sph(20) (exact) | error | difference')
    for n_trials in [1,10, 100,1000,10000,100000,1000000]:
        Vs=[]
        for n_runs in range(n_runs):
            V=1
            for d in range(1,21):
                V=run(d,n_trials,0.5,0,V)
            Vs.append(V)
        V_Average=sum(Vs)/n_runs
        error=math.sqrt(sum([(v-V_Average)*(v-V_Average) for v in Vs])/n_runs)
        print ('{0:9d}|{1:12.6f}|{2:16.6f}     |{3:7.4f}|{4:12.4f}'.\
               format(n_trials,V_Average,V_sph(20),error,abs(V_Average-V_sph(20))))