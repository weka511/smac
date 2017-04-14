import random, pylab, os, math

# Extract root of file name, so we can use it as name of plot
def figure_path(ext='png'):
    root,_=os.path.splitext(os.path.split(__file__)[-1])    
    return '{0}.{1}'.format(root,ext)

# Select one position in L, then take a single step.
# If new position invalid, stay put

def markov_step(sigma,delta):
    a = random.choice(L)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
    if not (box_cond or min_dist < 4.0 * sigma ** 2):
        a[:] = b

# Do one complete markov evolution (n_runs steps) and return
# the x coordinate (index=0) after each step, or the y coordinate (index=1)

def markov_run(n_runs,sigma,delta,index=0):
    trace=[]
    for step in range(n_runs):
        markov_step(sigma,delta)
        for disk in L:
            trace.append(disk[index])
    return trace

L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
V = 1
N = len(L)

eta = 0.18
sigma = math.sqrt(eta*V/(math.pi*N))
delta = 0.1
del_xy = 0.05

n_runs = 20000000


histo_data=markov_run(n_runs, sigma,delta)

pylab.hist(histo_data, bins=100, normed=True)
pylab.xlabel('x')
pylab.ylabel('frequency')
pylab.title(                                                                      \
    'Markov Disks: x coordinate histogram (density eta={0:4.2f})\nProduced by {1}'.\
            format(eta,os.path.split(__file__)[-1]))
pylab.grid()
pylab.savefig(figure_path())
pylab.show()