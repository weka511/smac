# $HeadURL: https://server/svn/sandbox/trunk/smac/homework_3/my_markov_disks.py $
# $LastChangedDate: 2016-06-11 11:30:28 +1200 (Sat, 11 Jun 2016) $
# $LastChangedRevision: 907 $

# This is the program for the 3rd week assignment
# https://www.coursera.org/learn/statistical-mechanics/peer/1aQUN/two-dimensional-liquids-and-solids/submit/preview

import random,math,pylab,os,getopt,sys, cmath, numpy,time

# Calculate distance, assuming periodic boundary conditions
# Snarfed from Coursera SMAC site

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)

# Calculate sigma from eta
def get_sigma_sq(eta):
    return eta/(len(L)*math.pi)

# Take a specified number of Markov Monte Carlo steps
def evolve(n_steps,sigma,delta_mult = 0.5):
    delta = delta_mult*sigma
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min(dist(b,c) for c in L if c != a)
        if not min_dist < 2.0 * sigma:
            a[:] = [coordinate%1.0 for coordinate in b]

# Extract root of the file name for this source file,
# so we can use it as name of plot
def figure_path(N,eta,ext='png'):
    # Count the number of files having same pattern
    # we use this to assign a sequnce number
    
    def count_matches():
        count=0
        ff=create_file_name(N,eta,prefix=root,suffix='',seq=-1)
        for _,_,files in os.walk('.'):
            for file in files:
                if file.startswith(ff) and file.endswith(ext):
                    count+=1
        return count
    
    # get file name, discarding the path to this file
    root,_=os.path.splitext(os.path.split(__file__)[-1])
    return create_file_name(N,eta,prefix=root,suffix=ext,seq=count_matches())

# Plot disks.
def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

# This is used to create file names for the configuration
def create_file_name(N,eta,prefix='disk_configuration',suffix='txt',seq=-1):
    file_name= '{0}_N{1}_eta{2:.2f}_{3}.{4}'.format(prefix,N, eta,seq,suffix)
    if file_name.endswith('.'):
        file_name=file_name[:-1]
    return file_name.replace('_-1','')

# Create an absolutely random configuration (used only for testing)

def create_configuration_random():
    L = []
    for k in range(3):
        L.append([random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)])
    return L

# Create an organized square configuration

def create_configuration_square(delxy,N_sqrt):
    two_delxy=2.0*delxy
    return [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(N_sqrt) for j in range(N_sqrt)]

# Try to open configuration file. If there is none,
# Use the function parameter create_configuration to create a new configuration
def start(filename,create_configuration=create_configuration_random):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        L = []
        for line in f:
            a, b = line.split()
            L.append([float(a), float(b)])
        f.close()
        print ('starting from file', filename)
        return L
    else:
        print ('starting from a new configuration')
        return create_configuration()

# Save configuration in file

def save(filename):
    f = open(filename, 'w')
    for a in L:
        f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
    f.close()    

# Snarfed from Coursera SMAC site

def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

# Snarfed from Coursera SMAC site

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)

# Compute average PSI_6 and print it
# NB, this can take a long time to execute, so we reassure the user by
# printing eta and the elapsed time for each step
def plot_psi(eta,n_steps_per_psi=100, n_steps_per_eta=10000):
    etas=[]
    average_psis=[]
    while eta>=0.2:
        start_time=time.time()
        sigma=math.sqrt(get_sigma_sq(eta))
        psis=[]
        for i in range(0,n_steps_per_psi+n_steps_per_eta,n_steps_per_psi):
            evolve(n_steps_per_psi,sigma)
            psis.append(abs(Psi_6(L, sigma)))
        etas.append(eta)
        average_psis.append(numpy.mean(psis))
        print('eta={0:.2f}, elapsed time={1:.0f} sec.'.format(eta,time.time()-start_time))
        eta-=0.02
        
    pylab.plot(etas,average_psis,'bo')
    pylab.xlabel(r'$\eta$')             #use latex to diplay symbols properly
    pylab.ylabel(r'$\Psi_{6}$')         #see http://matplotlib.org/users/mathtext.html
    pylab.title('Variation of global order parameter with density\nn_steps_per_psi={0},n_steps_per_eta={1}'.\
                format(n_steps_per_psi,n_steps_per_eta))
    pylab.savefig('Psi_6.png')
    pylab.show()

# Here is the main program. The command line parameters permit us to do
#  section B and section C things    
if __name__=='__main__':
    N               = 256
    eta             = 0.42
    n_steps         = 10000   
    should_plot_psi = False    #used for section C only
    n_steps_per_psi = 100      #used for section C only
    n_steps_per_eta = 10000    #used for section C only
    try:
        opts, args = getopt.getopt( \
              sys.argv[1:],\
              'N:e:n:p:',\
              ['eta','n_steps','psi'])
    except getopt.GetoptError:
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ['-N']:
            N=int(arg)
        elif opt in ['-e','--eta']:
            eta=float(arg)         
        elif opt in ['-n','--n_steps']:
            n_steps=int(arg)
        elif opt in ['-p','--psi']:  #used for section C only
            should_plot_psi = True
            pp=arg.split(',')
            if len(pp)==2:
                n_steps_per_psi=int(pp[0])
                n_steps_per_eta=int(pp[1]) 
                
    n_sqrt=int(math.sqrt(N))
    if n_sqrt*n_sqrt==N:
        delxy=1.0/(2*n_sqrt)
        filename=create_file_name(N,eta)
        L= start(filename,lambda : create_configuration_square(delxy,n_sqrt))
        if should_plot_psi:
            plot_psi(eta,n_steps_per_psi,n_steps_per_eta)
        else:
            sigma=math.sqrt(get_sigma_sq(eta))
            evolve(n_steps,sigma) 
            title='Configuration for eta={0:.2f} after {1} steps.'.format(eta,n_steps)
            show_conf(L,sigma,title,figure_path(N,eta,ext='png'))
            save(filename)
    else:
        print ('{0} is not a square number'.format(N))
        
