'''Compute acceptance probability for hard disks as a function of density'''
from math    import exp, pi, sqrt
from random  import random
from os.path import splitext, split
from pylab   import figure, hist, legend, plot, savefig, show, title, xlabel, ylabel

def figure_path(ext='png'):
    '''Extract root of file name, so we can use it as name of plot'''
    root,_ = splitext(split(__file__)[-1])
    return '{0}.{1}'.format(root,ext)


def dist(x, y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  sqrt(d_x**2 + d_y**2)

N            = 16
n_confs      = 10 ** 5
pairs        = [(i, j) for i in range(N - 1) for j in range(i + 1, N)]
eta_max_list = []
for conf in range(n_confs):
    L         = [(random(), random()) for k in range(N)]
    sigma_max = min(dist(L[i], L[j]) for i, j in pairs) / 2.0
    eta_max   = N * pi * sigma_max ** 2
    eta_max_list.append(eta_max)

# Begin of graphics output
figure()
_, bins, _ = hist(eta_max_list, 100,
                  histtype   = 'step',
                  cumulative = -1,
                  log        = True,
                  density    = True,
                  label      = "numerical evaluation of p_accept")
explaw    = [exp( - 2.0 * (N - 1) * eta) for eta in bins]
plot(bins, explaw, 'r--', linewidth=1.5, label="1st order virial expansion")
xlabel('density eta')
ylabel('p_accept(eta)')
legend()
savefig(figure_path())
show()

