import random, pylab, os

def figure_path(ext='png'):
    root,_=os.path.splitext(os.path.split(__file__)[-1])    
    return '{0}.{1}'.format(root,ext)

def direct_disks_box(N, sigma):
    overlap = True
    while overlap == True:
        L = [(random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))]
        for k in range(1, N):
            a = (random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))
            min_dist_sq = min(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in L)
            if min_dist_sq < 4.0 * sigma ** 2:
                overlap = True
                break
            else:
                overlap = False
                L.append(a)
    return L

N = 4
sigma = 0.1197
n_runs = 1000000
histo_data = []
for run in range(n_runs):
    pos = direct_disks_box(N, sigma)
    for k in range(N):
        histo_data.append(pos[k][0])
pylab.hist(histo_data, bins=100, normed=True)
pylab.xlabel('x')
pylab.ylabel('frequency')
pylab.title(                                                                      \
    'Direct sampling: x coordinate histogram (density eta=0.18)\nProduced by {0}'.\
            format(os.path.split(__file__)[-1]))
pylab.grid()
pylab.savefig(figure_path())
pylab.show()