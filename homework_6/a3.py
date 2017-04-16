'''
Peer-graded Assignment: Path sampling: A firework of algorithms
'''

import random, math, pylab

def gauss_cut(cut=1.0):
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= cut:
            return x

def compare(x1s,y1s,x2s,y2s,bins=(30,30),xmin=-1,xmax=+1,ymin=-1,ymax=+1):
    w,h=bins
    def histogram(xs,ys):
        def index (u,umin,umax,r):
            return int((r-1)*(u-umin)/(umax-umin))
        counts = [[0 for x in range(w)] for y in range(h)]
        for x,y in zip(xs,ys):
            i = index(x,xmin,xmax,w)
            j = index(y,ymin,ymax,h)
            counts[i][j]+=1
        return counts
    h1=[item for sublist in histogram(x1s,y1s) for item in sublist]
    h2=[item for sublist in histogram(x2s,y2s) for item in sublist]
    h3=[abs (a/b if b>0 else 1 if a==0 else 0) for (a,b) in zip(h1,h2)]
    iis = [i for i in range(len(h1))]
    pylab.plot(iis,h3,'g') # iis,h1,'r',iis,h2,'b',
    
alpha = 0.5
nsteps = 1000000

def evolve(proposer=lambda: random.uniform(-1.0, 1.0),
          accepter=lambda x,y: math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4))):
    samples_x = []
    samples_y = []
    x, y = 0.0, 0.0
    for step in range(nsteps):
        xnew = proposer()
        ynew = proposer()
        exp_new = accepter(xnew,ynew)
        exp_old = accepter(x,y)
        if random.uniform(0.0, 1.0) < math.exp(exp_new - exp_old):
            x = xnew
            y = ynew
        samples_x.append(x)
        samples_y.append(y)
    return (samples_x, samples_y)

def plot(name,samples_x, samples_y):
    pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
    pylab.axis([-1.0, 1.0, -1.0, 1.0])
    cb = pylab.colorbar()
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.title(name)
    pylab.savefig('{0}.png'.format(name))
    
# Evolve and plot with uniform distribution

pylab.figure(1)    
(x1s, y1s)=evolve()
plot('A3_1',x1s, y1s)

# Evolve and plot with gauss_cut

pylab.figure(2) 
(x2s, y2s)=evolve(proposer=gauss_cut, 
                  accepter=lambda x,y: math.exp(- alpha * (x ** 4 + y ** 4)))
plot('A3_2',x2s, y2s)

pylab.figure(3)
compare(x1s,y1s,x2s,y2s)

pylab.show()