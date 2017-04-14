import random, math, getopt, sys

def display(rec,out):
    print (rec)
    out.write(rec+'\n')
    
def run(n_trials):
    with open('run.txt','w') as out:
        display ('N Trials={0}'.format(n_trials),out)
        for delta in [0.062, 0.125, 0.25, 0.5, 0.75, 1.0, 2.0, 4.0]:
            x, y,z = 0.0, 0.0, 0.0
            n_hits = 0
            n_accepted = 0
            for i in range(n_trials):
                if i%1000000==0:
                    print (delta,i)
                del_x, del_y,del_z = random.uniform(-delta, delta), random.uniform(-delta, delta), random.uniform(-delta, delta)
                if (x + del_x)*(x + del_x) + (y + del_y)*(y + del_y)  + (z + del_z)*(z + del_z)<1.0:
                    x, y,z = x + del_x, y + del_y,z + del_z
                    n_accepted+=1
                alpha = random.uniform(-1.0, 1.0)
        
                if x**2 + y**2 +z**2+alpha**2< 1.0:
                    n_hits += 1
             
            display('Delta={0:.3f}, acceptance={1:.2f}, <Q_4>={2:.6f}, diff={3:.2g}'.\
                   format(delta, n_accepted/n_trials, 2*n_hits/n_trials ,abs(2*n_hits/n_trials- 3*math.pi/8)),\
                   out) 
 
if __name__=='__main__':
    N=2**10
    try:
        opts, args = getopt.getopt( \
              sys.argv[1:],\
              'N:',\
              ['n_trials'])
    except getopt.GetoptError:
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ['-N']:
            N=int(arg)    
    run(N)